# Copyright 2018 justworx
# This file is part of the trix project, distributed under
# the terms of the GNU Affero General Public License.
#


from . import *
from ...urli import *


class Announce(IRCPlugin):
	"""Scan lines for urls and check for embed info (eg, youtube)."""
	
	def __init__(self, pname, config=None, bot=None, **k):
		IRCPlugin.__init__(self, pname, config, bot, **k)
		keys = config.get('tags')
		self.uu = EmbedInfo(keys)
	
	def handle(self, event):
		if event.nick != self.bot.nick:
			targ = event.target
			info = self.uu.query(event.text)
			if info:
				self.bot.writeline("PRIVMSG %s :%s" % (targ, info))
	
