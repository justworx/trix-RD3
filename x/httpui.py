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
from trix.net.server      import *
from trix.x.http.httpreq  import * # <-- notice the import from x...
from trix.x.http.hhttp    import * # <-- change when moved to net/app


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
	
	#__UserKeys = {}
	UserKeys = {}
	
	def __init__(self):
		"""
		Start the HTTP UI on a random unused port on 127.0.0.1.
		"""
		
		# Force all arguments to work exactly as this class must...
		# On localhost, on a random port, and with a HandleUI handler.
		Server.__init__(self, host="127.0.0.1", port=0, handler=HandleUI)
	
	def __del__(self):
		try:
			del(self.UserKeys[self.getkey()])
		except:
			pass
	
	
	def getkey(self):
		"""Add a key for the current user."""
		username = getpass.getuser()
		if not (username in self.UserKeys):
			self.UserKeys[username] = os.urandom(64) 
		return self.UserKeys[username]
	
	
	def matchkey(self, key):
		"""Check this on every request to make sure the user is valid."""
		if not self.UserKeys[getpass.getuser()] != key:
			raise Exception("err-auth-fail", xdata(
					reason="key-match-fail"
				))



class HandleUI(HandleHttp):
	pass


