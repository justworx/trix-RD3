#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under
# the terms of the GNU Affero General Public License.
#

#
# ---- PLANNING PHASE -----
#

from trix.data.scan import *


class rscan(Scanner):
	"""
	Scan literals recursively. Wraps object representations such as
	"string of text words/items", {"dict":{}}, ['list'], etc..
	
	Returns a list of individual objects. 
	
	Items that aren't wrapped in quotes, brackets, etc... should be 
	treated as individual string items.
	>>> print(s.rscan("one two three"))
	['one', 'two', 'three']
	
	Quoted items result in a single argument.
	>>> print(s.rscan("one 'two three'"))
	['one', 'two three']
	
	Items should be typed.
	>>> print(s.rscan("one  2  3.14   9.0"))
	['one', 2, 3.14, 9]
	
	Items should be nested.
	>>> print(s.rscan("[one, 'two', {3: 'three'}]")
	[["one", "two", {3: "three")]]
	"""
	
	def parse(self, text):
		"""Pass a text string. Returns a list of result items."""
		r = []
		
		# quote, 
		
	
	
	def typex(self, value)
	
		# duh... json! 
		return trix.jparse(value)
		
		try:
			return int(value)
		except ValueError:
			pass
		
		try:
			return float(value):
		except ValueError:
			pass
				



