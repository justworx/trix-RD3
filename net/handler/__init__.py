#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.
#

#from .. import *
from ...util.sock.sockwrap import * # time


HANDLER_MAXIDLE = 300
HANDLER_BUFFER  = 4096


class Handler(sockwrap):
	"""Server Connection handler; Default action: echo server."""
	
	def __init__(self, sock, **k):
		
		k.setdefault('buflen', HANDLER_BUFFER)
		trix.log("Handler.__init__", sock=repr(sock), k=k)
		
		# 
		# INIT
		#  - Receives a socket as produced by sockserv. DOES NOT store
		#    the socket here, but passes it to sockwrap, which passes it
		#    on to sockprop.
		#  - The sockprop class stores the actual socket object privately
		#    and exposes only a proxy to the socket (so as to prevent any
		#    chance of losing track of the socket and allowing it to stay
		#    open after the program exits.
		#
		#    REMEMBER...
		#  - DO NOT STORE the actual socket object anywhere but sockprop.
		#
		sockwrap.__init__(self, sock, **k)
		trix.log("Handler.config", config=self.config)
		
		# defaults
		self.timeout = self.config.get('timeout', SOCK_TIMEOUT)
		
		# handler setup
		self.__maxidle = k.get('maxidle', HANDLER_MAXIDLE)
		self.__lastrecv = time.time()
	
	
	@property
	def maxidle(self):
		return self.__maxidle
	
	@property
	def lastrecv(self):
		return self.__lastrecv
	
	@property
	def countdown(self):
		return self.maxidle - (time.time() - self.lastrecv)
	
	
	# HANDLE
	def handle(self):
		# receive/handle any sent data
		try:
			data = self.socket.recv(self.buflen)
			#trix.log("Handler.handle", data=data)
			if data:
				self.__lastrecv = time.time() # update for timeout
				self.handledata(data)
		except socket.timeout as ex:
			pass # Ignore Timeout
		except BaseException as ex:
			#trix.log("Handler.handle FAIL!", 
			#	data=data, ex=type(ex).__name__, xargs=ex.args
			#)
			raise
	
	
	# HANDLE DATA
	def handledata(self, data):
		"""
		OVERRIDE THIS METHOD!
		This method is a placeholder. You must override it to implent
		meaningful functionality (unless what you want is an echo server).
		"""
		if data:
			self.socket.send(data)

