#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under 
# the terms of the GNU Affero General Public License.
#

from . import *


class help(cline):
	"""
	Command-line Plugin Test - Prints given command data.
	
	Arguments given on the command line are split into a list of values
	and processed as follows:
		
		1. The first argument is the `app` name is placed in `self.app`.
		2. The second is the command, and is placed in `self.cmd`.
		3. Arguments preceeded by two dash characters are considered 
		   keyword arguments and placed in a `self.kwargs` dict.
		4. Arguments preceeded by a single dash character are considered
		   flags; All characters following the dash are added to the 
		   `self.flags` string.
		5. All other arguments are stored in `self.args` in the order
		   they're received.
	
	"""
	
	def __init__(self):
		cline.__init__(self)
		
		print ('\nTest Response:')
		print (" - App   :", self.app)
		print (" - Cmd   :", self.cmd)
		print (" - Args  :", self.args)
		print (" - Flags :", self.flags)
		print (" - Kwargs:", self.kwargs)
		print ('')
