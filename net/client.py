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
		self.__connections = {}
	
	
	# DEL
	def __del__(self):
		"""Calls `Stop()`."""
		self.stop()
	
	
	# CALL
	def __call__(self, connid):
		"""Read `connid` and handle any received data."""
		data = self.__connections[connid].read()
		if data:
			self.handleio(data)
	
	
	# CONTAINS
	def __contains__(self, connid):
		"""Return True if connid in this Client's connection list."""
		return connid in self.__connections
	
	
	# GET ITEM
	def __getitem__(self, connid):
		"""Return named connection."""
		return self.__connections[connid]
	
	
	@property
	def conlist(self):
		"""Return list of of connection names."""
		return list(self.__connections.keys())
	
	
	
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
		xt=xa=xd = None
		config = config or {}
		try:
			
			# this allows dict config
			config.update(k)
			if 'create' in config:
				T = trix.value(config['connect'])
			elif 'ncreate' in config:
				T = trix.nvalue(config['nconnect'])
			else:
				T = self.DefType #Connect
		except Exception as ex:
			T = self.DefType 
			xt = type(ex)
			xa = ex.args
			xd = xdata()
		
		
		# this allows a config other than type dict (eg, port number)
		try:
			connection = T(config)
			self.__connections[connid] = connection
		except Exception as ex:
			raise type(ex)('err-connect-fail', xdata(
				xprior=[xt,xa,xd], config=config, T=T
			))			
	
	
	# IO
	def io(self):
		"""Check for (and handle) input for each connection."""
		condict = self.__connections
		if condict:
			rmvlist = []
			
			# loop through each connection name 
			for connid in condict:
				try:
					#
					# If the connection exists, handle it's io. Otherwise, 
					# remove it.
					#
					conn = condict.get(connid)
					if conn:
						self.handleio(conn)
					else:
						rmvlist.append(connid)
				
				except BaseException as ex:
					#
					# BIG CHANGE! 
					#  - Prefix identity of connect object that threw the 
					#    exception.
					#  - The Client class has been around (and unused, at least
					#    by me) for a long time. Neglecting to pass the connect
					#    objct from which the excepption has been a fatal flaw
					#    all along. This class has been unusable, or at least
					#    extremely annoying, because of it.
					#
					self.handlex(connid, type(ex), ex.args, xdata())
			
			# Handle any connection removals, specified in `rmvlist` by
			# connid string.
			if rmvlist:
				self.remove(rmvlist)
	
	
	# STOP
	def stop(self):
		Runner.stop(self)
		self.remove(list(self.__connections.keys()))

	
	# REMOVE (connections)
	def remove(self, rmvlist):
		for cname in rmvlist:
			conn = self.__connections.get(cname)
			if conn:
				try:
					conn.shutdown()
				except:
					pass
				try:
					del(self.__connections[cname])
				except:
					pass
	
	
	
	# --- override these to handle input and exceptions ---
	
	# HANDLE-DATA
	def handleio(self, conn):
		x = conn.read()
		if x:
			print (x)
	
	
	# HANDLE-X (Exception)
	def handlex(self, ident, xtype, xargs, xdata):
		print ("\nEXCEPTION! %s: %s(%s)" % (ident, xtype, xargs))
		if xdata:
			trix.display(xdata)
	

