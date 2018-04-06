# Copyright 2018 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.

from ...util.runner import *  # trix
from ..connect import Connect

"""python3
# sample server (echo)
from trix.net.server import *
s = Server(8888)
s.start()

# client
from trix.net.client import Client
c = Client()
c.connect("test1", s.port)
c["test1"].write("Hello!")
c["test1"].read()
"""


class Client(Runner):
	"""Client with multiple connections."""
	
	def __init__(self, config=None, **k):
		"""Pass config for Runner."""
		Runner.__init__(self, config, **k)
		
		if 'connect' in self.config:
			self.__contype = trix.value(self.config['connect'])
		elif 'nconnect' in self.config:
			self.__contype = trix.nvalue(self.config['nconnect'])
		else:
			self.__contype = Connect
		
		self.__conlist = {}
		self.get = self.__conlist.get
	
	def __del__(self):
		"""Calls `Stop()`."""
		self.stop()
	
	def __call__(self, conid):
		"""Read `conid` and handle any received data."""
		data = self.__conlist[conid].read()
		if data:
			self.handleio(data)
	
	def __contains__(self, conid):
		"""Return True if conid in this Client's connection list."""
		return conid in self.__conlist
	
	def __getitem__(self, conid):
		"""Return named connection."""
		return self.__conlist[conid]
			
	
	@property
	def contype(self):
		return self.__contype
	
	@property
	def conlist(self):
		return list(self.__conlist.keys())
	
	# CONNECT
	def connect(self, connid, config=None, **k):
		"""Pass required connection name and connect params."""
		self.__conlist[connid] = self.__contype(config, **k)
	
	# IO
	def io(self):
		"""Check for (and handle) input for each connection."""
		condict = self.__conlist
		if condict:
			rmvlist = []
			for k in condict:
				try:
					conn = condict.get(k)
					if conn:
						data = conn.read()
						if data:
							self.handleio(data)
					else:
						rmvlist.append(k)
				except BaseException as ex:
					self.handlex(type(ex), ex.args, xdata())
			
			if rmvlist:
				self.remove(rmvlist)
	
	# STOP
	def stop(self):
		Runner.stop(self)
		self.remove(self.__conlist)
	
	# REMOVE (connections)
	def remove(self, rmvlist):
		for cname in rmvlist:
			conn = cc.get(cname)
			try:
				conn.shutdown()
			except:
				pass
			try:
				del(self.__conlist[cname])
			except:
				pass
	
	# HANDLE-DATA
	def handleio(self, data):
		print (data)

