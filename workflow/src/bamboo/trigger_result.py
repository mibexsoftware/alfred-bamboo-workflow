# -*- coding: utf-8 -*-

from src.bamboo import EqualityMixin


class TriggerResult(EqualityMixin):
    def __init__(self, build_result_key, link):
        self.build_result_key = build_result_key
        self.link = link

    @classmethod
    def from_json(cls, json):
        trigger_result = cls(json['buildResultKey'], json['link']['href'])
        return trigger_result

    def __str__(self):
        return 'TriggerResult(buildResultKey="{}", link="{}")'.format(self.build_result_key, self.link)
