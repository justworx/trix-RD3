#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.
#

import time
from ..event import *
from ...util.xinput import *
from ...util.enchelp import *
from ...fmt import List


#
#
# CONSOLE CLASS
#
#
class Console(EncodingHelper):
	"""Base class for an interactive terminal-based user interface."""
	
	DefLang = 'en'
	DefConf = "app/console/config/%s.conf"
	
	def __init__(self, config=None, **k):
		"""
		Pass config dict keys:
		 * welcome  : A string with any message/description/info
		 * prompt   : If set, replaces the default command prompt.
		 * help     : A dict containing keywords/help messages
		 * closing  : Message to print when exiting console
		 * c_errors : A dict containing error-code:error-message strings
		
		COMMANDS:
		 * help : print help on the specified topic
		 * exit : exit the console (returning to previous activity)
		
		EXTEND CONSOLE:
		To extend the console class, add 'help' 
		"""
		
		# because this is the default Console, it can have a default
		# config path
		config = config or self.DefConf % self.DefLang
		try:
			# if config is a dict, update with kwargs it and continue
			config.update(**k)
		except AttributeError:
			# otherwise, config must be the inner file path to a config
			# file such as 'app/config/en.conf'.
			confile = trix.innerfpath(config)
			jconf   = trix.ncreate("app.jconf.jconf", confile)
			config  = jconf.obj
		
		EncodingHelper.__init__(self, config)
		
		# set member variables from config
		self.__welcome = config.get('welcome', '')
		self.__prompt  = config.get('prompt',  '')
		self.__help    = config.get('help',    '')
		self.__closing = config.get('closing', '')

		self.__cerrors = config.get('cerrors',  '')
		
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
		if err in self.__cerrors:
			print ("Error! %s" % self.__cerrors[err])
	
	
	
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

	
	