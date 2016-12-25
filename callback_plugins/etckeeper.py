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

    The idea is to have nice etckeeper commit for every ansible task.

    Current limitations:

    * ``connection: local`` only (the plugin doesn't handle remore hosts)
    * ansible-playbook process is expected to run under root account (so that
      this plugin can run etckeeper to create new commits)
    * fedora only
    """
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = None # TODO: specify the type properly
    CALLBACK_NAME = 'etckeeper'
    CALLBACK_NEEDS_WHITELIST = False

    def __init__(self):
        super(CallbackModule, self).__init__()
        self._etckeeper_installed = \
            subprocess.call(['rpm', '-q', 'etckeeper']) == 0
        self._etckeeper_initialized = os.path.exists('/etc/.etckeeper')
        # when etckeeper is not installed or initialized, don't do anything
        if not self._etckeeper_installed or not self._etckeeper_initialized:
            return
        # when etckeeper repo contains uncommited changes, stop right there
        if etckeeper_unclean():
            raise Exception("etckeeper repository is unclean")

    def v2_on_any(self, *args, **kwargs):
        print("plugin: v2_on_any")
