#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under 
# the terms of the GNU Affero General Public License.
#

from . import *


class portscan(cline):
	"""
	Scan local ports.
	"""
	def __init__(self):
		print ("Scanning local ports...")
		n = trix.ncreate('util.network.Host')
		r = n.portscan() 
		trix.display(r)
