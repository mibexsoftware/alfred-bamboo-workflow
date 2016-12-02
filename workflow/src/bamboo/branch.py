# -*- coding: utf-8 -*-

from src.bamboo import EqualityMixin


class Branch(EqualityMixin):
    def __init__(self, key, name, description, plan_key):
        self.key = key
        self.name = name
        self.description = description
        self.plan_key = plan_key

    @classmethod
    def from_json(cls, json, plan_key):
        branch = cls(json['searchEntity']['key'],
                     json['searchEntity']['branchName'],
                     json['searchEntity']['description'] if 'description' in json['searchEntity'] else '',
                     plan_key)
        return branch

    def __str__(self):
        return 'Branch(key="{}", name="{}", description="{}", plan_key="{}"'.format(self.key,
                                                                                    self.name,
                                                                                    self.description,
                                                                                    self.plan_key)
