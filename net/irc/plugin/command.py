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
		
		#
		# AUTHORIZATION
		#  - Currently, only 'owner' (as set in bot.json file) can
		#    control the bot via PRIVMSG/NOTICE.
		#  - NOTE: The 'owner' member variable is a list.
		#  - TODO: Needs a better auth scheme that allows partial 
		#          control by others and/or all.
		#
		if (e.host in self.bot.owner): #or ???:
			
			if e.irccmd == "PRIVMSG":
				self.handle_privmsg(e)
			elif e.irccmd == "NOTICE":
				self.handle_notice(e)
	
	#
	# dispatch command as it was received (PRIVMSG or NOTICE)
	#
	def handle_privmsg (self, e):
		x = self.handle_command(e)
		if x:
			self.bot.writeline("PRIVMSG %s :%s" % (e.nick, x))
	
	def handle_notice (self, e):
		x = self.handle_command(e)
		if x:
			self.bot.writeline("NOTICE %s :%s" % (e.nick, x))
	
	#
	# actual handling of commands
	#
	def handle_command( self, e):
		
		try:
			cmd = e.argv[0].lower()
			if cmd == 'join':
				self.bot.writeline("JOIN %s" % e.argv[1])
			elif cmd == 'part':
				if self.is_channel_name(e.argv[1]): # TODO: see below 
					self.bot.writeline("PART %s" % e.argv[1])
			elif cmd == 'quit':
				self.bot.writeline("QUIT :%s" % " ".join(e.argv[1:]))
			elif cmd == 'nick':
				self.bot.writeline("NICK %s" % " ".join(e.argv[1:]))
			elif cmd == 'tell':
				target = e.argv[1]
				message = " ".join(e.argv[2:])
				self.bot.writeline("PRIVMSG %s :%s" % (target, message))
			elif cmd == 'mode':
				self.bot.writeline(" ".join(e.argv[0:]))
		
			# -- bot internal control --
			elif cmd == 'debug':
				self.bot.debug = int(e.argv[1])
			
			# -- all purpose --
			# e.g., do mode +v nick
			elif cmd == 'do':
				self.bot.writeline(" ".join(e.argv[1:]))
		
		# -- error handling --
		except Exception as ex: 
			typ = str(type(ex))
			err = str(ex)
			msg = "%s: %s" % (typ, err)
			print ("# %s" % msg)
			return msg
	
	#
	# TODO: This probably belings in `irc.__init__` or something...
	#       possibly in some kind of extension system.
	#
	def is_channel_name(self, text):
		return text[0] == '#'

