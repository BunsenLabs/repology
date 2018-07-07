# Copyright (C) 2016-2017 Dmitry Marakasov <amdmi3@amdmi3.ru>
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

from repology.fetchers import Fetcher
from repology.fetchers.state import StateDir
from repology.logger import NoopLogger
from repology.subprocess import RunSubprocess


class WgetTarFetcher(Fetcher):
    def __init__(self, url, fetch_timeout=60):
        self.url = url
        self.fetch_timeout = fetch_timeout

    def Fetch(self, statepath, update=True, logger=NoopLogger()):
        if os.path.isdir(statepath) and not update:
            logger.Log('no update requested, skipping')
            return

        with StateDir(statepath) as statedir:
            tarpath = os.path.join(statedir, '.temporary.tar')
            RunSubprocess(['wget', '--timeout', str(self.fetch_timeout), '--tries', '1', '-O', tarpath, self.url], logger)
            RunSubprocess(['tar', '-x', '-z', '-f', tarpath, '-C', statedir], logger)
            os.remove(tarpath)
