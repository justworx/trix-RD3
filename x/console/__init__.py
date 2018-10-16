#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.
#

from getpass import *
from ...util.xinput import *
from ...util.enchelp import *
from ...util.linedbg import *
from ...util.wrap import *
from ...fmt import List, Lines

# the following will need to be changed when this moves to trix.app
from trix.app.jconfig import *
from trix.app.event import *


#
#
# CONSOLE CLASS
#
#
class Console(EncodingHelper):
	"""Base class for an interactive terminal-based user interface."""
	
	dv = {}
	
	DefLang = 'en'
	DefConf = "x/console/config/%s.conf"  # REM: Change x to app!
	
	def __init__(self, config=None, **k):
		"""
		Pass config dict keys:
		 * title    : The console's title, "Console".
		 * about    : A string with any message/description/info
		 * messages : A dict containing message key/value pairs
		 * help     : A dict containing keywords/help messages
		 * closing  : Message to print when exiting console
		 * plugins  : A dict containing app.plugin config
		
		COMMANDS:
		 * help : print help on the specified topic
		 * exit : exit the console (returning to previous activity)
		"""
		#
		# ident
		#
		id_mod = self.__module__.split('.')[-2]
		self.__ident_prefix = "%s@%s" % (getuser(), id_mod)
		
		#
		# If no config is given, use a default config path. Subclasses
		# must replace DefConf with their own path.
		#
		config = config or self.DefConf % self.DefLang
		try:
			# if config is a dict, update with kwargs it and continue
			config.update(**k)
		except AttributeError:
			#
			# otherwise config is given by the `config` argument or by 
			# a 'config' or 'nconfig' kwargs (which take precedence over 
			# the `config` argument).
			#
			
			# at this point, config is a file path
			if "nconfig" in k:
				config = trix.nconfig(config['nconfig'], **k)
			elif "config" in k:
				config = trix.config(config['config'], **k)
			else:
				config = trix.nconfig(config, **k)
			
		# -- now config is a dict --
		
		EncodingHelper.__init__(self, config)
		
		
		# debugging - store config
		self.__config = config

		
		#
		# set member variables from config
		#
		self.__title    = config.get('title'   , 'Console')
		self.__about    = config.get('about'   , 'Hello.' )
		self.__closing  = config.get('closing' , 'Closing')
		self.__help     = config.get('help'    , {}       )
		self.__messages = config.get('messages', {}       )
		
		# exerimental - probably going away
		self.__objects = {}
		
		#
		# alternate experiment
		#  - Console can open one "subconsole" - Typically a Wrap object
		#    that calls some object's methods as directed by a line of
		#    input.
		#
		self.__wrappers = config.get('wrappers', {})
		self.__object = None
		
		
		#
		# PLUGINS
		#
		
		# plugin config
		pconf = config.get('plugins', {})
		self.__plugins = {}
		
		# plugin load
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
		
		# LINES - for display of text
		self.__lines = Lines()
		
		# ACTIVE - Is the prompt active? If not, exit this console.
		self.__active = False
	
	
	
	@property
	def ident(self):
		"""
		An informative (and hopefully unique) identity string that's
		used as the prompt for a given console.
		
		The returned string is "{username}@{modulename}/{Identity}",
		where the suggested Identity is a classname, or a more
		descriptive term, if appropriate. These values are generated
		in the constructor, but subclasses can easily alter the
		id_suffix property to return a more suitable Identity if
		necessary.
		"""
		return "%s/%s" % (self.id_prefix, self.id_suffix)
	
	@property
	def id_prefix(self):
		"""
		Returns a format string that merges the system username, the
		module name, and a distishing, meaningful name of any kind -
		typically a class name, but potentially some other name 
		representative of the function the prompt intends to perform.
		"""
		return self.__ident_prefix
	
	@property
	def id_suffix(self):
		"""
		Ident line suffix is the class name, is the last element in the
		construction of the prompt string.
		
		Wrappers should override this property, setting it to the wrapped
		class's name. Subclasses should use the class name of the object
		they're "prompting" for, unless a different name seems more 
		appropriate or descriptive of the its function.
		"""
		return type(self).__name__
	
	@property
	def prompt(self):
		"""
		The command-line input prompt for this object.
		"""
		return "%s: " % self.ident
	
	@property
	def lines(self):
		"""
		Convenience. A fmt.Lines object used to format lines of text
		to within a preconfigured width.
		"""
		return self.__lines	
	
	@property
	def title(self):
		"""This console's title string, as read from config."""
		return self.__title	
	
	@property
	def about(self):
		"""This console's about section text, as read from config."""
		return self.__about	
	
	@property
	def help(self):
		"""
		A dict containing this console's help messages, as read from 
		config.
		"""
		return self.__help	
	
	@property
	def closing(self):
		"""An 'exit' message string, as read from config."""
		return self.__closing	
	
	@property
	def plugins(self):
		"""A dict containing this console's plugins."""
		return self.__plugins	
	
	@property
	def config(self):
		"""The entire config dict, for reference."""
		return self.__config
	
	@property
	def wrappers(self):
		"""A dict of wrappers available for use by this console."""
		return self.__wrappers
	
	
	def wrapper(self, wrapperid, *a):
		"""
		Return the wrapper from self.wrappers whose key matches
		`wrapperid`.
		"""
		# get the basic config
		wconf = self.__wrappers[wrapperid]
		if 'nconfig' in wconf:
			wconf = Wrapper(trix.nconfig(wconf['nconfig']))
		elif 'config' in wconf:
			wconf = Wrapper(trix.config(wconf['config']))
		else:
			raise ValueError("Config Requires config or nconfig path.",
					xdata(config=wconf)
				)
		
		#trix.display(wconf)
		
		return Wrapper(wconf)
		
		# load the wrapper config
		#wconfig = 
		
		"""
		#
		# CREATE
		#  - Use the creation method specified in the config file.
		#
		if 'ncreate' in wconf:
			obj = trix.ncreate(wconf['ncreate'], *a)
		elif 'create' in wconf:
			obj = trix.create(wconf['create'], *a)
		
		wrap = trix.ncreate("x.wrap.Wrap", obj)
		self.w = wrap
		self.o = obj
		"""
	
	#
	# CONSOLE - Start the console.
	#  
	def console(self):
		"""Call this method to start a console session."""
		
		try:
			self.banner()
			self.__active = True
			while self.__active:
				cmd=evt=None
				try:
					evt = TextEvent(xinput(self.prompt))
					self.handle_input(evt)
				
				except EOFError:
					# Ctrl-C exits this prompt
					self.__active = False
				
				except Exception as ex:
					#
					# Handle other exceptions by displaying them with linedbg
					#
					print('') # get off the "input" line
					event_dict = evt.dict if evt else None
					linedbg().dbg(self, args=ex.args, edict=event_dict)
					#linedbg().dbg(self) #, *ex.args)
				
		except KeyboardInterrupt:
			print('')
		
		except BaseException:
			linedbg().dbg(self, "Fatal Exception. %s\n" % self.closing)
			raise
		
		# close banner
		print("%s\n" % self.closing)
	
	
	
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
	
	
	
	#
	# HANDLERS...
	#  - Add a handler for each console command you want to implement.
	#  - Override these if you need to change behavior/output.
	#
	
	# HANDLE HELP
	def handle_help(self, e):
		flist = List(sep=': ', titles=sorted(self.__help.keys()))
		print (flist.format(self.__help))
	
	
	# HANDLE ERROR
	def handle_error(self, err, *a):
		if err in self.__messages:
			print ("Error! %s" % self.__messages[err])
		else:
			print ("Unknown Error!")
		if a:
			trix.display({"args":a})
	
	
	# HANDLE INPUT
	def handle_input(self, e):
		"""Handle input event `e`."""
		
		if e.argc:
			
			# check plugins first
			for p in self.__plugins:
				self.__plugins[p].handle(e)
				if e.reply:
					self.lines.output ("%s\n" % str(e.reply))
					return
			
			# handle valid commands...
			if e.argvl[0] == 'help':
				self.handle_help(e)
			elif e.argvl[0] == 'plugins':
				self.lines.output(" ".join(self.plugins.keys()))
			elif e.argvl[0] == 'wrappers':
				self.lines.output(" ".join(self.wrappers.keys()))
			elif e.argvl[0] == 'exit':
				self.__active = False
			
			# create and run a Wrapper object's console
			elif e.argv[0] in self.wrappers:
				#
				# Generate a new Wrapper each time; this wrapper object 
				# holds control until its `console()` method is exited.
				#
				
				# first, get the config out of this command line
				wrapperid = e.argv[0]
				wrap_conf = self.wrappers[e.argv[0]]
				wrap_args = e.argv[1:]
				
				# the entire config must be passed
				w = Wrapper(wrap_conf, *wrap_args)
				w.console()
		
			#
			# CHECK FIRST ARG!
			#  - There's always at least one argument, even if it's ''.
			#    In this case, nothing (or only white space) was entered,
			#    so just hit the next line. Otherwise, it's an unknown 
			#    command, so complain.
			#
			elif e.argvl[0]:
				self.handle_error("unknown-command", *e.argv)
	




