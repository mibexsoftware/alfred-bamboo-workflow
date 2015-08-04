# -*- coding: utf-8 -*-

from unittest import TestCase

from mock import MagicMock, patch
from nose.tools import nottest
from src.routing import route

wf = MagicMock()


def noop(fun):
    pass


class TestConfigure(TestCase):

    def tearDown(self):
        wf.reset_mock()

    @nottest
    @patch('src.util.workflow', return_value=wf)
    @patch('src.util.call_alfred', side_effect=noop)
    def test_delcache_should_invalidate_cache(self, call_alfred_fun, workflow_fun):
        # GIVEN
        # WHEN
        route([':config sync', '--exec'])
        # THEN
        self.assertTrue(wf.clear_cache.called)

    @nottest
    @patch('src.util.workflow', return_value=wf)
    @patch('src.util.call_alfred', side_effect=noop)
    def test_update_should_call_workflow_update(self, call_alfred_fun, workflow_fun):
        # GIVEN
        # WHEN
        route([':config update', '--exec'])
        # THEN
        self.assertTrue(wf.start_update.called)
