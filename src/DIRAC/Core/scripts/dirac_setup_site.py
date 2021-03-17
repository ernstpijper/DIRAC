#!/usr/bin/env python
########################################################################
# File :    dirac-setup-site
# Author :  Ricardo Graciani
########################################################################
"""
Initial installation and configuration of a new DIRAC server (DBs, Services, Agents, Web Portal,...)
"""
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
__RCSID__ = "$Id$"

from DIRAC import S_OK
from DIRAC.Core.Utilities.DIRACScript import DIRACScript


class SetupSite(DIRACScript):

  def initParameters(self):
    self.exitOnError = False

  def setExitOnError(self, value):
    self.exitOnError = True
    return S_OK()


@SetupSite()
def main(self):
  self.disableCS()
  self.registerSwitch("e", "exitOnError",
                      "flag to exit on error of any component installation",
                      self.setExitOnError)

  self.addDefaultOptionValue('/DIRAC/Security/UseServerCertificate', 'yes')
  self.addDefaultOptionValue('LogLevel', 'INFO')
  self.parseCommandLine()
  args = self.getExtraCLICFGFiles()

  if len(args) > 1:
    self.showHelp(exitCode=1)

  cfg = None
  if len(args):
    cfg = args[0]
  from DIRAC.FrameworkSystem.Client.ComponentInstaller import gComponentInstaller

  gComponentInstaller.exitOnError = self.exitOnError

  result = gComponentInstaller.setupSite(self.localCfg, cfg)
  if not result['OK']:
    print("ERROR:", result['Message'])
    exit(-1)

  result = gComponentInstaller.getStartupComponentStatus([])
  if not result['OK']:
    print('ERROR:', result['Message'])
    exit(-1)

  print("\nStatus of installed components:\n")
  result = gComponentInstaller.printStartupStatus(result['Value'])
  if not result['OK']:
    print('ERROR:', result['Message'])
    exit(-1)


if __name__ == "__main__":
  main()  # pylint: disable=no-value-for-parameter
