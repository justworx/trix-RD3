#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under 
# the terms of the GNU Affero General Public License.
#

from . import *
from ...net.irc import *


class irc(cline):
	"""Connect to an IRC server using IRCConnect."""
	
	def __init__(self):
		cline.__init__(self)
		
		if self.args:
			irc_connect(self.args[0], run=True, **self.kwargs)
	
	
