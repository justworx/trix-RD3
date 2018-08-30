#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under
# the terms of the GNU Affero General Public License.
#


from . import *


class IRCCommand(IRCPlugin):
	"""Useful commands for controlling the bot via privmsg/notify."""
	
	#
	# AUTHORIZATION
	#  - Currently, only 'owner' (as set in bot/<botname>.json file)
	#    can control the bot via PRIVMSG/NOTICE.
	#  - NOTE: The 'owner' member variable is a list.
	#  - TODO: Needs a better auth scheme that allows partial 
	#          control by others and/or all.
	#
	def authorize(self, e):
		return e.host in self.bot.owner
	
	
	
	#
	# HANDLE
	#
	def handle(self, e):
		
		# only handles PRIVMSG 	and NOTICE events
		if not (e.irccmd in ["PRIVMSG","NOTICE"]):
			return
		
		if self.authorize(e):
			result = self.handle_command(e)
			if result:
				self.reply(e, result)
	
	
	
	#
	# HANDLE COMMAND
	#  - actual handling of commands
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
			
			"""
			#
			# PLUGINS
			#
			elif cmd in ['plugin', 'plugins']:
				
				# lowercase the first argument
				arg1 = e.argv[1].lower()
				if arg1 == 'list':
					self.reply(e, " ".join(self.bot.plugins.keys()))
				else:
					argx = e.argv[2:] # plugin cmd <plugin list>
					
					# respond to argument 1
					if arg1 == 'load':
						for p in argx:
							# find plugin path
							ppath = 'net.irc.plugin.%s' % p.lower()
							
							# load plugin at ppath
							self.bot.plugins[p] = trix.ncreate(ppath)
						
						# report successful load
						self.reply(e, "load: %s" % (" ".join(argx)))
					
					elif arg1 == 'unload':
						for p in argx:
							# delete specified plugin (by name `p`)
							p = p.lower()
							del(self.bot.plugins[p])
						
						# report successful unload
						self.reply(e, "unload: %s" % (" ".join(argx)))
			"""
		
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

