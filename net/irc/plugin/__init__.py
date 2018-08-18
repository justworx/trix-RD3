#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under
# the terms of the GNU Affero General Public License.
#


from .. import *


class IRCPlugin(EncodingHelper):
	"""Base IRC plugin."""

	def __init__(self, config=None, bot=None, **k):
		self.bot = bot
		self.config = config or {}
		self.config.update(k)
		EncodingHelper.__init__(self, self.config)
	
	
	def reply(self, e, text):
		"""Reply (`text`) to the user who triggerred the event `e`."""
		if text and (e.irccmd in ["PRIVMSG", "NOTICE"]):
			self.bot.writeline("PRIVMSG %s :%s" % (e.nick, text))
	
	
	def handle(self, event):
		# Plugins may override this to handle whatever action is
		# indicated by `event`.
		pass
	
	
	def update(self):
		# Plugins may override this to handle any maintenance activities;
		# It's called periodically as set in config.
		pass

