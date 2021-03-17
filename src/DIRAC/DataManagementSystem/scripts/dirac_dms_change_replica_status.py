#! /usr/bin/env python
"""
Change status of replica of a given file or a list of files at a given Storage Element

Usage:
  dirac-dms-change-replica-status <lfn | fileContainingLfns> <SE> <status>
"""
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

__RCSID__ = "$Id$"

import os

from DIRAC import exit as DIRACExit
from DIRAC.Core.Utilities.DIRACScript import DIRACScript


@DIRACScript()
def main(self):
  self.registerArgument(("LocalFile: Path to local file containing LFNs",
                         "LFN:       Logical File Names"))
  self.registerArgument(" SE:        Storage Element")
  self.registerArgument(" status:    status")

  self.parseCommandLine()

  from DIRAC.Resources.Catalog.FileCatalog import FileCatalog
  catalog = FileCatalog()

  inputFileName, se, newStatus = self.getPositionalArgs(group=True)

  if os.path.exists(inputFileName):
    inputFile = open(inputFileName, 'r')
    string = inputFile.read()
    lfns = string.splitlines()
    inputFile.close()
  else:
    lfns = [inputFileName]

  res = catalog.getReplicas(lfns, True)
  if not res['OK']:
    print(res['Message'])
    DIRACExit(-1)
  replicas = res['Value']['Successful']

  lfnDict = {}
  for lfn in lfns:
    lfnDict[lfn] = {}
    lfnDict[lfn]['SE'] = se
    lfnDict[lfn]['Status'] = newStatus
    lfnDict[lfn]['PFN'] = replicas[lfn][se]

  res = catalog.setReplicaStatus(lfnDict)
  if not res['OK']:
    print("ERROR:", res['Message'])
  if res['Value']['Failed']:
    print("Failed to update %d replica status" % len(res['Value']['Failed']))
  if res['Value']['Successful']:
    print("Successfully updated %d replica status" % len(res['Value']['Successful']))


if __name__ == "__main__":
  main()  # pylint: disable=no-value-for-parameter
