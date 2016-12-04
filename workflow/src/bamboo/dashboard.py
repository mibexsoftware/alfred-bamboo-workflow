# -*- coding: utf-8 -*-

from src.bamboo import EqualityMixin


class DashBoard(EqualityMixin):
    def __init__(self, status, agent_summary, builds):
        self.status = status
        self.agent_summary = agent_summary
        self.builds = builds

    @classmethod
    def from_json(cls, json):
        dashboard = cls(json['status'], json['agentSummary'], json['builds'])
        return dashboard

    def __str__(self):
        return 'Branch(key="{}", name="{}", description="{}", plan_key="{}"'.format(self.key,
                                                                                    self.name,
                                                                                    self.description,
                                                                                    self.plan_key)
