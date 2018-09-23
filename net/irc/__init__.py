#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under
# the terms of the GNU Affero General Public License.
#

from ... import *
from ...util.enchelp import *
from ...util.linedbg import *

IRC_DEBUG = 1  # debug level default: 1
PLUG_UPDT = 15 # update plugins every 15 seconds


#
# ---- IRC Functions -----
#
class irc(object):
	"""Common top-level irc classmethods."""
	
	@classmethod
	def config(cls, config, **k):
		"""
		Pass config dict or string path to config json file. Connects to 
		IRC network and returns an IRCConnect object (see below).
		"""
		
		# get configuration
		if isinstance(config, str):
			conf = trix.path(config).wrapper(encoding='utf_8').read()
			conf = trix.jparse(conf)
		elif isinstance(config, dict):
			conf = config
		else:
			raise ValueError("err-invalid-config", xdata(
					detail="bad-config-type", 
					require1=['dict','json-file-path'],
					Note="Requires a dict or string path to json file"
				))
				
		return conf
	
	
	@classmethod
	def client(cls, clientconfig=None, **k):
		"""
		Return an IRCClient object. If `clientconfig` is a dict and
		contains a `connections` key with valid IRCConnect configuration
		dicts, the connections will be added to the client object before
		it's returned.
		"""
		
		# sort out config
		try:
			# default clientconfig is an empty dict plus any kwargs
			conf = clientconfig or {}
			
			# if it's given as a string (file path) an raise an error
			# and load the json file as a dict
			conf.update(k)
			
		except AttributeError:
			# load json file and update with any given kwargs
			conf = cls.config(clientconfig)
			conf.update(k)
		
		
		# create the client object
		client = trix.ncreate("net.irc.irc_client.IRCClient", conf)
		
		# open any specified connections
		if 'connections' in conf:
			connections = conf['connections']
			for connid in connections:
				cconfig = connections[connid]
				if cconfig.get('enabled', True):
					client.connect(connid, cconfig)
		
		#
		# Start the client in a thread so that any connections receive
		# the time they need to handle input. If config or kwargs specify
		# that run=True, the client will be run in a closed loop (rather
		# than being started in a thread).
		#
		if conf.get('run'):
			client.run()
		else:
			client.start()
		
		# return the client
		return client
	
	
	@classmethod
	def connect(cls, config, **k):
		"""
		Returns an IRCConnect object.
		
		This is only useful if you want to manually handle io for the
		connection object. In this case, it's necessary to keep up with
		commands/data received from the server.
		"""
		
		# get the configuration dict
		conf = cls.config(config, **k)
		
		# create and return the connect object
		return trix.ncreate("net.irc.irc_connect.IRCConnect", conf)
	
	
	@classmethod
	def debug (*a, **k):
		if IRC_DEBUG:
			linedbg().dbg(*a, **k)



