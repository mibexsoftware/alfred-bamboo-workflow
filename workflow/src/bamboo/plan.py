# -*- coding: utf-8 -*-

from src.bamboo import EqualityMixin


class Plan(EqualityMixin):
    def __init__(self, plan_key, project_key, name, description, link, is_favourite, enabled):
        self.plan_key = plan_key
        self.project_key = project_key
        self.name = name
        self.description = description
        self.link = link
        self.is_favourite = is_favourite
        self.enabled = enabled
        self._branches = []

    @property
    def branches(self):
        return self._branches

    @branches.setter
    def branches(self, value):
        self._branches = value

    @classmethod
    def from_json(cls, json):
        plan = cls(json['key'],
                   json['projectKey'],
                   json['name'],
                   json.get('description', ''),  # not every plan has a description
                   json['link']['href'],
                   json['isFavourite'],
                   json['enabled'])
        return plan

    def __str__(self):
        return ('Plan(plan_key="{}", project_key="{}", name="{}", '
                'description="{}", link="{}", is_favourite="{}", enabled="{}")'.format(self.plan_key,
                                                                                       self.project_key,
                                                                                       self.name,
                                                                                       self.description,
                                                                                       self.link,
                                                                                       self.is_favourite,
                                                                                       self.enabled))
