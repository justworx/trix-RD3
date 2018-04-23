#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under 
# the terms of the GNU Affero General Public License.
#

from . import *


class test(cline):
	"""
	Run basic compilation test.
	
	Loads all modules and prints a report listing modules and a brief
	error message, if any.
	"""
	def __init__(self):
		print ("Scanning local ports...")
		trix.ncreate('app.test.report')
	
