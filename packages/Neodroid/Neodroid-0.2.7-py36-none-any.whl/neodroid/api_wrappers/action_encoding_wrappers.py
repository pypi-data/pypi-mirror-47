#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Any

from neodroid.api_wrappers import NeodroidVectorGymWrapper
from neodroid.utilities.transformations.encodings import signed_ternary_encoding

__author__ = 'cnheider'


class BinaryActionEncodingWrapper(NeodroidVectorGymWrapper):

  def step(self, action: int = 0, **kwargs) -> Any:
    ternary_action = signed_ternary_encoding(size=self.action_space.n,
                                             index=action)
    return super().step(ternary_action, **kwargs)

  @property
  def action_space(self):
    self.act_spc = super().action_space

    return self.act_spc
