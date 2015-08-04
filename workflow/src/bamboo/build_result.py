# -*- coding: utf-8 -*-

from src.bamboo import EqualityMixin


class BuildResult(EqualityMixin):
    def __init__(self, build_state, build_number, build_result_key,
                 test_summary, duration_desc, relative_time, build_reason,
                 plan_key, plan_name, artifact_href, link):
        self.build_state = build_state
        self.build_number = build_number
        self.build_result_key = build_result_key
        self.test_summary = test_summary
        self.duration_desc = duration_desc
        self.relative_time = relative_time
        self.build_reason = build_reason
        self.plan_key = plan_key
        self.plan_name = plan_name
        self.artifact_href = artifact_href
        self.link = link

    def is_failed(self):
        return self.build_state == 'Failed'

    @classmethod
    def from_json(cls, json):
        artifacts = json['artifacts'].get('artifact', [])
        artifact_href = artifacts[0]['link']['href'] if artifacts else ''
        build_result = cls(json['buildState'],
                           json['buildNumber'],
                           json['buildResultKey'],
                           json['buildTestSummary'],
                           json['buildDurationDescription'],
                           json['buildRelativeTime'],
                           json['buildReason'],
                           json['plan']['key'],
                           json['plan']['name'],
                           artifact_href,
                           json['link']['href'])
        return build_result

    def __str__(self):
        return ('BuildResult(buildState="{}", buildNumber="{}", buildResultKey="{}", '
                'test_summary="{}", duration_desc="{}", relative_time="{}", build_reason="{}", '
                'plan_key="{}", plan_name="{}", artifact_href="{}", link="{}"').format(self.build_state,
                                                                                       self.build_number,
                                                                                       self.build_result_key,
                                                                                       self.test_summary,
                                                                                       self.duration_desc,
                                                                                       self.relative_time,
                                                                                       self.build_reason,
                                                                                       self.plan_key,
                                                                                       self.plan_name,
                                                                                       self.artifact_href,
                                                                                       self.link)
