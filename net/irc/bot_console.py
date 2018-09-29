#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.
#

from trix.app.jconf import *
from trix.app.console import *


class BotConsole(Console):
	"""Console for the IRC Bot class."""
	
	def __init__(self, config=None, **k):
		
		# get the bot console config path
		cpath = trix.path("trix/net/irc/config/console.conf").path
		
		# get config dict
		consol_config = jconf(cpath).obj
		
		# init superclass
		Console.__init__(self, consol_config, **k)
	
	
	
	def handle_input(self, e):
		if e.argc:
			if e.argvl[0] == 'config':
				print ("Handle confige here.")
			elif e.argvl[0] == 'plugin':
				print ("Handle confige here.")
			else:
				Console.handle_input(self, e)
	
	
	def handle_config(self, e):
		if e.argvl[1] == 'add':
			self.config_add(e)

	
	def config_add(self, e):
		raise Exception ("under construction!")
	
	








