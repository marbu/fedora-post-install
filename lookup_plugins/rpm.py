# -*- coding: utf-8 -*-

# Copyright (C) 2016 Martin Bukatovič <martin.bukatovic@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

# make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import subprocess

from ansible.plugins.lookup import LookupBase


class LookupModule(LookupBase):

    def run(self, terms, variables=None, **kwargs):
        results = []
        for package_name in terms:
            try:
                package_nevra = subprocess.check_output(
                    ['rpm', '-q', package_name])
                package_nevra = package_nevra.rstrip('\n')
            except subprocess.CalledProcessError:
                package_nevra = ""
            results.append(package_nevra)
        return results
