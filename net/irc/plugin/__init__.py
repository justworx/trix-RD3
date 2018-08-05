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
		
	def handle(self, event):
		pass
	
	def update(self):
		pass


