#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.
#


# import
from . import *
from .plugin import *    # <-- reload IRCPlugin before other plugins
from .irc_event import *
from ..connect import *


# connect class
class IRCConnect(Connect):
	"""
	IRC Connection class.
	
	IRCConnect creates and maintains one connection to one irc network
	server. The functionality is limited to connecting and replying to
	PING lines from the server and management of plugins. All other 
	activity is handled by plugins themselves.
	"""
	
	cache = "~/.cache/trix"
	
	def __init__(self, config=None, **k):
			
		# read config
		config = config or {}
		config.setdefault('encoding', DEF_ENCODE)
		config.setdefault('errors', "replace")
		config.update(k)
		
		# client sets the connid, the key from the config dict, which
		# is also the bot's id.
		self.__botid = config.get('connid')
		
		# store config for plugin load/unload
		self.pconfig = config.get('plugins', {})
		
		# host-masks in this list fully control the bot
		self.owner = config.get('owner', [])
		
		# display/debug
		self.show = None
		self.debug = k.get('debug', IRC_DEBUG)
		
		# if debugging at all, display config in terminal
		#if self.debug > 0:
		#	trix.display(config)
		
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
		
		# global information storage - set by plugins, used by all.
		self.ginfo = {}
		
		# This is replaced by ginfo['info']['pair']['CHANTYPES'] if
		# and when the 005 command is parsed.
		self.chantypes = '#'
		
		#
		# INIT PLUGINS
		# Check for plugins that need to be created from config
		#
		if 'plugins' in config:
			# loop through each name in the pconf dict
			for pname in self.pconfig:
				self.ginfo[pname] = {}
				pi = self.__plugin_load(pname)
				if pi:
					self.plugins[pname] = pi
		
		#
		# initialize superclass
		#  - Connect opens a connection to the server immediately
		#
		Connect.__init__(self, (host, port),
				encoding = config.get('encoding', 'utf_8'),
				errors   = config.get('errors', 'replace')
			)
		
		
		#
		# connection
		#
		user_line = "USER "+nick+' '+user+' '+host+' :'+ident
		nick_line = "NICK "+nick
		
		self.writeline(user_line)
		self.writeline(nick_line)
		
		logplugin = self.plugins.get('irclog')
		LOGS = logplugin.logfile or "None"
		
		if self.debug:
			irc.debug(
				"#\n# CONNECTING:",
				"#       HOST: %s" % host,
				"#       USER: %s" % user_line,
				"#       NICK: %s" % nick_line,
				"#       LOGS: %s" % LOGS
			)
		
		# runtime values
		self.pi_update = time.time()
		self.pi_interval = config.get('pi_interval', PLUG_UPDT)
		
		# plugin management - runtime add/remove
		self.pm_add = []
		self.pm_rmv = []
	
	
	@property
	def botid(self):
		return self.__botid
	
	
	
	#
	# RUNTIME - ADD/REMOVE OF PLUGINS 
	#
	
	# ------ lists that control what will happen next .io() ------
	
	def plugin_add(self, pname):
		"""Add `pname` to the plugin add-list."""
		if pname not in self.plugins:
			self.pm_add.append(pname)
	
	
	def plugin_remove(self, pname):
		"""Add `pname` to the plugin remove list."""
		if pname in self.plugins:
			self.pm_rmv.append(pname)		
	
	
	# ------ stuff that happens during io ------
	
	def plugin_reload(self, pname):
		"""
		Reload `pname` and add it to the plugin add and remove lists.
		"""
		try:
			reload(plugin)
			
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
				
				irc.debug("plugin_reload",
						pm_rmv = self.pm_rmv,
						pm_add = self.pm_add
					)
		
		except Exception as ex:
			irc.debug (
				"plugin_reload", "DEBUG: reload fail", pname
			)
			raise

	
	#
	# IO LOOP - ADD/REMOVE OF PLUGINS 
	#
	def __plugin_load(self, pname):
		"""Load plugin `pname` immediately."""
		try:
			if not (pname in self.plugins):
				pi = self.__plugin_create(pname)
				if not pi:
					raise Exception ("plugin-create-fail", xdata(pname=pname))
				self.plugins[pname] = pi
				return pi
		except:
			irc.debug (
				"__plugin_load", "load plugin fail!", pname
			)
			raise
			
	
	def __plugin_unload(self, pname):
		"""Unload (delete) plugin `pname` immediately."""
		try:
			if (pname in self.plugins):
				del(self.plugins[pname])
		except:
			irc.debug ("__plugin_unload", pname)
			raise
	
	
	def __plugin_create(self, pname):
		"""
		Create and return a plugin object given plugin name `pname`.
		"""
		ppath = self.pconfig[pname]['plugin'] # path for `trix.create`
		pconf = self.pconfig[pname]
		pi = trix.create(ppath, pname, self, pconf)
		if not pi:
			raise Exception ("plugin-create-fail", xdata(
					pname=pname, ppath=ppath, pconf=pconf
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
			self.__handle_received_text(intext)

		#
		# PLUGINS	- - - - - - - - - - - - - - - - - - - - - - - - - - -
		#  - every now-n-then, call the plugins' `update` method
		#
		if time.time() > (self.pi_update + self.pi_interval):
			self.__handle_plugin_update()
		
		#
		# MANAGE PLUGINS - - - - - - - - - - - - - - - - - - - - - - - -
		#  - add, remove, reload plugins
		#  - do removes first (in case a plugin has been reloaded)
		#  - do adds afterward, so reloaded plugins can be re-added
		#
		if self.pm_rmv:
			self.__handle_plugin_rmv()
		
		if self.pm_add:
			self.__handle_plugin_add()
	
	
	#
	# HANDLE RECEIVED LINES
	#
	def __handle_received_text(self, intext):
		
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
					if self.debug > 7:
						print ("# pong")
				else:
					self.on_message(line)  # handle everything besides PINGs
		
		except Exception as ex:
			irc.debug (str(type(ex)), str(ex))
	
	
	#
	# HANDLE PLUGIN UPDATE
	#
	def __handle_plugin_update(self):
		
		# update to wait another `interval` seconds.
		self.pi_update = time.time()
		
		pfailed = []
		for pname in self.plugins:
			try:
				self.plugins[pname].update()
			except Exception as ex:
				if self.debug:
					irc.debug(
						"Plugin Update Failed", "Removing: %s" % pname,
						"Error: %s" % str(ex)
					)
				pfailed.append(pname)
		
		# remove plugins that failed to load
		if pfailed:
			for pname in pfailed:
				del(self.plugins[pname])
		
	
	
	#
	# HANDLE PLUGIN REMOVE
	#
	def __handle_plugin_rmv(self):
		try:
			for pname in self.pm_rmv:
				if (pname in self.pm_rmv) and (pname in self.plugins):
					del(self.plugins[pname])
					irc.debug(
						"irc_connect.__handle_plugin_rmv", "removed plugin", 
							pname
						)
		except Exception as ex:
			irc.debug ("irc_connect.__handle_plugin_rmv", 
					str(type(ex), str(ex))
				)
		finally:
			self.pm_rmv = []
	
	
	
	#
	# HANDLE PLUGIN ADD
	#
	def __handle_plugin_add(self):
		pname = None
		try:
			for pname in self.pm_add:
				if (pname in self.pm_add):
					self.plugins[pname] = self.__plugin_load(pname)
		except Exception as ex:
			irc.debug ("irc_connect.__handle_plugin_add", 
					pname=pname, addlist=self.pm_add
				)
		finally:
			self.pm_add = []
			
	
	
	
	
	# ----------------------------------------------------------------
	#
	# ON MESSAGE
	#
	# ----------------------------------------------------------------
	def on_message(self, line):
		
		e = IRCEvent(line)
		
		# showing text
		if self.show or self.debug:
			print (e.line)
		
		# HANDLE! Let each plugin handle each event (but not PINGs)
		for pname in self.plugins:
			try:
				p = self.plugins[pname]
				p.handle(e)
			except BaseException as ex:
				msg = "Error: %s %s" % (str(type(ex)), str(ex))
				irc.debug(msg)
				p.reply(e, msg)
	
	
	
	# ----------------------------------------------------------------
	#
	# OTHER UTIL
	#
	# ----------------------------------------------------------------
	
	def status(self):
		return self.config
	
	def ping(self, x=None):
		x = x or time.time()
		self.writeline("PING :%s" % x)




