#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.
#


from trix.x.console import *


BOTCONSOLE_NCONFIG = "net/irc/config/irc_console.conf"


class BotConsole(Console):
	"""
	
	   EXTREMELY SERIOUSLY DEATH-DEFYINGLY **UNDER CONSTRUCTION**
	
	"""
	
	
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
			# NOTES
			#   * Quit is fine for killing all connections and ending the
			#     bot and its client, but we also need a command to end
			#     single connections. I guess `close` is the command...
			#   
			#   * Could this be a Wrapper?
			#     Considering the fact that Console is now using LineEvent,
			#     and there's nothing here (at the moment, anyway) of any
			#     use at all... couldn't I just add some well-named methods
			#     to the bot and use a console.Wrapper for Bot config?
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
	
	
	#
	# Console is now using LineEvent, so this doesn't need to be here.
	#
	def create_event(self, commandLineText):
		"""We need Console to call for custom event types."""
		return LineEvent(commandLineText)


