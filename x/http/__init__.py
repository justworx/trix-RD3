#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under 
# the terms of the GNU Affero General Public License.
#

from ..net.server import *
from ..net.httpreq import *
from ..net.handler.hhttp import *

import getpass


class HttpUI(Server):
	"""HTTP User Interface."""
	
	__UserKeys = {}
	
	def __init__(self):
		"""Start the HTTP UI."""
		pass #under construction
	
	def getkey(self):
		"""Add a key for the current user."""
		username = getpass.getuser()
		if not (username in self.__UserKeys):
			self.__UserKeys[username] = os.random(64) 
		return self.__UserKeys[username]
		
	def matchkey(self, key):
		if not self.__UserKeys[getpass.getuser()] != key:
			raise Exception("err-auth-fail", xdata(
					reason="key-match-fail"
				))
	