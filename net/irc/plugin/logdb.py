#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under
# the terms of the GNU Affero General Public License.
#

#####    ---    UNDER CONSTRUCTION!    ---    #####

from . import *

class LogDB(IRCPlugin):
	"""Log IRC chat to a database."""
	
	def __init__(self, pname, bot, config=None, *a, **k):
		
		# init superclass; sort out config
		IRCPlugin.__init__(self, pname, bot, config, *a, **k)
		
		# create the database object
		dbconfig = trix.nconfig("net/irc/config/logdb.conf")
		self.__db = trix.ncreate("data.database.Database", dbconfig)
	
	
	
	
	def handle(self, e):
		pass
