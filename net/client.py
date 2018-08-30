# Copyright 2018 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.

from ..util.runner import *  # trix
from .connect import Connect


class Client(Runner):
	"""Client with multiple connections."""
	
	DefType = Connect
	
	# INIT
	def __init__(self, config=None, **k):
		"""Pass config for Runner."""
		Runner.__init__(self, config, **k)
		self.__conlist = {}
	
	
	# DEL
	def __del__(self):
		"""Calls `Stop()`."""
		self.stop()
	
	
	# CALL
	def __call__(self, conid):
		"""Read `conid` and handle any received data."""
		data = self.__conlist[conid].read()
		if data:
			self.handleio(data)
	
	
	# CONTAINS
	def __contains__(self, conid):
		"""Return True if conid in this Client's connection list."""
		return conid in self.__conlist
	
	
	# GET ITEM
	def __getitem__(self, conid):
		"""Return named connection."""
		return self.__conlist[conid]
	
	
	@property
	def conlist(self):
		"""Return list of of connection names."""
		return list(self.__conlist.keys())
	
	
	
	# CONNECT
	def connect(self, connid, config=None, **k):
		"""
		Pass string `connid`, a unique name for this connection. Also 
		pass optional `config` dict (which is, as always, updated by 
		kwargs). 
		
		Config (or kwargs) should contain a "create" or "ncreate" key 
		describing the full (or inner, repsectively) pythonic path to 
		the [package.][module.]class to be created. This object must 
		implement the Config class (which is based on Runner).
		
		If no "create" or "ncreate" class path string is specified, the
		default trix.net.connect.Connect is used.
		
		Creates the described connection object and adds it to the 
		`self.conlist` connection list property.
		"""
		config = config or {}
		config.update(k)
		
		if 'create' in config:
			T = trix.value(config['connect'])
		elif 'ncreate' in config:
			T = trix.nvalue(config['nconnect'])
		else:
			T = self.DefType #Connect
		
		connection = T(config)
		self.__conlist[connid] = connection
	
	
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
			conn = c.get(cname)
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

