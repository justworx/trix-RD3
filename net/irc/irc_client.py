#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.
#

#
# DEPRECATED!
#  - Do NOT use this package; it's absolutely 100% deprecated (except
#    for having been removed, which it soon will be). 
#  - Use `trix.net.irc.bot.Bot` instead.
#


from trix.net.client import *
from .irc_connect import *


class IRCClient(Client):
	
	DefType = IRCConnect
	
	
	# HANDLE-DATA
	def handleio(self, conn):
		
		if conn.debug:
			# Call the connection object's `io()` method so that received
			# text may be handled.
			conn.io()
	
	
	# HANDLE-X (Exception)
	def handlex(self, connid, xtype, xargs, xdata):
		if connid in self.conlist:
			conn = self[connid]
			
			#
			# DO WE REALLY NEED TO PASS THE XARGS HERE?
			# DON'T THEY AUTOMATICALLY SHOW UP IN XDATA?
			#
			irc.debug("irc_client.handlex", xtype, list(xargs))

