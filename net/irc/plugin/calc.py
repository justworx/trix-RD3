#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under
# the terms of the GNU Affero General Public License.
#

from . import *
from ....util.matheval import *
from ....util.compenc import *

class IRCCalc(IRCPlugin):
	"""Useful commands for controlling the bot via privmsg/notify."""
	
	#
	# HANDLE
	#
	def handle(self, e):
		
		# only handles PRIVMSG 	and NOTICE events
		if not (e.irccmd in ["PRIVMSG","NOTICE"]):
			return 

		cmd = e.argvl[0]
		if not cmd.strip():
			return
		
		try:
			args = " ".join(e.argvl[1:])
			if cmd in ['calc', 'calculate']:
				self.reply(e, str(matheval(args)))
			
			else:
				enc = self.bot.encoding
				try:
					spx = e.text.split(' ', 1) # get all but the first word
					bts = spx[1].encode(enc)   # encode it to bytes
					if cmd == 'b64':
						self.reply(e, b64.encode(bts).decode(enc))
					elif cmd == 'b64d':
						self.reply(e, b64.decode(bts).decode(enc))
					elif cmd == 'b32':
						self.reply(e, b32.encode(bts).decode(enc))
					elif cmd == 'b32d':
						self.reply(e, b32.decode(bts).decode(enc))
					elif cmd == 'b16':
						self.reply(e, b16.encode(bts).decode(enc))
					elif cmd == 'b16d':
						self.reply(e, b16.decode(bts).decode(enc))
				except IndexError:
					err = "%s command requires arguments. Eg, `%s some text`"
					self.reply(e, err % (cmd, cmd))
				
		except Exception as ex:
			typ = str(type(ex))
			err = str(ex)
			irc.debug("command plugin error", typ, err)
			
			msg = "%s: %s" % (typ, err)
			self.reply(e, msg)
		