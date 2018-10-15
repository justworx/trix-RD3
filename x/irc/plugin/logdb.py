#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under
# the terms of the GNU Affero General Public License.
#

#####    ---    UNDER CONSTRUCTION!    ---    #####

from . import *

class LogDB(IRCPlugin):
	"""Log IRC chat conversations to a database."""
	
	def __init__(self, pname, bot, config=None, *a, **k):
		"""Pass database logging config."""
		
		# init superclass; sort out config
		IRCPlugin.__init__(self, pname, bot, config, *a, **k)
		
		# create the database object
		config = trix.nconfig("x/irc/plugin/logdb.conf")
		self.__db = trix.ncreate("data.database.Database", self.config)
	
	
	
	
	def handle(self, e):
		pass


