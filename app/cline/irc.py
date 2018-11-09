#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under 
# the terms of the GNU Affero General Public License.
#

#
# THIS DOES NOT WORK - I DON'T KNOW WHY (Maybe it's `run`)
#

from . import *
from ...net.irc.bot import *

class irc(cline):
	"""
	Connect to an IRC server using IRCConnect.
	
	Pass your botname. If you haven't yet created a bot configuration,
	a form will appear to gather the information needed to connect to
	your IRC network. Subsequent calls using this botname will reuse
	that same config ("~/.config/trix/irc/bots/<botname>.conf").
	"""
	
	def __init__(self):
		cline.__init__(self)
		
		if self.args:
			Bot(*self.args, **self.kwargs).run()
		else:
			print ("Error:", "You must provide a bot name.")
