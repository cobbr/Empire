import os.path
from lib.common import helpers

class Module:

    def __init__(self, mainMenu, params=[]):

        self.info = {
            'Name': 'Get-ComputerDetails',

            'Author': ['@JosephBialek'],

            'Description': ('Enumerates useful information on the system. By default, all checks are run.'),

            'Background' : True,

            'OutputExtension' : None,

            'NeedsAdmin' : True,

            'OpsecSafe' : True,

            'MinPSVersion' : '2',

            'Comments': [
                'https://github.com/mattifestation/PowerSploit/blob/master/Recon/Get-ComputerDetails.ps1'
            ]
        }

        # any options needed by the module, settable during runtime
        self.options = {
            # format:
            #   value_name : {description, required, default_value}
            'Agent' : {
                'Description'   :   'Agent to run module on.',
                'Required'      :   True,
                'Value'         :   ''
            },
            '4648' : {
                'Description'   :   'Switch. Only return 4648 logon information (RDP to another machine).',
                'Required'      :   False,
                'Value'         :   ''
            },
            '4624' : {
                'Description'   :   'Switch. Only return 4624 logon information (logons to this machine).',
                'Required'      :   False,
                'Value'         :   ''
            },
            'AppLocker' : {
                'Description'   :   'Switch. Only return AppLocker logs.',
                'Required'      :   False,
                'Value'         :   ''
            },
            'PSScripts' : {
                'Description'   :   'Switch. Only return PowerShell scripts run from operational log.',
                'Required'      :   False,
                'Value'         :   ''
            },
            'SavedRDP' : {
                'Description'   :   'Switch. Only return saved RDP connections.',
                'Required'      :   False,
                'Value'         :   ''
            }
        }

        # save off a copy of the mainMenu object to access external functionality
        #   like listeners/agent handlers/etc.
        self.mainMenu = mainMenu

        for param in params:
            # parameter format is [Name, Value]
            option, value = param
            if option in self.options:
                self.options[option]['Value'] = value


    def generate(self, obfuscate=False, obfuscationCommand=""):

        # read in the common module source code
        moduleSource = self.mainMenu.installPath + "/data/module_source/situational_awareness/host/Get-ComputerDetails.ps1"
        if obfuscate:
            moduleSource = self.mainMenu.installPath + "/data/obfuscated_module_source/situational_awareness/host/Get-ComputerDetails.ps1"
            if not self.is_obfuscated():
                self.obfuscate(obfuscationCommand=obfuscationCommand)
        try:
            f = open(moduleSource, 'r')
        except:
            print helpers.color("[!] Could not read module source path at: " + str(moduleSource))
            return ""

        moduleCode = f.read()
        f.close()

        script = moduleCode + "\n\n"

        for option,values in self.options.iteritems():
            if option.lower() != "agent":
                if values['Value'] and values['Value'] != '':
                    if option == "4624":
                        script += "$SecurityLog = Get-EventLog -LogName Security; $Filtered4624 = Find-4624Logons $SecurityLog;"
                        script += 'Write-Output "Event ID 4624 (Logon):`n";'
                        script += "Write-Output $Filtered4624.Values | Out-String"
                        return script
                    if option == "4648":
                        script += "$SecurityLog = Get-EventLog -LogName Security; $Filtered4648 = Find-4648Logons $SecurityLog;"
                        script += 'Write-Output "Event ID 4648 (Explicit Credential Logon):`n";'
                        script += "Write-Output $Filtered4648.Values | Out-String"
                        return script
                    if option == "AppLocker":
                        script += "$AppLockerLogs = Find-AppLockerLogs;"
                        script += 'Write-Output "AppLocker Process Starts:`n";'
                        script += "Write-Output $AppLockerLogs.Values | Out-String"
                        return script
                    if option == "PSLogs":
                        script += "$PSLogs = Find-PSScriptsInPSAppLog;"
                        script += 'Write-Output "PowerShell Script Executions:`n";'
                        script += "Write-Output $PSLogs.Values | Out-String"
                        return script
                    if option == "SavedRDP":
                        script += "$RdpClientData = Find-RDPClientConnections;"
                        script += 'Write-Output "RDP Client Data:`n";'
                        script += "Write-Output $RdpClientData.Values | Out-String"
                        return script

        # if we get to this point, no switched were specified
        return script + "Get-ComputerDetails -ToString"

    def obfuscate(self, obfuscationCommand="", forceReobfuscation=False):
        if self.is_obfuscated() and not forceReobfuscation:
            return

        # read in the common module source code
        moduleSource = self.mainMenu.installPath + "/data/module_source/situational_awareness/host/Get-ComputerDetails.ps1"
        try:
            f = open(moduleSource, 'r')
        except:
            print helpers.color("[!] Could not read module source path at: " + str(moduleSource))
            return ""

        moduleCode = f.read()
        f.close()

        # obfuscate and write to obfuscated source path
        obfuscatedSource = self.mainMenu.installPath + "/data/obfuscated_module_source/situational_awareness/host/Get-ComputerDetails.ps1"
        obfuscatedCode = helpers.obfuscate(psScript=moduleCode, installPath=self.mainMenu.installPath, obfuscationCommand=obfuscationCommand)
        try:
            f = open(obfuscatedSource, 'w')
        except:
            print helpers.color("[!] Could not read obfuscated module source path at: " + str(obfuscatedSource))
            return ""
        f.write(obfuscatedCode)
        f.close()

    def is_obfuscated(self):
        obfuscatedSource = self.mainMenu.installPath + "/data/obfuscated_module_source/situational_awareness/host/Get-ComputerDetails.ps1"
        return os.path.isfile(obfuscatedSource)
