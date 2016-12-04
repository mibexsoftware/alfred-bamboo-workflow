# -*- coding: utf-8 -*-

from unittest import TestCase

import httpretty
from src.bamboo.bamboo_facade import BambooFacade
from src.bamboo.branch import Branch
from src.bamboo.build_result import BuildResult
from src.bamboo.plan import Plan
from src.bamboo.project import Project
from src.bamboo.trigger_result import TriggerResult


class TestBambooFacade(TestCase):
    def setUp(self):
        self.bamboo_facade = BambooFacade(bamboo_host="http://localhost:7990/bamboo")

    @httpretty.activate
    def test_get_all_projects(self):
        # GIVEN
        self._mock_projects_rest_call()
        # WHEN
        projects = self.bamboo_facade.projects()
        # THEN
        self.assertEquals(
            [Project(key="COMMONS",
                     name="Commons Lang",
                     link="http://localhost:7990/bamboo/rest/api/latest/project/COMMONS"),
             Project(key="TEST",
                     name="Test",
                     link="http://localhost:7990/bamboo/rest/api/latest/project/TEST"),
             Project(key="MIRA",
                     name="Mira",
                     link="http://localhost:7990/bamboo/rest/api/latest/project/MIRA")],
            projects
        )

    @httpretty.activate
    def test_get_all_plans_paged(self):
        # GIVEN
        self._mock_plans_rest_call()
        # WHEN
        plans = self.bamboo_facade.plans()
        # THEN
        self.assertEquals([Plan(plan_key='MIRA-RSS',
                                project_key='MIRA',
                                name='Mira - Activity Streams for Stash',
                                link='http://localhost:7990/bamboo/rest/api/latest/plan/MIRA-RSS',
                                description='',
                                is_favourite=False,
                                enabled=True),
                           Plan(plan_key='MIRA-BEAUTIFUL',
                                project_key='MIRA',
                                name='Mira - Beautilful Math for Confluence',
                                link='http://localhost:7990/bamboo/rest/api/latest/plan/MIRA-BEAUTIFUL',
                                description='',
                                is_favourite=False,
                                enabled=True)],
                          plans)

    @httpretty.activate
    def test_get_branches_for_plan_paged(self):
        # GIVEN
        self._mock_branches_rest_call()
        # WHEN
        plans = self.bamboo_facade.branches(plan_key='MIRA-RSS')
        # THEN
        self.assertEquals([Branch(key='MIRA-RSS',
                                  name='master',
                                  description='',
                                  plan_key='MIRA-RSS'),
                           Branch(key='MIRA-RSS0',
                                  name='develop',
                                  description='',
                                  plan_key='MIRA-RSS'),
                           Branch(key='MIRA-RSS12',
                                  name='feature-RSS-40-global-activity-stream-fails-when',
                                  description='',
                                  plan_key='MIRA-RSS')],
                          plans)

    @httpretty.activate
    def test_get_bamboo_status_paged(self):
        # GIVEN
        self._mock_status_rest_call()
        # WHEN
        build_results = self.bamboo_facade.results()
        # THEN
        self.assertEquals([BuildResult(build_state='Successful',
                                       build_number=14,
                                       build_result_key='MIRA-RSS-14',
                                       test_summary='28 passed',
                                       duration_desc='48 seconds',
                                       relative_time='1 week ago',
                                       build_reason='',
                                       plan_key='MIRA-RSS',
                                       plan_name='Mira - Activity Streams for Stash',
                                       artifact_href='http://localhost:7990/bamboo/browse/MIRA-RSS-14/artifact/shared/Activity-Streams-for-Stash/target',
                                       link='http://localhost:7990/bamboo/rest/api/latest/result/MIRA-RSS-14',
                                       completed_date='2015-07-21T15:32:31.000+02:00'),
                           BuildResult(build_state='Failed',
                                       build_number=7,
                                       build_result_key='MIRA-BEAUTIFUL-7',
                                       test_summary='No tests found',
                                       duration_desc='3 seconds',
                                       relative_time='2 weeks ago',
                                       build_reason='',
                                       plan_key='MIRA-BEAUTIFUL',
                                       plan_name='Mira - Beautilful Math for Confluence',
                                       artifact_href='',
                                       link='http://localhost:7990/bamboo/rest/api/latest/result/MIRA-BEAUTIFUL-7',
                                       completed_date='2015-07-14T16:13:29.000+02:00')
                           ], build_results)

    @httpretty.activate
    def test_is_running(self):
        # GIVEN
        httpretty.register_uri(httpretty.GET, "http://localhost:7990/bamboo/rest/api/latest/info",
                               body='''{
                                        "state": "RUNNING",
                                        "reindexInProgress": false
                                    }''')
        # WHEN
        is_running = self.bamboo_facade.is_running()
        # THEN
        self.assertTrue(is_running)

    @httpretty.activate
    def test_trigger_build(self):
        # GIVEN
        httpretty.register_uri(httpretty.POST, "http://localhost:7990/bamboo/rest/api/latest/queue/MIRA-RSS4",
                               body='''{
                                   "planKey":"MIRA-RSS4",
                                   "buildNumber":5,
                                   "buildResultKey":"MIRA-RSS4-5",
                                   "triggerReason":"Manual build",
                                   "link":{"href":"http://localhost:7990/bamboo/rest/api/latest/result/MIRA-RSS4-5","rel":"self"}
                               }''')
        # WHEN
        trigger_result = self.bamboo_facade.trigger_build(build_key='MIRA-RSS4')
        # THEN
        self.assertEquals(TriggerResult(build_result_key='MIRA-RSS4-5',
                                        link='http://localhost:7990/bamboo/rest/api/latest/result/MIRA-RSS4-5'),
                          trigger_result)

    def _mock_projects_rest_call(self):
        httpretty.register_uri(httpretty.GET, "http://localhost:7990/bamboo/rest/api/latest/project",
                               body='''{
                                      "expand": "projects",
                                      "link": {
                                        "href": "http://localhost:7990/bamboo/rest/api/latest/project",
                                        "rel": "self"
                                      },
                                      "projects": {
                                        "size": 3,
                                        "expand": "project",
                                        "start-index": 0,
                                        "max-result": 3,
                                        "project": [
                                          {
                                            "key": "COMMONS",
                                            "name": "Commons Lang",
                                            "link": {
                                              "href": "http://localhost:7990/bamboo/rest/api/latest/project/COMMONS",
                                              "rel": "self"
                                            }
                                          },
                                          {
                                            "key": "TEST",
                                            "name": "Test",
                                            "link": {
                                              "href": "http://localhost:7990/bamboo/rest/api/latest/project/TEST",
                                              "rel": "self"
                                            }
                                          },
                                          {
                                            "key": "MIRA",
                                            "name": "Mira",
                                            "link": {
                                              "href": "http://localhost:7990/bamboo/rest/api/latest/project/MIRA",
                                              "rel": "self"
                                            }
                                          }
                                        ]
                                      }
                                    }''',
                               content_type="application/json")

    def _mock_plans_rest_call(self):
        httpretty.register_uri(httpretty.GET, "http://localhost:7990/bamboo/rest/api/latest/plan",
                               responses=[
                                   httpretty.Response(body='''
                                   {
                                          "expand": "plans",
                                          "link": {
                                            "href": "http://localhost:7990/bamboo/rest/api/latest/plan",
                                            "rel": "self"
                                          },
                                          "plans": {
                                            "size": 2,
                                            "expand": "plan",
                                            "start-index": 1,
                                            "max-result": 1,
                                            "plan": [
                                              {
                                                "expand": "actions,stages,branches",
                                                "projectKey": "MIRA",
                                                "projectName": "Mira",
                                                "project": {
                                                  "key": "MIRA",
                                                  "name": "Mira",
                                                  "link": {
                                                    "href": "http://localhost:7990/bamboo/rest/api/latest/project/MIRA",
                                                    "rel": "self"
                                                  }
                                                },
                                                "shortName": "Activity Streams for Stash",
                                                "buildName": "Activity Streams for Stash",
                                                "shortKey": "RSS",
                                                "type": "chain",
                                                "enabled": true,
                                                "link": {
                                                  "href": "http://localhost:7990/bamboo/rest/api/latest/plan/MIRA-RSS",
                                                  "rel": "self"
                                                },
                                                "isFavourite": false,
                                                "isActive": false,
                                                "isBuilding": false,
                                                "averageBuildTimeInSeconds": 46,
                                                "actions": {
                                                  "size": 7,
                                                  "start-index": 0,
                                                  "max-result": 7
                                                },
                                                "stages": {
                                                  "size": 2,
                                                  "start-index": 0,
                                                  "max-result": 2
                                                },
                                                "branches": {
                                                  "size": 6,
                                                  "start-index": 0,
                                                  "max-result": 6
                                                },
                                                "key": "MIRA-RSS",
                                                "name": "Mira - Activity Streams for Stash",
                                                "planKey": {
                                                  "key": "MIRA-RSS"
                                                }
                                            }
                                   ]}}'''),
                                   httpretty.Response(body='''
                                   {
                                          "expand": "plans",
                                          "link": {
                                            "href": "http://localhost:7990/bamboo/rest/api/latest/plan",
                                            "rel": "self"
                                          },
                                          "plans": {
                                            "size": 2,
                                            "expand": "plan",
                                            "start-index": 0,
                                            "max-result": 1,
                                            "plan": [
                                              {
                                                "expand": "actions,stages,branches",
                                                "projectKey": "MIRA",
                                                "projectName": "Mira",
                                                "project": {
                                                  "key": "MIRA",
                                                  "name": "Mira",
                                                  "link": {
                                                    "href": "http://localhost:7990/bamboo/rest/api/latest/project/MIRA",
                                                    "rel": "self"
                                                  }
                                                },
                                                "shortName": "Beautilful Math for Confluence",
                                                "buildName": "Beautilful Math for Confluence",
                                                "shortKey": "BEAUTIFUL",
                                                "type": "chain",
                                                "enabled": true,
                                                "link": {
                                                  "href": "http://localhost:7990/bamboo/rest/api/latest/plan/MIRA-BEAUTIFUL",
                                                  "rel": "self"
                                                },
                                                "isFavourite": false,
                                                "isActive": false,
                                                "isBuilding": false,
                                                "averageBuildTimeInSeconds": 2,
                                                "actions": {
                                                  "size": 7,
                                                  "start-index": 0,
                                                  "max-result": 7
                                                },
                                                "stages": {
                                                  "size": 1,
                                                  "start-index": 0,
                                                  "max-result": 1
                                                },
                                                "branches": {
                                                  "size": 4,
                                                  "start-index": 0,
                                                  "max-result": 4
                                                },
                                                "key": "MIRA-BEAUTIFUL",
                                                "name": "Mira - Beautilful Math for Confluence",
                                                "planKey": {
                                                  "key": "MIRA-BEAUTIFUL"
                                                }
                                              }
                                   ]}}''')
                               ],
                               content_type="application/json")

    def _mock_branches_rest_call(self):
        httpretty.register_uri(httpretty.GET, "http://localhost:7990/bamboo/rest/api/latest/search/branches",
                               responses=[
                                   httpretty.Response(body='''
                                   {
                                      "size": 2,
                                      "searchResults": [
                                        {
                                          "id": "MIRA-RSS",
                                          "type": "chain",
                                          "searchEntity": {
                                            "id": "MIRA-RSS",
                                            "key": "MIRA-RSS",
                                            "projectName": "Mira",
                                            "planName": "Activity Streams for Stash",
                                            "branchName": "master",
                                            "description": "",
                                            "type": "chain"
                                          }
                                        },
                                        {
                                          "id": "MIRA-RSS0",
                                          "type": "chain_branch",
                                          "searchEntity": {
                                            "id": "MIRA-RSS0",
                                            "key": "MIRA-RSS0",
                                            "projectName": "Mira",
                                            "planName": "Activity Streams for Stash",
                                            "branchName": "develop",
                                            "description": "",
                                            "type": "chain_branch"
                                          }
                                        }
                                        ],
                                     "start-index": 1,
                                     "max-result": 3
                                   }'''),
                                   httpretty.Response(body='''
                                   {
                                      "size": 1,
                                      "searchResults": [
                                        {
                                          "id": "MIRA-RSS12",
                                          "type": "chain_branch",
                                          "searchEntity": {
                                            "id": "MIRA-RSS12",
                                            "key": "MIRA-RSS12",
                                            "projectName": "Mira",
                                            "planName": "Activity Streams for Stash",
                                            "branchName": "feature-RSS-40-global-activity-stream-fails-when",
                                            "description": "",
                                            "type": "chain_branch"
                                          }
                                        }
                                     ],
                                     "start-index": 0,
                                     "max-result": 3
                                   }'''),
                               ],
                               content_type="application/json")

    def _mock_status_rest_call(self):
        httpretty.register_uri(httpretty.GET, "http://localhost:7990/bamboo/rest/api/latest/result",
                               responses=[
                                   httpretty.Response(body='''
                                   {
                                      "results": {
                                        "size": 2,
                                        "expand": "result",
                                        "start-index": 1,
                                        "max-result": 2,
                                        "result": [
                                          {
                                            "expand": "plan,vcsRevisions,artifacts,comments,labels,jiraIssues,stages",
                                            "link": {
                                              "href": "http://localhost:7990/bamboo/rest/api/latest/result/MIRA-RSS-14",
                                              "rel": "self"
                                            },
                                            "plan": {
                                              "shortName": "Activity Streams for Stash",
                                              "shortKey": "RSS",
                                              "type": "chain",
                                              "enabled": true,
                                              "link": {
                                                "href": "http://localhost:7990/bamboo/rest/api/latest/plan/MIRA-RSS",
                                                "rel": "self"
                                              },
                                              "key": "MIRA-RSS",
                                              "name": "Mira - Activity Streams for Stash",
                                              "planKey": {
                                                "key": "MIRA-RSS"
                                              }
                                            },
                                            "planName": "Activity Streams for Stash",
                                            "projectName": "Mira",
                                            "buildResultKey": "MIRA-RSS-14",
                                            "lifeCycleState": "Finished",
                                            "id": 21365255,
                                            "buildStartedTime": "2015-07-21T15:31:43.000+02:00",
                                            "prettyBuildStartedTime": "Tue, 21 Jul, 03:31 PM",
                                            "buildCompletedTime": "2015-07-21T15:32:31.000+02:00",
                                            "buildCompletedDate": "2015-07-21T15:32:31.000+02:00",
                                            "prettyBuildCompletedTime": "Tue, 21 Jul, 03:32 PM",
                                            "buildDurationInSeconds": 48,
                                            "buildDuration": 48933,
                                            "buildDurationDescription": "48 seconds",
                                            "buildRelativeTime": "1 week ago",
                                            "buildTestSummary": "28 passed",
                                            "buildReason": "",
                                            "reasonSummary": "",
                                            "artifacts": {
                                              "size": 1,
                                              "start-index": 0,
                                              "max-result": 1,
                                              "artifact": [
                                                {
                                                  "name": "Activity Streams for Stash",
                                                  "link": {
                                                    "href": "http://localhost:7990/bamboo/browse/MIRA-RSS-14/artifact/shared/Activity-Streams-for-Stash/target",
                                                    "rel": "self"
                                                  },
                                                  "producerJobKey": "MIRA-RSS-BUIL-14",
                                                  "shared": true,
                                                  "size": 6554084,
                                                  "prettySizeDescription": "6 MB"
                                                }
                                              ]
                                            },
                                            "key": "MIRA-RSS-14",
                                            "planResultKey": {
                                              "key": "MIRA-RSS-14",
                                              "entityKey": {
                                                "key": "MIRA-RSS"
                                              },
                                              "resultNumber": 14
                                            },
                                            "state": "Successful",
                                            "buildState": "Successful",
                                            "number": 14,
                                            "buildNumber": 14
                                          }
                                    ]}}'''),
                                   httpretty.Response(body='''
                                   {
                                      "results": {
                                        "size": 2,
                                        "expand": "result",
                                        "start-index": 0,
                                        "max-result": 2,
                                        "result": [
                                          {
                                            "expand": "plan,vcsRevisions,artifacts,comments,labels,jiraIssues,stages",
                                            "link": {
                                              "href": "http://localhost:7990/bamboo/rest/api/latest/result/MIRA-BEAUTIFUL-7",
                                              "rel": "self"
                                            },
                                            "plan": {
                                              "shortName": "Beautilful Math for Confluence",
                                              "shortKey": "BEAUTIFUL",
                                              "type": "chain",
                                              "enabled": true,
                                              "link": {
                                                "href": "http://localhost:7990/bamboo/rest/api/latest/plan/MIRA-BEAUTIFUL",
                                                "rel": "self"
                                              },
                                              "key": "MIRA-BEAUTIFUL",
                                              "name": "Mira - Beautilful Math for Confluence",
                                              "planKey": {
                                                "key": "MIRA-BEAUTIFUL"
                                              }
                                            },
                                            "planName": "Beautilful Math for Confluence",
                                            "projectName": "Mira",
                                            "buildResultKey": "MIRA-BEAUTIFUL-7",
                                            "lifeCycleState": "Finished",
                                            "id": 21365210,
                                            "buildStartedTime": "2015-07-14T16:13:26.000+02:00",
                                            "prettyBuildStartedTime": "Tue, 14 Jul, 04:13 PM",
                                            "buildCompletedTime": "2015-07-14T16:13:29.000+02:00",
                                            "buildCompletedDate": "2015-07-14T16:13:29.000+02:00",
                                            "prettyBuildCompletedTime": "Tue, 14 Jul, 04:13 PM",
                                            "buildDurationInSeconds": 3,
                                            "buildDuration": 3907,
                                            "buildDurationDescription": "3 seconds",
                                            "buildRelativeTime": "2 weeks ago",
                                            "buildTestSummary": "No tests found",
                                            "buildReason": "",
                                            "reasonSummary": "",
                                            "artifacts": {
                                              "size": 0,
                                              "start-index": 0,
                                              "max-result": 0,
                                              "artifact": []
                                            },

                                            "key": "MIRA-BEAUTIFUL-7",
                                            "planResultKey": {
                                              "key": "MIRA-BEAUTIFUL-7",
                                              "entityKey": {
                                                "key": "MIRA-BEAUTIFUL"
                                              },
                                              "resultNumber": 7
                                            },
                                            "state": "Failed",
                                            "buildState": "Failed",
                                            "number": 7,
                                            "buildNumber": 7
                                          }
                                    ]}}'''),
                               ],
                               content_type="application/json")
