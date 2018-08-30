#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.
#


# import
from . import *
from .irc_event import *
from ..connect import *
from ...util.runner import *


# connect class
class IRCConnect(Connect, Runner):
	"""
	IRC Connection class.
	
	IRCConnect creates and maintains one connection to one irc network
	server. The functionality is limited to connecting and replying to
	PING lines from the server and management of plugins. All other 
	activity is handled by plugins themselves.
	"""
	
	def __init__(self, config=None, **k):
		
		# read config
		config = config or {}
		config.setdefault('encoding', DEF_ENCODE)
		config.update(k)
		
		# store config for plugin load/unload
		self.pconfig = config.get('plugins', {})
		
		# host-masks in this list fully control the bot
		self.owner = config.get('owner', [])
		
		# display/debug
		self.show = None
		self.debug = k.get('debug', IRC_DEBUG)
		
		# if debugging at all, display config in terminal
		if self.debug > 0:
			trix.display(config)
		
		# config
		host = config['host']
		port = config['port']
		nick = self.nick = config['nick']
		
		# user/ident (optional; defaults to: nick)
		user = self.user = config.get('user', self.nick).lower()
		ident = self.ident = config.get('ident', self.nick)
		
		#
		# plugin support - start initial plugins
		#
		self.plugins = {} # store existing plugins here
		
		# check for plugins that need to be created from config
		if 'plugins' in config:
			# INIT PLUGINS
			#  - loop through each name in the pconf dict
			for pname in self.pconfig:
				pi = self.__plugin_load(pname)
				if pi:
					self.plugins[pname] = pi
		
		#
		# initialize superclasses
		#  - Runner repeatedly calls the event loop `io`
		#  - Connect opens a connection to the server immediately
		#
		Runner.__init__(self, config, **k)
		Connect.__init__(self, (host, port))
		
		#
		# connection
		#
		user_line = "USER "+nick+' '+user+' '+host+' :'+ident
		nick_line = "NICK "+nick
		
		self.writeline(user_line)
		self.writeline(nick_line)
		
		if self.debug:
			irc.debug(
				"#\n# CONNECTING:",
				"#       HOST: %s" % host,
				"#       USER: %s" % user_line,
				"#       NICK: %s" % nick_line
			)
		
		# runtime values
		self.pi_update = time.time()
		self.pi_interval = config.get('pi_interval', PLUG_UPDT)
		
		#
		# start running so that io() gets called frequently
		#
		if k.get('run'):
			self.show = k.get('show', self.debug)
			if self.debug:
				irc.debug ("# Running %s" % (nick))
			Runner.run(self)
		elif k.get('start', True):
			if self.debug:
				print ("# Starting %s!%s@%s" % (nick, user, host))
			self.show = k.get('show', True)
			Runner.start(self)
		
		# plugin management - runtime add/remove
		self.pm_add = []
		self.pm_rmv = []
	
	
	#
	# RUNTIME - ADD/REMOVE OF PLUGINS 
	#
	def plugin_add(self, pname):
		"""Add `pname` to the plugin add-list."""
		if pname not in self.plugins:
			self.pm_add.append(pname)
	
	
	def plugin_remove(self, pname):
		"""Add `pname` to the plugin remove list."""
		if pname in self.plugins:
			self.pm_rmv.append(pname)		
	
	
	def plugin_reload(self, pname):
		"""
		Reload `pname` and add it to the plugin add and remove lists.
		"""
		if pname in self.plugins:
			
			# find and reload the plugin
			ppath = self.pconfig[pname]['plugin']   # plugin class path
			pmodp = ".".join(ppath.split('.')[:-1]) # plugin module path
			pmod = trix.value(pmodp)                # plugin module object
			reload(pmod)
			
			# set the current plugin to be removed, then recreated (as the
			# newly reloaded version) on next call to self.io();
			# NOTE: trix defines `reload()` to work in python3.
			self.pm_rmv.append(pname)
			self.pm_add.append(pname)
	
	
	#
	# IO LOOP - ADD/REMOVE OF PLUGINS 
	#
	def __plugin_load(self, pname):
		"""Load plugin `pname` immediately."""
		if not (pname in self.plugins):
			pi = self.__plugin_create(pname)
			if not pi:
				raise Exception ("plugin-create-fail", xdata(pname=pname))
			self.plugins[pname] = pi
			return pi
	
	
	def __plugin_unload(self, pname):
		"""Unload (delete) plugin `pname` immediately."""
		if (pname in self.plugins):
			del(self.plugins[pname])
	
	
	def __plugin_create(self, pname):
		"""
		Create and return a plugin object given plugin name `pname`.
		"""
		ppath = self.pconfig[pname]['plugin'] # path for `trix.create`
		pconf = self.pconfig[pname]
		pi = trix.create(ppath, pconf, self)
		if not pi:
			raise Exception ("plugin-create-fail", xdata(pname=pname,
					ppath=ppath, pconf=pconf
				))
		
		return pi
	
	
	
	# ----------------------------------------------------------------
	# IO
	# ----------------------------------------------------------------
	def io(self):
		
		# read all received text since last io;
		# might be multiple lines (or empty).
		try:
			intext = self.read()
		except BaseException as e:
			intext = ''
			irc.debug(
				"# READ ERROR (WARNING)",
				"# -type: %s" % type(e),
				"# -err : %s" % str(e),
				"# -time: %s" % str(time.time())
			)
		
		#
		# INPUT - - - - - - - - - - - - - - - - - - - - - - - - - - - -
		#  - Handle received text.
		#
		if intext:
			
			try:
				# split them...
				inlines = intext.splitlines()
				
				# ...and handle each line.
				for line in inlines:
					
					if line[0:4] == 'PING':
						if self.debug > 1:
							print ("# ping")
						RESP = line.split()[1] # handle PING
						self.writeline('PONG ' + RESP)
						if self.debug > 1:
							print ("# pong")
					else:
						self.on_message(line)  # handle everything besides PINGs
			
			except Exception as ex:
				print ("ERROR: %s: %s" % (str(type(ex)), str(ex)))
				print (traceback.extract_tb(sys.exc_info()[2]))

		
		#
		# PLUGINS	- - - - - - - - - - - - - - - - - - - - - - - - - - -
		#  - every now-n-then, call the plugins' `update` method
		#
		if time.time() > (self.pi_update + self.pi_interval):
			
			# update to wait another `interval` seconds.
			self.pi_update = time.time()
			
			#print ("# plugins update; " + str(time.time()))
			
			pfailed = []
			for pname in self.plugins:
				try:
					self.plugins[pname].update()
				except Exception as ex:
					if self.debug:
						print("#")
						print("# Plugin Update Failed. Removing: %s" % pname)
						print("# Error: %s" % str(ex))
						print("#")
					pfailed.append(pname)
			
			# remove plugins that failed to load
			if pfailed:
				for pname in pfailed:
					del(self.plugins[pname])
		
		#
		# MANAGE PLUGINS - - - - - - - - - - - - - - - - - - - - - - - -
		#  - add, remove, reload plugins
		#  - this must be handled outside the event loop so that 
		#    changes to the self.plugins dict won't happen during 
		#    iteration.
		#
		
		# do removes first (in case a plugin has been reloaded)
		if self.pm_rmv:
			try:
				for pname in self.pm_rmv:
					if (pname in self.pm_rmv) and (pname in self.plugins):
						del(self.plugins[pname])
			except Exception as ex:
				print ("Plugin Rmv Fail! %s: %s" % (str(type(ex), str(ex))))
			finally:
				self.pm_rmv = []
		
		# do adds afterward, so reloaded plugins can be re-added
		if self.pm_add:
			try:
				for pname in self.pm_add:
					if (pname in self.pm_add):
						self.plugins[pname] = self.__plugin_load(pname)
			except Exception as ex:
				print ("Plugin Add Fail! %s: %s" % (str(type(ex)), str(ex)))
			finally:
				self.pm_add = []
		
	
	
	# ----------------------------------------------------------------
	# ON MESSAGE
	# ----------------------------------------------------------------
	def on_message(self, line):
		
		e = IRCEvent(line)
		
		# showing text
		if self.show or self.debug:
			print (e.line)
		
		# debugging 
		if self.debug > 2:
			trix.display(e.dict)
		
		# HANDLE! Let each plugin handle each event (but not PINGs)
		for pname in self.plugins:
			try:
				p = self.plugins[pname]
				p.handle(e)
			except BaseException as ex:
				p.reply(e, "Error: %s %s" % (str(type(ex)), str(ex)))
	
	
	
	# ----------------------------------------------------------------
	# OTHER UTIL
	# ----------------------------------------------------------------
	
	def status(self):
		s = {}
		s['ircconf'] = self.config
		s['runner'] = Runner.status(self)
		return s
	
	def ping(self, x=None):
		x = x or time.time()
		self.writeline("PING :%s" % x)




