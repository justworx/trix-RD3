#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.
#
# UNDER CONSTRUCTION - DOES NOT WORK! - DO NOT USE! - DANGER W.R.!!!
#
#	 - This module is under construction. I need to push it so that I 
#    can access it from a different location. (It's complicated.)
#
#  - USE OF THIS CODE MAY DAMAGE YOUR FILES, EQUIPMENT, SANITY!
#

#
#  SERIOUSLY... DO NOT USE THIS MODULE YET!
# 
#raise BaseException ("DO NOT RUN THIS CODE!")


from . import *
from ..client import *
from ...app.jconf import *
	
BOT_CACHE_DIR = "~/.cache/trix/irc/bots/%s.json"

# For building paths to default config files.
IRC_CONFIG_DIR  = "trix/net/irc/config/"
BOT_CONF_PLUGIN = "irc_plugin.conf"
BOT_CONF_DEF    = "irc_config.conf"
BOT_CONF_FORM   = "irc_config.conf"


class Bot(Client):
	"""An irc bot object, containing zero or more irc connections."""
	
	# the type for new connection objects
	DEF_TYPE = 'trix.net.irc.irc_connect'
	
	# debugging
	Debugging = False
	def dbg(self, *a, **k):
		if self.Debugging:
			irc.debug(self, *a, **k)
	
	
	def __init__(self, botid):
		"""
		Pass string `botid` - the bot's name. The bot will be started if
		its config file exists in BOT_CACHE_DIR.  Otherwise, a new config 
		for the given `botid` must be generated, so a series of questions
		will appear in the terminal.
		
		NOTES: 
		 * The botid value is always reset to lower-case. 
		 * The BOT_CACHE_DIR is: "~/.cache/trix/irc/bots/";
		   The config file will be saved as <botid>.json, where <botid>
		   is the `botid` string given as the constructor.
		"""
		
		#
		# BOT ID 
		# Users give a name to each of their bots. Mine are:
		#  - rebbot: the bot running on the best working version 
		#  - botix : the bot I use to develop new features
		# Every bot config file in .cache config is named for its botid
		# in the format '~/.cache/trix/irc/bots/<BOTID>.json'
		#
		self.__botid = str(botid).lower()
		self.dbg("BOTID", self.__botid)
		
		#
		# Use the `trix.app.jconf` class to manage the config file.
		#	Load the config file at '~/.cache/trix/irc/bots/<BOTID>.json'
		#
		self.__pconfig = BOT_CACHE_DIR % self.__botid
		self.dbg("PCONFIG", self.__pconfig)
		
		self.__jconfig = jconf(self.__pconfig)
		self.dbg("JCONFIG", self.__jconfig)
		
		# Keep track of the config in self.__config
		self.__config = self.__jconfig.obj
		self.dbg("JCONFIG-OBJ", self.__jconfig.obj)
		
		#
		# The first time a botid is used, its config file will start
		# as an empty dict. That dict must be filled with defaults 
		# from `irc.config`.
		#
		if not self.__config.keys():
			#
			# Each new bot must start with config for all plugins, and an 
			# and an empty connection config dict.
			#
			self.__config['botid'] = botid
			self.__config['connections'] = {}
			self.__config['plugins'] = jconf(
					IRC_CONFIG_DIR + "irc_plugin.conf"
				).obj
			
			# make sure we get this far
			self.dbg("CONFIG-1 - GENERATED", self.__config)
			
			#
			# Every new botid requires at least one connection to run.
			# If on connection exists, add one now using the interactive
			# prompt in `self.conadd`.
			#
			conlist = self.__config.get('connections')
			if not conlist:
				self.conadd(botid)
	
	
	@property
	def botid (self):
		return self.__botid
	
	@property
	def config(self):
		return self.__config
	
	@property
	def jconfig(self):
		return self.__jconfig
	
	
	def conadd(self, botid):
		self.__addconfig(botid)
	
	
	def __loadconfig(self):
		botid = self.__botid
		self.__jconfig = jconf(BOT_CACHE_DIR % botid)
		self.__config = self.__jconfig.obj
		if not self.__config['connections']:
			self.__addconfig()
	
	
	def __addconfig(self, botid):
		cc = self.__config['connections']
		fm = trix.nmodule("x.form")
		fo = fm.Form(IRC_CONFIG_DIR + "irc_config.conf")
		
		self.config['connections'] = fo.fill()
		self.jconfig.save()
		#self.jconfig.obj['connections'] = scc
		
		
		#
		#
		#
		# YOU ARE HERE!
		#  - generate and save a config from console
		#  - i want to add a config param that lets me put the user
		#    into an "config add" form.
		#
		#
		#
	
	
	"""
	# HANDLE-DATA
	def handleio(self, conn):
		if conn.debug:
			# Call the connection object's `io()` method so that received
			# text may be handled.
			conn.io()
	
	
	def conadd(self):
		
		conlist=bc=xin=None
		try:
			# get the current exception list
			conlist = self.config.get('connections', {})
			
			# bot-config - import the default config values config
			bc = trix.nmodule('net.irc.config')
			
			# create a `trix.util.xinput.Form` object
			form = trix.ncreate(
					"util.xinput.Form", bc.CONNECTION_TEMPLATE
				)
			
			# run the form
			newcon = form.fill()
			newcid = newcon['connid']
			
			# make sure the conid is valid and unique
			if newcid in ['', None]:
				raise Exception("Invalid Connection ID: '%s'" % newcid) 
			if newcid in self.config['connections']:
				raise Exception("Connection '%s' already Exists!" % newcid)
			
			newconfig = xin()
			newconfig['port'] = int(newconfig['port'])
			newconfig['pi_update'] = int(newconfig['pi_update'])
			newconfig['pi_list'] = newconfig['pi_list'].split()
			
			# set connections values
			self.config['connections'][newcid] = newconfig
		
		except Exception as ex:
			raise type(ex)('err-config-fail', xdata(
					connid=connid, config=self.config, xin=xin, bc=bc
				))
	
	
	
	
	# HANDLE-X (Exception)
	def handlex(self, connid, xtype, xargs, xdata):
		if connid in self.conlist:
			conn = self[connid]
			irc.debug("irc_client.handlex", xtype, xargs)
	"""
