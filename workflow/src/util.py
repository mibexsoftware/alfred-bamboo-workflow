# -*- coding: utf-8 -*-
from HTMLParser import HTMLParser
import subprocess

from src import HELP_URL, __version__
from src.lib.workflow import Workflow

# inspired by https://github.com/idpaterson/alfred-wunderlist-workflow
_workflow = None


def workflow():
    global _workflow
    if _workflow is None:
        _workflow = Workflow(
            help_url=HELP_URL,
            update_settings={
                'github_slug': 'mibexsoftware/alfred-bamboo-workflow',
                'frequency': 1,
                'version': __version__
            }
        )
    return _workflow


def call_alfred(args):
    alfred_major_version = workflow().alfred_env['version'][0]
    subprocess.call([
        '/usr/bin/env', 'osascript', '-l', 'JavaScript',
        'launcher/launch_alfred.scpt', args, alfred_major_version
    ])


class HtmlStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.content = []

    def handle_data(self, d):
        self.content.append(d)

    def get_data(self):
        return ''.join(self.content)


def strip_tags(html):
    s = HtmlStripper()
    s.feed(html)
    return s.get_data()
