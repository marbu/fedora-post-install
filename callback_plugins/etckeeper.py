# -*- coding: utf-8 -*-

# Copyright 2016 Martin Bukatovič <martin.bukatovic@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


import os
import subprocess

# another python3-ish hack
try:
    from subprocess import DEVNULL
except ImportError:
    DEVNULL = open(os.devnull, 'w')

from ansible.plugins.callback import CallbackBase
from ansible import constants as C


def etckeeper_unclean():
    """
    Return True if etckeeper repository is in unclean state (there are
    uncommited changes in /etc directory).
    """
    retcode = subprocess.call(['etckeeper', 'unclean'])
    return retcode == 0


class CallbackModule(CallbackBase):
    """
    Initial version (see limitations below) of ansible etckeeper integration
    plugin.

    The idea is to have nice etckeeper commit for every ansible task (when
    a task uses with_items, only single commit is created).

    Current limitations:

    * ``connection: local`` only (the plugin doesn't handle remore hosts)
    * ansible-playbook process is expected to run under root account (so that
      this plugin can run etckeeper to create new commits)
    * git only
    """
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = None # TODO: specify the type properly
    CALLBACK_NAME = 'etckeeper'
    CALLBACK_NEEDS_WHITELIST = True

    def __init__(self):
        super(CallbackModule, self).__init__()
        # make ansible immeditally fail when uncommited changes are detected
        self._on_start()

    def _do_nothing(self):
        """
        Check if etckeeper is installed and initialized to return True when the
        plugin is expected to do nothing.

        Reasoning: loading this plugin should not break ansible functionality
        when etckeeper is either not installed or not configured. Moreover we
        need to check etckeeper installation and configuration status every
        time again to make it possible to setup etckeeper with this plugin
        enabled, expecting it to work immediately after eckeeper setup.
        """
        # TODO: cache status to not check this every time over and over again
        retcode = subprocess.call(
            ['which', 'etckeeper'], stdout=DEVNULL, stderr=DEVNULL)
        etckeeper_installed = retcode == 0
        if not etckeeper_installed:
            return True
        # HACK: this is git only
        retcode = subprocess.call(
            ['etckeeper', 'vcs', 'rev-parse', 'HEAD'],
            stdout=DEVNULL, stderr=DEVNULL)
        etckeeper_initialized = retcode == 0
        return not etckeeper_initialized

    #
    # start callbacks
    #

    def _on_start(self):
        if self._do_nothing():
            return
        # when etckeeper repo contains uncommited changes, show a warning
        if etckeeper_unclean():
            raise Exception("etckeeper repository is unclean")

    def v2_playbook_on_start(self, playbook):
        self._on_start()

    def v2_playbook_on_play_start(self, play):
        self._on_start()

    def v2_playbook_on_task_start(self, task, is_conditional):
        self._on_start()

    def v2_playbook_on_handler_task_start(self, task):
        self._on_start()

    #
    # result callbacks
    #

    def v2_runner_on_failed(self, result, ignore_errors=False):
        # keep any changes uncommited
        pass

    def v2_runner_on_ok(self, result):
        if self._do_nothing():
            return
        if result.is_changed():
            msg = "{0}\n\n{1}".format(
                result._task.name,
                "Committing changes in /etc after successful ansible task.")
            retcode = subprocess.call(['etckeeper', 'commit', msg])
            print("etckeeper retcode:", retcode)
        elif etckeeper_unclean():
            msg = (
                "etckeeper repository is unclean "
                "(there are uncommited changes in /etc repository), "
                "but the task result is 'ok' (unchanged)")
            raise Exception(msg)
