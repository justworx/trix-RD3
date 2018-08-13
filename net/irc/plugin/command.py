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
		
		# DEBUGGING 
		#print ("# DEBUG:")
		#trix.display(e.dict)
		
		# FIX THIS! (auth needs to be passed through config somehow)
		if e.host == 'ninebits.users.undernet.org':
			
			if e.irccmd == "PRIVMSG":
				self.handle_privmsg(e)
			elif e.irccmd == "NOTICE":
				self.handle_notice(e)
	
	
	def handle_privmsg (self, e):
		x = self.handle_command(e)
		if x:
			self.bot.writeline("PRIVMSG %s :%s" % (e.nick, x))
	
	
	def handle_notice (self, e):
		x = self.handle_command(e)
		if x:
			self.bot.writeline("NOTICE %s :%s" % (e.nick, x))
	
	
	def handle_command( self, e):
		#print ("# handle_command")
		#print ("# ARGV: %s" % (e.argv))
		cmd = e.argv[0].lower()
		if cmd == 'join':
			self.bot.writeline("JOIN %s" % e.argv[1])
		elif cmd == 'part':
			if self.is_channel_name(e.argv[1]): # TODO: see below 
				self.bot.writeline("PART %s" % e.argv[1])
		elif cmd == 'quit':
			self.bot.writeline("QUIT %s" % " ".join(e.argv[1:]))
		elif cmd == 'nick':
			self.bot.writeline("NICK %s" % " ".join(e.argv[1:]))
		elif cmd == 'tell':
			target = e.argv[1]
			message = " ".join(e.argv[2:])
			self.bot.writeline("PRIVMSG %s :%s" % (target, message))
		elif cmd == 'mode':
			self.bot.writeline(" ".join(e.argv[0:]))

		# all purpose
		# e.g., do mode +v nick
		elif cmd == 'do':
			self.bot.writeline(" ".join(e.argv[1:]))
		
	
	#
	# TODO: This probably belings in `irc.__init__` or something...
	#       possibly in some kind of extension system.
	#
	def is_channel_name(self, text):
		return text[0] == '#'

