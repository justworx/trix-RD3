#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.
#



from . import *
from .irc_connect import *
from ..client import *



BOT_CACHE_DIR = "~/.cache/trix/irc/bots/%s.json"
IRC_CONFIG_DIR  = trix.npath("net/irc/config").path



class Bot(Client):
	"""An irc bot object, containing zero or more irc connections."""
	
	# the type for new connection objects
	DefType = trix.nvalue("net.irc.irc_connect", "IRCConnect")
	
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
		# Users give a name to each of their bots.
		# Every bot config file in .cache config is named for its botid
		# in the format '~/.cache/trix/irc/bots/<BOTID>.json'
		#
		self.__botid = str(botid).lower()
		
		#
		# Use the `trix.app.jconf` class to manage the config file.
		#	Load the config file at '~/.cache/trix/irc/bots/<BOTID>.json'
		#
		self.__pconfig = BOT_CACHE_DIR % self.__botid
		self.__jconfig = trix.jconfig(self.__pconfig)
		self.__debug = 0
		
		# Keep track of the config in self.__config
		self.__config = self.__jconfig.obj
		
		#
		# The first time a botid is used, its config file will start
		# as an empty dict. That dict must be filled with defaults 
		# from `irc.config`.
		#
		if not self.__config.keys():
			#
			# Each new bot must start with a botid and an empty connection
			# config dict.
			#
			self.__config['botid'] = botid
			self.__config['connections'] = {}
			
			#
			# Every new botid requires at least one connection to run.
			# If on connection exists, add one now using the interactive
			# prompt in `self.configadd`.
			#
			conlist = self.__config.get('connections')
			if not conlist:
				self.configadd(botid)
		
		# Finally, init the superclass
		Client.__init__(self, self.config)
	
	
	def start(self):
		"""
		Start running all connections for this Bot.
		"""
		try:
			# for except clause, in case it doesn't get far enough to 
			# define one of these...
			connid = None
			config = None
			
			# get the connections dict from self.config
			cconnections = self.config.get('connections', {})
			
			# loop through each connections key
			for connid in cconnections:
				
				# get this connection's config
				config = cconnections[connid]
				
				# if the connection is marked inactive, skip it
				if not config.get("active", True):
					continue
				
				#
				# At this point, DefType is irc_config, and variables are:
				#  * connid = the connection-dict's key
				#  * config = the connection's value
				#
				self.connect(connid, config)
				
			#
			# FINALLY - The connections are added to client.conlist and
			#           it's time for the Bot (Client) to start calling
			#           its io() method.
			#
			Client.start(self)
		
		
		except Exception as ex:
			self.stop()
			raise type(ex)("err-bot-fail", xdata(detail="bot-start-fail",
					connid=connid, conntype=self.DefType, config=config
				))
	
	
	
	@property
	def botid (self):
		return self.__botid
	
	@property
	def config(self):
		return self.__config
	
	@property
	def jconfig(self):
		return self.__jconfig
	
	@property
	def debug (self):
		return self.__debug
	
	@debug.setter
	def debug (self, i=1):
		self.__debug = i
	
	
	
	# CONFIG-ADD
	def configadd(self, botid):
		self.__addconfig(botid)
	
	
	# HANDLE-DATA
	def handleio(self, conn):
		if conn.debug:
			# Call the connection object's `io()` method so that received
			# text may be handled.
			conn.io()
	
	# HANDLE-X (Exception)
	def handlex(self, connid, xtype, xargs, xdata):
		if connid in self.conlist:
			conn = self[connid]
			irc.debug("irc_client.handlex", xtype, xargs)

	
	#
	# private methods
	#
	
	def __loadconfig(self):
		botid = self.__botid
		self.__jconfig = jconf(BOT_CACHE_DIR % botid)
		self.__config = self.__jconfig.obj
		if not self.__config['connections']:
			self.__addconfig()
	
	#
	#
	# ADD CONFIG
	#  - Create a new configuration file for a given `botid`
	#
	def __addconfig(self, botid):
		
		# get the configuration directory
		confdir = IRC_CONFIG_DIR
		
		cc = self.__config['connections']         # connections dict
		fm = trix.nmodule("app.form")             # form entry module
		fo = fm.Form(confdir + "irc_config.conf") # form object
		
		# use `fo` Form to get a connection configuration
		condict = fo.fill()
		
		# save network name and configid for use below
		network = condict.get('network')
		configid = "%s-%s" % (network, botid)
		
		#
		# LOAD FRESH PLUGIN CONFIG
		#  - Add plugin config for each connection; plugin config must
		#    be duplicated so that each connection retains fine-tuneable 
		#    control over its own set of plugin objects.
		#
		condict['plugins'] = trix.jconfig(confdir + "/irc_plugin.conf").obj
		
		# add the connection for `botid`
		self.config['connections'][configid] = condict
		self.config['connections'][configid]['plugins'] = plugins
		
		self.jconfig.save()
		
		return self.jconfig.obj
