#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import sys

from neodroid.models import ReactionParameters
from .ucb1 import UCB1

__author__ = 'cnheider'

import neodroid.api_wrappers.single_environment_wrapper as neo
from neodroid import messaging


def construct_displayables(normed, tries, totals):
  d1 = messaging.N.Displayable('BeliefBarLeftDisplayer', normed[0])
  d2 = messaging.N.Displayable('BeliefBarMiddleDisplayer', normed[1])
  d3 = messaging.N.Displayable('BeliefBarRightDisplayer', normed[2])
  d12 = messaging.N.Displayable('BeliefTextLeftDisplayer', normed[0])
  d22 = messaging.N.Displayable('BeliefTextMiddleDisplayer', normed[1])
  d32 = messaging.N.Displayable('BeliefTextRightDisplayer', normed[2])
  d13 = messaging.N.Displayable('CountTextLeftDisplayer', f'{totals[0]} / {tries[0]}')
  d23 = messaging.N.Displayable('CountTextMiddleDisplayer', f'{totals[1]} / {tries[1]}')
  d33 = messaging.N.Displayable('CountTextRightDisplayer', f'{totals[2]} / {tries[2]}')
  return [d1, d2, d3, d12, d22, d32, d13, d23, d33]


def main(connect_to_running=False):
  parser = argparse.ArgumentParser(prog='mab')
  parser.add_argument('-C',
                      action='store_true',
                      help='connect to running',
                      default=connect_to_running)
  args = parser.parse_args()
  if args.C:
    connect_to_running = True

  _environment = neo.SingleEnvironmentWrapper(environment_name='mab',
                                              connect_to_running=connect_to_running)

  num_arms = _environment.action_space.num_discrete_actions

  beliefs = [1 / num_arms] * num_arms
  totals = [0] * num_arms
  tries = [0] * num_arms
  normed = [1 / num_arms] * num_arms

  ucb1 = UCB1(num_arms)

  i = 0
  while _environment.is_connected:
    action = int(ucb1.select_arm())

    motions = [messaging.N.Motion('MultiArmedBanditKillableActor',
                                  'MultiArmedBanditMotor',
                                  action)]

    i += 1

    reaction = messaging.N.Reaction(motions=motions,
                                    displayables=construct_displayables(normed, tries, totals),
                                    parameters=ReactionParameters(step=True,
                                                                  episode_count=True,
                                                                  terminable=True),
                                    serialised_message='this is a serialised_message'
                                    )

    _, signal, terminated, info = _environment.react(reaction).to_gym_like_output()

    ucb1.update_belief(action, signal)

    tries[action] += 1
    totals[action] += signal
    beliefs[action] = float(totals[action]) / tries[action]

    for i in range(len(beliefs)):
      normed[i] = beliefs[i] / (sum(beliefs) + sys.float_info.epsilon)

    if terminated:
      print(info.termination_reason)


if __name__ == '__main__':
  main(connect_to_running=True)
