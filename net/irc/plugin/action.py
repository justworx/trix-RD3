# Copyright 2018 justworx
# This file is part of the trix project, distributed under
# the terms of the GNU Affero General Public License.
#

from . import *


class IRCAction(IRCPlugin):
	"""Info collected from various commands."""
	
	CONNECT_HANDLED = False
	
	def __init__(self, pname, bot, config=None, **k):
		IRCPlugin.__init__(self, pname, bot, config, **k)
		self.on_connect = self.config.get("on_connect")
		self.connected = False
	
	
	def handle(self, e):
		pass
		
		"""
		if not self.CONNECT_HANDLED:
			if e.argvl.irccmd == '376':  # end motd
				print ("\n")
				trix.display(e.dict)
				for cmd in self.on_connect:
					self.bot.writeline(cmd)
					print (cmd, "\n")
				self.CONNECT_HANDLED = True
		
		"""

