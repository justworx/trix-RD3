#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under
# the terms of the GNU Affero General Public License.
#


from . import *


class IRCCommand(IRCPlugin):
	"""Useful commands for controlling the bot via privmsg/notify."""
	
	def handle(self, e):
		
		# only handles PRIVMSG 	and NOTICE events
		if not (e.irccmd in ["PRIVMSG","NOTICE"]):
			return
		
		# FIX THIS! (auth needs to be passed through config somehow)
		if e.uid == 'ninebits@ninebits.users.undernet.org':
			
			if e.irccmd == "PRIVMSG":
				self.handle_privmsg(e)
			elif e.irccmd == "NOTICE":
				self.handle_notice(e)
	
	
	def handle_privmsg (self, e):
		pass
	
	
	def handle_notice (self, e):
		x = self.handle_command(e)
		if x:
			self.bot.writeline("NOTICE %s :%s" % (e.nick, x))
	
	
	def handle_command( self, e):
		cmd = e.argv[0]
		if cmd == 'JOIN':
			self.bot.writeline("JOIN %s" % e.argv[1])
		elif cmd == 'PART':
			if self.is_channel_name(e.argv[1]): # TODO: see below 
				self.bot.writeline("PART %s" % e.argv[1])
		elif cmd == 'QUIT':
			self.bot.writeline("QUIT %s" % " ".join(e.argv[1:]))
	
	
	#
	# TODO: This probably belings in `irc.__init__` or something...
	#       possibly in some kind of extension system.
	#
	def is_channel_name(self, text):
		return text[0] == '#'

