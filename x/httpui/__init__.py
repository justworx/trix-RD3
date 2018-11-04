#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under 
# the terms of the GNU Affero General Public License.
#

#
# UNDER CONSTRUCTION - JUST GETTING STARTED
#  - This file belongs in trix.app. It's not a typical HTTP server,
#    it's an attempt at the implementation of a user interface for 
#    trix. 
#


import os, getpass
from trix.app.event import *
from trix.net.server import *
from trix.net.handler.hhttp import *
from trix.fmt import JCompact


class HttpUI(Server):
	"""
	This HTTP User Interface is intended only for use on localhost, and
	on a single-user (that is, one user at a time) system. It checks 
	system username and associates it with a random key which is used
	as authentication to operate as (and with the same access as) the 
	current (real) user. 
	
	This should be perfectly safe for the typical user who does not
	have remote access enabled (and does not have any other security
	holes).
	
	HOWEVER:
	Altering or overriding this class to allow network access outside 
	of your own localhost could carry some significant risks.
	
	Using this interface on a system to which other users might connect
	simultaneously would open you up to surveillance by a network
	sniffer, which could easily extract the transaction key for use to 
	impersonate the valid user - a potentially serious threat to your 
	privacy, data, and system integrity.
	"""
	
	def __init__(self):
		"""
		Start the HTTP UI on a random unused port on 127.0.0.1.
		"""
		
		# Force all arguments to work exactly as this class must...
		# On localhost, on a random port, and with a HandleUI handler.
		Server.__init__(self, host="127.0.0.1", port=0, handler=HandleUI)



#
#
#   User Interface Handler
#
#
class HandleUI(HandleHttp):
	"""
	To be used internally - future user interface for trix features.
	"""
	
	WebContent = "x/httpui/content/"
	
	#__UserKeys = {}
	UserKeys = {}
	
	def __init__(self, sock, **k):
		
		self.__username = getpass.getuser()
		
		rootdir = trix.innerfpath(self.WebContent)
		k['rootdir'] = rootdir
		
		HandleHttp.__init__(self, sock, **k)
	
	
	def __del__(self):
		"""Remove the UserKeys item associated with this object."""
		try:
			del(self.UserKeys[self.getkey()])
		except:
			pass
	
	
	def getkey(self):
		"""Add a key for the current user."""
		username = self.__username
		if not (username in self.UserKeys):
			self.UserKeys[username] = os.urandom(64) 
		return self.UserKeys[username]
	
	
	def matchkey(self, key):
		"""Check this on every request to make sure the user is valid."""
		if not self.UserKeys[self.__username] != key:
			raise Exception("err-auth-fail", xdata(
					reason="key-match-fail"
				))
	
	
	
	def handledata(self, data, **k):
		
		if data:
			# handle incoming javascript requests
			data = data.strip()
			if data == 'auth whoami':
				self.send(self.__username)
			elif data == 'state':
				self.send(JCompact().format({
						"server" : "trix/httpui", "revision" : "0.0 (rd3)",
						"title" : "trix!"
					}))
			
			else:
				# send content from httpui/content directory
				HandleHttp.handledata(self, data, **k)
	
	

