# -*- coding: utf-8 -*-

from src.bamboo import EqualityMixin


class Project(EqualityMixin):
    def __init__(self, key, name, link):
        self.key = key
        self.name = name
        self.link = link

    @classmethod
    def from_json(cls, json):
        project = cls(json['key'],
                      json['name'],
                      json['link']['href'])
        return project

    def __str__(self):
        return 'Project(key="{}", name="{}", link="{}")'.format(self.key,
                                                                self.name,
                                                                self.link)
