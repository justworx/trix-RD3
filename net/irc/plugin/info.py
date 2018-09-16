#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under
# the terms of the GNU Affero General Public License.
#


from . import *


class IRCInfo(IRCPlugin):
	"""Info collected from various commands."""
	
	def __init__(self, pname, bot, config=None, **k):
		IRCPlugin.__init__(self, pname, bot, config, **k)
		if not self.info:
			self.info['flag'] = []
			self.info['pair'] = {}
	
	
	def handle(self, e):
		
		if not e.argv:
			return
		
		bcmd = e.argv[0]
		
		# connect info
		if bcmd == 'flags':
			trix.display(e.dict)
			self.reply(e, str(self.info['flag']))
		
		elif bcmd == 'pairs':
			item = bcmd.upper()
			self.reply(e, " ".join(self.info['pair'].keys()))
		
		elif bcmd == 'pair':
			if e.argc < 2:
				self.reply(e, "ERROR: pair key required.")
			else:
				key = e.argv[1].upper()
				if key in self.info['pair']:
					self.reply(e, self.info['pair'].get(key))
		
		
		#
		# PASSIVE
		#  - This one's different in that it responds to an irc command
		#    rather than a command given by PRIVMSG or NOTICE.
		#
		elif e.irccmd == '005':
			
			# data is an array now... need the first item
			data = e.text.split(':')
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
			
			# set channel types so they're directly available to the conn
			chantypes = self.info.get('pair',{}).get('CHANTYPES')
			if chantypes:
				self.bot.chantypes = chantypes
			
			# debug
			if self.bot.debug > 8:
				print("\n# info debug")
				trix.display(e.dict)
				trix.display(self.info)
				print("")
			

