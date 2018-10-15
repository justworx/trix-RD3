#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under
# the terms of the GNU Affero General Public License.
#


from . import *


class IRCCalc(IRCPlugin):
	"""Calculate the result of math functions."""
	
	#
	# HANDLE
	#
	def handle(self, e):
		
		# only handles PRIVMSG 	and NOTICE events
		if not (e.irccmd in ["PRIVMSG","NOTICE"]):
			return

	
	
	#
	# HANDLE COMMAND
	#  - actual handling of commands
	#
	def handle_command( self, e):
		
		try:
			cmd = e.argvl[0]
			if cmd in ['calc', 'calculate']:
				pass
