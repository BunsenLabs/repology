# Copyright (C) 2016-2018 Dmitry Marakasov <amdmi3@amdmi3.ru>
#
# This file is part of repology
#
# repology is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# repology is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with repology.  If not, see <http://www.gnu.org/licenses/>.

import os
import re

from repology.parsers import Parser
from repology.parsers.maintainers import extract_maintainers


def normalize_version(version):
    match = re.match('(.*)-r[0-9]+$', version)
    if match is not None:
        version = match.group(1)

    return version


class ApkIndexParser(Parser):
    def iter_parse(self, path, factory):
        with open(os.path.join(path, 'APKINDEX'), 'r', encoding='utf-8') as apkindex:
            state = {}
            for line in apkindex:
                line = line.strip()
                if line:
                    state[line[0]] = line[2:].strip()
                    continue

                # empty line, we can flush our state
                if state and state['P'] == state['o']:
                    pkg = factory.begin()

                    pkg.set_name(state['P'])
                    pkg.set_version(state['V'], normalize_version)

                    pkg.set_summary(state['T'])
                    pkg.add_homepages(state['U'])  # XXX: split?
                    pkg.add_licenses(state['L'])

                    pkg.add_maintainers(extract_maintainers(state.get('m')))

                    yield pkg

                state = {}
