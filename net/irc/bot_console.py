#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.
#


from trix.x.console import *


BOTCONSOLE_NCONFIG = "net/irc/config/irc_console.conf"


class BotConsole(Console):
	
	
	
	def __init__(self, bot):
		"""Pass the Bot object for which this console will operate."""
		
		# set up variables
		self.__bot = bot
		
		# config - Always uses the BOTCONSOLE_NCONFIG configuration
		Console.__init__(self, trix.nconfig(BOTCONSOLE_NCONFIG))
	
	
	@property
	def bot(self):
		return self.__bot
	
	
	#
	# HANDLE INPUT
	#
	def handle_input(self, e):
		"""Handle input event `e`."""
		
		if e.argc and e.argv[0]:
			
			if e.arg(0):
				print (
					"BotConsole:", 
					trix.formatter(f="JDisplay").output(e.argv)
				)
			
			else:
				Console.handle_input(self, e)
			
			#
			# now i need to:
			#  * get Console to use CLIEvent instead of TextEvent
			#  * get a 'pause' feature going in the bot
			#
			"""
			# handle valid commands...
			if e.argvl[0] == "quit":
				msg = "Bye!"
				self.bot.writeline("QUIT :%s" % msg)
			
			elif e.argvl[0] == 'edit':
				if e.argc > 2:
					pass ("not yet implemented")
			
			elif e.argvl[0] == 'add':
				if e.argc > 2 and e.arglv[1] == 'bot':
					trix.display(self.__bot.configadd(e.argv[2]))
				else:
					print ("USE --> add bot 'botname'")
					#print (" - add connection 'connection-name'")
			"""
	
	
	
	def create_event(self, commandLineText):
		return CLIEvent(commandLineText)
		