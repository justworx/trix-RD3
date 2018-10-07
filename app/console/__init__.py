#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.
#

import time
from ..event import *
from ...util.xinput import *
from ...util.enchelp import *
from ...fmt import List, Lines


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
		 * title    : The console's title, "Console".
		 * about    : A string with any message/description/info
		 * prompt   : If set, replaces the default command prompt
		 * messages : A dict containing message key/value pairs
		 * help     : A dict containing keywords/help messages
		 * closing  : Message to print when exiting console
		 * plugins  : A dict containing app.plugin config
		
		COMMANDS:
		 * help : print help on the specified topic
		 * exit : exit the console (returning to previous activity)
		
		EXTEND CONSOLE:
		To extend the console class, add commands (and their 'help'). 
		"""
		
		#
		# If no config is given, use a default config path. Subclasses
		# must replace DefConf with their own path.
		#
		config = config or self.DefConf % self.DefLang
		try:
			# if config is a dict, update with kwargs it and continue
			config.update(**k)
			trix.display(config)
		except AttributeError:
			# ...otherwise, config must be the inner file path to a config
			# file such as 'app/config/en.conf'.
			confile = trix.innerfpath(config)
			jconf   = trix.ncreate("app.jconf.jconf", confile)
			config  = jconf.obj
		
		EncodingHelper.__init__(self, config)
		
		# debugging - store config
		self.__config = config
		
		#
		# set member variables from config
		#
		self.__title    = config.get('title', 'Console')
		self.__about    = config.get('about', 'About')
		self.__prompt   = config.get('prompt', '-->')
		self.__help     = config.get('help', {})
		self.__closing  = config.get('closing', 'Closing')
		self.__messages = config.get('messages', {})
		
		pconf = config.get('plugins', {})
		self.__plugins = {}
		
		perrors = {}
		for p in pconf:
			try:
				cpath = pconf[p].get("plugin")
				self.__plugins[p] = trix.create(
						cpath, p, self, pconf[p], **self.ek
					)
			except Exception as ex:
				perrors[p] = xdata(
						pluginname=p, ncreatepath=cpath, pluginconf=pconf
					)
		
		if perrors:
			raise Exception("plugin-load-errors", xdata(errors=perrors))
		
		# for display of text
		self.__lines = Lines()
		
		# prompt active
		self.__active = False
	
	
	
	@property
	def lines(self):
		return self.__lines	
	
	@property
	def title(self):
		return self.__title	
	
	@property
	def about(self):
		return self.__about	
	
	@property
	def help(self):
		return self.__help	
	
	@property
	def closing(self):
		return self.__closing	
	
	@property
	def plugins(self):
		return self.__plugins	
	
	
	@property
	def config(self):
		return self.__config
	
	
	#
	# CONSOLE - Start the console.
	#  
	def console(self):
		"""Call this method to start a console session."""
		
		try:
			self.banner()
			self.__active = True
			while self.__active:
				try:
					cmd = xinput(self.__prompt)
					evt = TextEvent(cmd)
					rsp = self.handle_input(evt)
					if evt.argc and evt.argv[0]:
						print ('')
				
				except EOFError:
					self.__active = False
				
		except KeyboardInterrupt:
			# print a blank line so exit message won't be on the input line
			print('')
		
		# close banner
		print("%s\n" % self.closing)
	
	
	
	#
	# HANDLE INPUT
	#  - Override (and add to) these
	#
	def handle_input(self, e):
		"""Handle input event `e`."""
		
		if e.argc:
			
			# check plugins first
			for p in self.__plugins:
				self.__plugins[p].handle(e)
				if e.reply:
					print ("%s\n" % str(e.reply))
			
			# handle valid commands...
			if e.argvl[0] == 'help':
				self.handle_help (e)
			elif e.argvl[0] == 'exit':
				self.__active = False
			
			# if the first argument is blank...
			elif e.argv[0]:
				self.handle_error("invalid-command")
	
	
	
	def _call_module(self, e):
		trix.display(e.dict)
		if e.argvl[0] == 'cq':
			if e.argc > 1:
				m = trix.nvalue('data.udata', "query")
				m(text=e.argv[1][0])
			
	
	
	#
	# HANDLERS...
	#  - Add a handler for each console command you want to implement.
	#  - Override these if you need to change behavior/output.
	#
	def handle_help(self, e):
		flist = List(sep=': ', titles=sorted(self.__help.keys()))
		print (flist.format(self.__help))
	
	
	def handle_error(self, err):
		if err in self.__messages:
			print ("Error! %s" % self.__messages[err])
	
	
	
	#
	# UTILITIES...
	#
	def display(self, message):
		lines = message.splitlines()
		for line in lines:
			print (line)
	
	
	def banner(self, *a):
		self.lines.output(self.title, ff='title')
		self.lines.output(self.about, ff='about')
		print("#")
	
	