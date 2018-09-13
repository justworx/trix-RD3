#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under
# the terms of the GNU Affero General Public License.
#


from .. import *


class IRCPlugin(EncodingHelper):
	"""Base IRC plugin."""

	def __init__(self, pname, config=None, bot=None, **k):
		
		# store the bot object
		self.bot = bot
		
		# set default for this objects bot.ginfo dict
		bot.ginfo.setdefault(pname, {})
		
		# store the current dict as `self.info`
		self.info = bot.ginfo[pname]
		
		# setup config and encoding-related args
		self.config = config or {}
		self.config.update(k)
		EncodingHelper.__init__(self, self.config)
		
		# save create time
		self.created = time.time()
	
	
	def reply(self, e, text):
		"""Reply (`text`) to the user who triggerred the event `e`."""
		if text and (e.irccmd in ["PRIVMSG", "NOTICE"]):
			self.bot.writeline("PRIVMSG %s :%s" % (e.nick, text))
	
	
	def handle(self, e):
		# Plugins may override this to handle whatever action is
		# indicated by `event`.
		if event.argv[0] == 'about':
			self.reply(e, self.created)
	
	
	def update(self):
		# Plugins may override this to handle any maintenance activities;
		# It's called periodically as set in config.
		pass

