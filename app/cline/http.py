#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under 
# the terms of the GNU Affero General Public License.
#

from . import *
from ...util.urlinfo import *

class http(cline):
	"""
	Launch a web server. Use Ctrl-c to stop.
	
	Examples:
	# The default  will run on port 8888
	python3 -m trix http
	
	# for a web server on a different port:
	python3 -m trix http 8080
	
	# to see debug messages after, pass the -d flag
	python3 -m trix http -d
	"""
	
	DefPort = 8888
	
	def __init__(self):
		
		cline.__init__(self)
		
		# config may be given as a url
		config = self.args[0] if self.args else {}
		config.update(self.kwargs)
		
		if config:
			try:
				# in case config was given as a port, make it an int
				config = int(config)
			except:
				# If it was given as anything that doesn't convert to int,
				# then config won't be altered.
				pass
			
			config = urlinfo(config).dict
		
		if not 'port' in config:
			config['port'] = self.DefPort
		
		# for display (Open: link)...
		config.setdefault('host', 'localhost')
		config.setdefault('scheme', 'http')
		config.setdefault('handler', 'trix.net.handler.hhttp.HandleHttp')
		
		"""
		# config (if it exists) is updated by any given keyword args
		self.kwargs.setdefault(
			'handler', 'trix.net.handler.hhttp.HandleHttp'
		)
		config.update(self.kwargs)
		"""
		
		#trix.display([config, ])
		
		# create the server
		s = trix.ncreate('net.server.Server', config)
		
		try:
			print ("HTTP Server running on port: %i" % s.port) 
			print ("Open: %s" % s.url)
			print ("Use Ctrl-c to stop.")
			s.run()
		except KeyboardInterrupt:
			print ("Server stopped.")
		
		# display debug messages after server stops
		if ('d' in self.flags):
			s.display()

