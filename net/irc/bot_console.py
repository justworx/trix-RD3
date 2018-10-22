#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.
#


from trix.app.console import *


BOTCONSOLE_NCONFIG = "net/irc/config/irc_console.conf"


class BotConsole(Console):
	def __init__(self, bot):
		"""Pass the Bot object for which this console will operate."""
		
		# set up variables
		self.__bot = bot
		
		# config - Always uses the BOTCONSOLE_NCONFIG configuration
		Console.__init__(self, trix.nconfig(BOTCONSOLE_NCONFIG))
	
	
	#
	# HANDLE INPUT
	#
	def handle_input(self, e):
		"""Handle input event `e`."""
		
		if e.argc:
			
			# handle valid commands...
			if e.argvl[0] == 'test':
				pass
			
			elif e.argvl[0] == "quit":
				msg = "Bye!"
				self.bot.writeline("QUIT :%s" % msg)
			
			elif e.argvl[0] == 'edit':
				if e.argc > 2:
					pass ("not yet implemented")
			
			elif e.argvl[0] == 'add':
				if e.argc > 2 and e.arglv[1] == 'bot':
					trix.display(self.__bot.configadd(e.argv[2]))
				else:
					print ("try: add bot 'botname'")
					#print (" - add connection 'connection-name'")
			
			
			else:
				Console.handle_input(e)
	
		