#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.
#


import time
from ..util.xinput import *
from ..util.enchelp import *
from ..app.event import *
from ..fmt import List



# --- DEFAULTS ---

DEF_WELCOME = """
BASE CONSOLE
 - Welcome to the interactive Console. Enter "help" to
   view options.
"""
DEF_PROMPT  = "trix.app: "
DEF_HELP    = {
	"exit" : "Close console.",
	"help" : "Display help messages."
}
DEF_CLOSING = "\nConsole Exiting. Bye!\n"
DEF_ERRORS = {"invalid-command": "Invalid Command"}


#
#
# CONSOLE CLASS
#
#
class Console(EncodingHelper):
	"""Base class for an interactive terminal-based user interface."""
	
	def __init__(self, config=None, **k):
		"""
		Pass config dict keys:
		 * welcome  : A string with any message/description/info
		 * prompt   : If set, replaces the default command prompt.
		 * help     : A dict containing keywords/help messages
		 * closing  : Message to print when exiting console
		 * errors   : A dict containing error-code:error-message strings
		
		COMMANDS:
		 * help : print help on the specified topic
		 * exit : exit the console (returning to previous activity)
		
		EXTEND CONSOLE:
		To extend the console class, add 'help' 
		"""
		
		config = config or {}
		try:
			config.update(**k)
		except AttributeError:
			jconf = trix.nvalue("app.jconf.jconf")
			config = jconf(config).obj
		
		EncodingHelper.__init__(self, config)
		
		# set member variables from config
		self.__welcome = config.get('welcome', DEF_WELCOME)
		self.__prompt  = config.get('prompt',  DEF_PROMPT)
		self.__help    = config.get('help',    DEF_HELP)
		self.__errors  = config.get('errors',  DEF_ERRORS)
		self.__closing = config.get('closing', DEF_CLOSING)
		
		# prompt active
		self.__active = False
	
	
	
	#
	# PROMPT
	#  - call this to start the console
	#
	def prompt(self):
		"""Call this method to start a console session."""
		
		try:
			self.banner(self.__welcome)
			self.__active = True
			while self.__active:
				try:
					cmd = xinput(self.__prompt)
					evt = TextEvent(cmd)
					self.handle_input(evt)
					if evt.argc and evt.argv[0]:
						print ('')
				
				except EOFError:
					self.__active = False
				
		except KeyboardInterrupt:
			pass
		
		# close banner
		self.banner(self.__closing)
	
	
	
	#
	# HANDLE INPUT
	#  - Override (and add to) these
	#
	def handle_input(self, e):
		"""Handle input event `e`."""
		
		if e.argc:
			
			# handle valid commands...
			if e.argvl[0] == 'help':
				self.handle_help (e)
			elif e.argvl[0] == 'exit':
				self.__active = False
			
			# if the first argument is blank...
			elif e.argv[0]:
				self.handle_error("invalid-command")
	
	
	
	#
	# HANDLERS...
	#  - Add a handler for each console command you want to implement.
	#  - Override these if you need to change behavior/output.
	#
	def handle_help(self, e):
		flist = List(sep=': ', titles=sorted(self.__help.keys()))
		print (flist.format(self.__help))
	
	
	def handle_error(self, err):
		if err in self.__errors:
			print ("Error! %s" % self.__errors[err])
	
	
	
	#
	# UTILITIES...
	#
	def display(self, message):
		lines = message.splitlines()
		for line in lines:
			print (line)
	
	
	def banner(self, message):
		lines = message.strip().splitlines()
		print ("*")
		for line in lines:
			print ("* %s" % line)
		print ("*")

	
	