#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under
# the terms of the GNU Affero General Public License.
# 

# This is totally under construction - just getting started - does
# pretty much nothing (except create itself) at the moment.

from ...data.database import *

IRC_LOGDB_NCONFIG = "net/irc/config/logdb.conf"

class IRCLogDB(Database):
	"""Manages the IRC Log Database."""
	
	def __init__(self, *a, **k):
		"""
		Pass any args/kwargs if necessary (probably not). Do not pass
		the config file path - that's defined by IRC_LOGDB_NCONFIG.
		
		>>> ircdb = IRCLogDB()
		>>> ircdb.open()
		>>> ircdb.addbot("mybot")
		"""
		
		# load the config file path
		config = trix.nconfig(IRC_LOGDB_NCONFIG, *a, **k)
		
		# init the superclass (Database)
		Database.__init__(self, config, *a, **k)
		




	def addbot(self, botname):
		self.opq("addbot", (botname,))
		self.commit()
	
	def getbot(self, botname):
		self.opq("getbot", (botname,))
		self.commit()
	
	def getbotid(self, botid):
		self.opq("getbotid", (botid,))
		self.commit()
	
	def getbots(self):
		c = self.opq("getbots")
	
	
	def addnet(self, network):
		self.opq("addnet", (network,))
		self.commit()
	
	def addnick(self, nick):
		self.opq("addnick", (nick,))
		self.commit()
		
		"""
			"addbot" : "insert into bot (botname) values (?)",
			"addnet" : "insert into network values (?,?)",
			"addchan" : "insert into channel values (?,?,?)",
			"addnick" : "insert into nickname values (?,?,?)",
			"adduser" : "insert into username values (?,?,?)",
			"addmask" : "insert into hostmask values (?,?,?)",
			"addname" : "insert into realname values (?,?,?)",
			"addid"   : "insert into identity values (?,?,?,?,?,?)",
			"addchat" : "insert into chatlog values (?,?,?,?,?)",
			
			"netid" : "select netid from network where network = ?",
			"chanid" : "select chanid from channel where channel = ?",
			"nickid" : "select nickid from nickname where nickname = ?",
			"userid" : "select userid from username where username = ?",
			"maskid" : "select maskid from hostmask where hostmask = ?"
		"""