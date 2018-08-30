#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under
# the terms of the GNU Affero General Public License.
#

from trix.util.enchelp import *
from trix.net.client import *


IRC_DEBUG = 1  # debug level default: 1
PLUG_UPDT = 15 # update plugins every 15 seconds


#
# ---- IRC Functions -----
#
class irc(object):
	"""IRC Utility Class."""
	
	@classmethod
	def config(cls, config, **k):
		"""
		Pass config dict or string path to config json file. Returns
		the given dict, or a dict taken from a json file, updated with
		any given keyword arguments.
		"""
		
		# get configuration
		if isinstance(config, str):
			conf = trix.path(config).wrapper(encoding='utf_8').read()
			conf = trix.jparse(conf)
		elif isinstance(config, dict):
			conf = config
		else:
			raise ValueError("err-invalid-config", xdata(
					detail="bad-config-type", require1=['dict','json-file-path'],
					Note="Requires a dict or string path to json file"
				))
		return conf
	
	
	
	@classmethod
	def connect(cls, config, **k):
		"""
		Pass config dict or string path to config json file. Connects to 
		IRC network and returns an IRCConnect object (see below).
		"""
		
		# get configuration
		conf = cls.config(config, **k)
		
		# create and return the connect object
		return trix.ncreate("net.irc.irc_connect.IRCConnect", conf, **k)
	
	
	
	"""
	@classmethod
	def client(cls, config=None):
		#Pass `config` as dict or json file path. If `config` is None,
		#a client object is returned with no clients running; You can use
		#`Client.connect()` to add new connections individually.
		
		# load the full config (or {})
		config = cls.config(config or {})
		
		
		#raise Exception(config)
		# Has "client" and "connections" keys; connections has botix
		
		
		# get client portion of config
		cclient = config.get("client", {})
		if not "create" in cclient:
			cclient.setdefault("ncreate", "net.irc.irc_connect.IRCConnect")
		
		
		#raise Exception(cclient)
		# Has "ncreate" and "sleep" keys
		
		
		# create the client object using `cclient` config dict
		client = Client(cclient)
		
		# load the connect portion of the config (the "networks" key)
		cconnect = config.get("connections", {})
		
		
		#raise Exception(cconnect)
		# has "botix" config
		
		
		# load any connections
		for con_name in cconnect:
			
			
			#print ("CON NAME:", con_name)
			
			
			# get each connection name and its configuration
			con_config = cconnect[con_name]
			
			
			#raise Exception(con_config)
			# has botix config dict
			
			
			# Client calls each connection's `io` method, so make sure 
			# both run and start are False. (This may not be necessary or
			# even desirable - it may change if the Client class changes.
			con_config['run'] = False
			con_config['start'] = False
			
			# add this connection to the client
			client.connect(con_name, con_config)
		
		# return the client object
		return client
	"""
	
	
	@classmethod
	def debug (*a, **k):
		if IRC_DEBUG:
			print ("\n#\n# DEBUG:")
			for item in a:
				print ("# %s" % str(item))
			if k:
				trix.display(k)
			print ("#\n")



