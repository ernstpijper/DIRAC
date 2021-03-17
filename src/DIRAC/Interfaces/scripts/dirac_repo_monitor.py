#!/usr/bin/env python
"""
Monitor the jobs present in the repository
"""
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

__RCSID__ = "$Id$"

import DIRAC
from DIRAC.Core.Utilities.DIRACScript import DIRACScript


@DIRACScript()
def main(self):
  self.registerArgument("RepoDir:  Location of Job Repository")
  _, args = self.parseCommandLine(ignoreErrors=False)

  repoLocation = args[0]
  from DIRAC.Interfaces.API.Dirac import Dirac
  dirac = Dirac(withRepo=True, repoLocation=repoLocation)

  exitCode = 0
  result = dirac.monitorRepository(printOutput=True)
  if not result['OK']:
    print('ERROR: ', result['Message'])
    exitCode = 2

  DIRAC.exit(exitCode)


if __name__ == "__main__":
  main()  # pylint: disable=no-value-for-parameter
