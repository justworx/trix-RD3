#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under
# the terms of the GNU Affero General Public License.
#


#
# UNDER CONSTRUCTION!
#  - Actually, this is totally untested. it may change or even
#    totally disappear.
#


from . import *


class IRCInfo(IRCPlugin):
	"""Info collected from various commands."""
	
	def __init__(self, config=None, bot=None, **k):
		IRCPlugin.__init__(self, config, bot, **k)
		self.info = {}
		
	def handle(self, event):
		
		# connect info
		if event.irccmd = '005':
			data = event.text.split()
			flag = []
			pair = {}
			
			for item in data:
				x = item.split("=")
				try:
					pair[x[0]] = x[1]
				except IndexError:
					flag.append(x[0]
