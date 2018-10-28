#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under 
# the terms of the GNU Affero General Public License.
#

# UNDER CONSTRUCTION - JUST GETTING STARTED

import os, getpass

from trix.net.server import *
from trix.net.httpreq import *

class HttpUI(Server):
	"""
	This HTTP User Interface is intended only for use on localhost, and
	on a single-user (that is, one user at a time) system. It checks 
	system username and associates it with a random key which is used
	as authentication to operate as (and with the same access as) the 
	current (real) user. 
	
	This should be relatively safe for the typical user who does not
	have remote access enabled.
	
	HOWEVER:
	Using this interface on a system to which other users might connect
	simultaneously poses a rather significant risk, because a network
	sniffer could easily extract the key from transactions and then
	impersonate the valid user - a serious threat to your privacy,
	data, and system integrity.
	
	NOTE ALSO:
	Altering or overriding this class to allow network access outside 
	of localhost would result in the same risk.
	"""
	
	#__UserKeys = {}
	UserKeys = {}
	
	def __init__(self):
		"""
		Start the HTTP UI on a random unused port on 127.0.0.1.
		"""
		
		Server.__init__(self, host="127.0.0.1", port=0, 
				nhandler='net.handler.hhttp.HandleHttp'
			)
	
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


