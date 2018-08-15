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
		self.info = {'flag':[], 'pair':{}}
		
	def handle(self, event):
		# connect info
		if event.irccmd == '005':
			
			# data is an array now... need the first item
			data = event.text.split(':')
			data = data[0].split() # <--- split on ' ' (space)
			
			# parse each item into the correct info dict structure
			for item in data:
				x = item.split("=")
				try:
					# NAME=VALUD
					self.info['pair'][x[0]] = x[1]
				except IndexError:
					# FLAG-LIKE ITEMS
					self.info['flag'].append(x[0])
			
			
			# debug
			if self.bot.debug > 8:
				print("\n# info debug")
				trix.display(event.dict)
				trix.display(self.info)
				print("")
			

