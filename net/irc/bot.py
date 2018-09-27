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
raise BaseException ("DO NOT RUN THIS CODE!")


from . import *
from .config import *      
from ..client import *
from ...app.jconf import *
	
BOT_CACHE_DIR = "~/.cache/trix/irc/bots/%s.json"


class Bot(Client):
	"""An irc bot object, containing zero or more irc connections."""
	
	# the type for new connection objects
	DEF_TYPE = 'trix.net.irc.irc_connect'
	
	def __init__(self, botid):
		"""
		Pass string `botid` - the bot's name. If the named bot exists
		in .cache/trix/config.json, it will be started. Otherwise, a
		new config for the given `botid` will be generated, afterwhich
		the bot will be started.
		
		NOTE: Bot id is always reset to lower-case. Files with capital
		      letters belong to the Bot class.
		"""
		
		#
		# BOT ID 
		# Users give a name to each of their bots. Mine are:
		#  - rebbot: the bot running on the best working version 
		#  - botix : the bot I use to develop new features
		# Every bot config file in .cache config is named for its botid
		# in the format '~/.cache/trix/irc/bots/<BOTID>.json'
		#
		self.__botid = botid.lower()
		
		#
		# CONFIG
		# Configuration files are stored in the cache as JSON text.
		# 
		# The bot's owner must add one or more connection configuration
		# dicts to the cache/config file.
		#
		
		#
		# Use the `trix.app.jconf` class to manage the config file.
		#	Load the config file at '~/.cache/trix/irc/bots/<BOTID>.json'
		# Store this jconf object so that config may be saved later. 
		#
		self.__jconfig = jconf("~/.cache/trix/irc/bots/%s.json" % botid)
		
		# Keep track of the config in self.__config
		self.__config = self.__jconfig.obj
		
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
			self.__config['plugins'] = DEF_PLUGIN_CONFIG
			self.__config['connections'] = {}
			
			#
			# Every new botid requires at least one connection to run.
			# If on connection exists, add one now using the interactive
			# prompt in `self.conadd`.
			#
			conlist = self.__config.get('connections')
			if not conlist:
				self.conadd()
	
	
	def conadd(self):
		"""Add a connection configuration."""
		
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
	
	
	
	
	@property
	def botid (self):
		"""Return the botid."""
		return self.__botid
	
	
	@property
	def config(self):
		"""Return the config dict."""
		return self.__config
	
	
	
	
	
	
	# HANDLE-DATA
	def handleio(self, conn):
		"""Overrides Client.handleio()"""
		if conn.debug:
			# Call the connection object's `io()` method so that received
			# text may be handled.
			conn.io()
	
	
	# HANDLE-X (Exception)
	def handlex(self, connid, xtype, xargs, xdata):
		"""Overrides Client.handlex()"""
		if connid in self.conlist:
			conn = self[connid]
			irc.debug("irc_client.handlex", xtype, xargs)
