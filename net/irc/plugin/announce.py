# Copyright 2018 justworx
# This file is part of the trix project, distributed under
# the terms of the GNU Affero General Public License.
#


from . import *
from ...urli import *


class Announce(IRCPlugin):
	"""Scan lines for urls and check for embed info (eg, youtube)."""
	
	def __init__(self, pname, bot, config=None, **k):
		IRCPlugin.__init__(self, pname, bot, config, **k)
		keys = config.get('tags')
		self.uu = EmbedInfo(keys)
	
	def handle(self, e):
		
		# don't let botix trigger the announcement!
		if e.nick != self.bot.nick:
			targ = e.target
			info = self.uu.query(e.text)
			if info:
				self.bot.writeline("PRIVMSG %s :%s" % (targ, info))
	
