#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under
# the terms of the GNU Affero General Public License.
#

from . import *
from ....util.matheval import *


class IRCCalc(IRCPlugin):
	"""Useful commands for controlling the bot via privmsg/notify."""
	
	#
	# HANDLE
	#
	def handle(self, e):
		
		# only handles PRIVMSG 	and NOTICE events
		if not (e.irccmd in ["PRIVMSG","NOTICE"]):
			return
		
		try:
			cmd = e.argvl[0]
			if cmd in ['calc', 'calculate']:
				self.reply(e, str(matheval(" ".join(e.argvl[1:]))))
		except Exception as ex:
			typ = str(type(ex))
			err = str(ex)
			irc.debug("command plugin error", typ, err)
			
			msg = "%s: %s" % (typ, err)
			self.reply(msg)
		