class Wrapper(Console):
	"""
	A Wrapper is a Console that holds a "wrapped" python object and 
	responds to console commands by calling methods of that object.
	
	Console creates a Wrapper whenever the first word entered in on
	line of text matches a key in its `self.wrappers` dict. The key's 
	value (self.wrappers[key]) is the Wrapper's config.
	
	Each wrapper config should contain the following config dict keys: 
	 * create  - the full pythonic path to the definition of the class
	             to be wrapped ('create')
	             ...OR...
	   ncreate - the inner path to the definition of the class to be 
	             wrapped ('ncreate').
	 * args    - a list of args for the object's constructor
	 * kwargs  - a dict of kwargs for the object's constructor
	
	When the Wrapper object's `console()` method is called, commands
	entered there are parsed and used as follows:
	 * The first argument (after the command) represents the name
	   of an attribute in the wrapped object;
	 * Remaining args are passed to that method and the event's reply
	   holds the return value.
	    - NOTE: these args are different from the constructor args;
	            they're generated from the prompt line and are received
	            by `Wrapper.handle_input()`.
	   
	"""
	
	def __init__(self, config, *a, **k):
		
		conf = None
		try:
			#
			# Load this wrapper's config file
			#
			if 'config' in config:
				conf = trix.config(config['config'])
			else:
				conf = trix.nconfig(config['nconfig'])
			
			# get the wrapped object's config
			if 'ncreate' in conf:
				self.__wrapped = trix.ncreate(conf['ncreate'], *a)
			else:
				self.__wrapped = trix.create(conf['create'], *a)
			
			self.__obj = self.__wrapped.obj
				
			# create the wrapped object, passing args received on the
			# command line.
			self.__wrap = Wrap(self.__obj)
			
			# INIT CONSTRUCTOR
			Console.__init__(self, conf, **k)
			
			# ADD A DEBUG VARIABLE
			Console.dv["Wrapper"] = self           # DEBUG VAR
			Console.dv["wrapped"] = self.__wrapped # DEBUG VAR
			Console.dv["wrap"] = self.__wrap       # DEBUG VAR
			Console.dv["obj"] = self.__obj         # DEBUG VAR
			
		except Exception as ex:
			raise type(ex)(xdata(a=a, conf=conf))
	
	
	
	@property
	def id_suffix(self):
		return type(self.__wrapped).__name__
	
	
	@property
	def obj(self):
		return self.__wrap.obj
	
	@property
	def wrap(self):
		return self.__wrap
	
	@property
	def wrapped(self):
		return self.__wrapped
	
	
	def resultformat(self, r):
		if r:
			if isinstance(r, (str,int,float,bool)):
				return str(r)
			else:
				try: # is it dict-like?
					return trix.formatter(f='JDisplay').format(dict(r))
				except Exception as ex:
					pass
				
				try: # list-like?
					return trix.formatter(f='JDisplay').format(list(r))
				except Exception as ex:
					pass
				
				try: # list-like?
					return str(r)
				except Exception as ex:
					pass
		return r
	
	
	
	def handle_input(self, e):
		
		cmd = e.argv[0]
		args = e.argv[1:]
		wrap = self.__wrap
		
		trix.display(['handle_input', cmd, args])
		
		result = wrap(cmd, *args)
		e.reply = self.resultformat(result)
		print( e.reply )
