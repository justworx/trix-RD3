#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.
#

from ..util.runner import *
from ..util.sock.sockcon import *

class AConnect(sockcon, Runner):
	"""
	Pass config for Runner and sockcon.
	
	AConnect is based on both sockcon and Runner. The Runner methods
	need not be used but are available so that subclasses can override
	AConnect.io() and call AConnect.start() to process received data in
	cases where this is necessary.
	
	Unlike Runner, AConnect objects connect immediately on creation.
	Unlike the previous version of connect, 
	
	The `AConnect.open` and `AConnect.close` method will still be 
	called automatically by `called.run` and `called.stop`.
	"""
	
	def __init__(self, config=None, **k):
		sockcon.__init__(config, **k)
		Runner.__init__(self, self.config, **k)
		
	
	
	
	def open(self):
		if self.active:
			raise Exception("err-already-open")
		sockcon.__init__(self, config, **k)
		Runner.open(self)
	
	
	
	def close(self):
		if self.active:
			sockcon.shutdown(self)
		Runner.shutdown()
	
	
	
	def status(self):
		return dict(
			runner=Runner.status(self),
			connect=dict(
				newl = self.newl,
				addr = self.addr,
				peer = self.peer,
				port = self.port,
				buflen = self.buflen,
				family = self.family,
				urlinfo = self.url,
				ctimeout = self.ctimeout,
				socktype = self.socktype
			)
		)
	
	
	# TESTING
	def io(self):
		x = self.read()
		if x:
			print (x)
	
