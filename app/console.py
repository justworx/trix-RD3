#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.
#

from getpass import *
from ..fmt import List, Lines
from ..util.xinput import *
from ..util.enchelp import *
from ..util.linedbg import *
from ..util.wrap import *

from .jconfig import *
from .event.cli import *



class ConsoleError(Exception):
	DEBUG = False
	def __init__(self, message, xdata):
		self.args = [message]
		self.more = xdata



# ------------------------------------------------------------------
#
# CONSOLE CLASS
#
# ------------------------------------------------------------------
class Console(EncodingHelper):
	"""Base class for an interactive terminal-based user interface."""
	
	dv = {} # Wrap debugging values
	
	Debug = True
	DefLang = 'en'
	DefConf = "app/config/console/%s.conf"
	
	#
	# ---- INIT -----
	#
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
		# If no config is given, use a default config path. Subclasses
		# must replace DefConf with their own path.
		#
		config = config or self.DefConf % self.DefLang
		try:
			# if config is a dict, update with kwargs it and continue
			config.update(**k)
		except AttributeError:
			# otherwise, it's some kind of file path
			if "nconfig" in k:
				config = trix.nconfig(config['nconfig'], **k)
			elif "config" in k:
				config = trix.config(config['config'], **k)
			else:
				config = trix.nconfig(config, **k)
		
		# store config
		self.__config = config
		
		# init superclass
		EncodingHelper.__init__(self, config)
		
		# Set member variables from config
		self.__title    = config.get('title'   , 'Console')
		self.__about    = config.get('about'   , 'Hello.' )
		self.__closing  = config.get('closing' , 'Closing')
		self.__help     = config.get('help'    , {}       )
		self.__messages = config.get('messages', {}       )
		
		# WRAPPERS - For "sub-prompts".
		self.__wrappers = config.get('wrappers', {})
		
		#
		# PLUGINS
		#
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
		try:
			return self.__ident_prefix
		except:
			id_mod = self.__module__.split('.')[-2]
			self.__ident_prefix = "%s@%s" % (getuser(), id_mod)
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
	
	#
	# WRAPPER
	#
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
		return Wrapper(wconf)
	
	
	# CONSOLE - Start the console.
	def console(self):
		"""Call this method to start a console session."""
		
		try:
			self.banner()
			self.__active = True
			while self.__active:
				evt=None
				try:
					# get input, create Event
					line = xinput(self.prompt).strip()
					
					# make sure there's some text to parse
					if line:
						# get and handle event
						evt = self.create_event(line)
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
				
		except KeyboardInterrupt:
			print('')
		
		except BaseException:
			linedbg().dbg(self, "Fatal Exception. %s\n" % self.closing)
			raise
		
		# close banner
		print("%s\n" % self.closing)
	
	
	def create_event(self, commandLineText):
		"""Returns a TextEvent."""
		return LineEvent(commandLineText)
	
	
	#
	# UTILITIES...
	#
	
	# DISPLAY
	def display(self, message):
		"""Display text formatted to fit within a preconfigured width."""
		lines = message.splitlines()
		for line in lines:
			print (line)
	
	
	# BANNER
	def banner(self, *a):
		"""Display text as a title/about banner combo."""
		self.lines.output(self.title, ff='title')
		self.lines.output(self.about, ff='about')
		print("#")
	
	
	
	#
	# HANDLERS...
	#  - Help, Errors, and Input handlers.
	#  - Subclasses may override these to change behavior/output.
	#
	
	# HANDLE HELP
	def handle_help(self, e):
		flist = List(sep=': ', titles=sorted(self.__help.keys()))
		print (flist.format(self.__help))
	
	
	# HANDLE ERROR
	def handle_error(self, err, *a):
		"""Print an error message and display arguments."""
		if err in self.__messages:
			print ("Error! %s" % self.__messages[err])
		else:
			print ("Unknown Error!")
		if a:
			trix.display({"args":a})
		
	
	
	# HANDLE INPUT
	def handle_input(self, e):
		"""Handle input event `e`."""
		
		if e.argc and e.argv[0]:
			
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
				if self.Debug:
					raise Exception(
							xdata(error="unknown-command", args=e.argv)
						)
				else:
					self.handle_error("unknown-command", *e.argv)




# ------------------------------------------------------------------
#
# WRAPPER CLASS
#
# ------------------------------------------------------------------
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
	
	#
	# INIT WRAPPER
	#
	def __init__(self, config, *a, **k):
		
		conf = None
		try:
			# Load this wrapper's config file
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
			self.__wrap = Wrap(self.__wrapped)
			
			
			
			# INIT CONSTRUCTOR
			Console.__init__(self, conf, **k)
			
			# ADD A DEBUG VARIABLE
			Console.dv["Wrapper"] = self           # DEBUG VAR
			Console.dv["wrapped"] = self.__wrapped # DEBUG VAR
			Console.dv["wrap"] = self.__wrap       # DEBUG VAR
			Console.dv["obj"] = self.__obj         # DEBUG VAR
		
		
		# ...but this one shows way to much stuff...
		except Exception as ex:
			try:
				o = str(self.__wrapped.obj)
			except:
				o = None
			raise ConsoleError(str(ex), xdata(a=a, o=o))
	
	
	
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
	
	
	def handle_input(self, e):
		
		if e.argc and e.argv[0] not in ['', None]:
			r = self.wrap(*e.argv)
			if r:
				trix.display(r)
	
	
	def resultformat(self, r):
		#print (" - r in:", r)
		if r:
			if isinstance(r, (str,int,float,bool)):
				return str(r)
			else:
				try: # is it dict-like?
					return trix.formatter(f='JDisplay').format(dict(r))
				except Exception as ex:
					pass
				
				try: # list-like?
					return trix.formatter(f='JSON').format(list(r))
				except Exception as ex:
					pass
				
				try: # if all else fails, convert to string
					return str(r)
				except Exception as ex:
					pass
		#print (" - r out:", r)
		return r
