#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under
# the terms of the GNU Affero General Public License.
#

from .charinfo import *


def scanner(iterable_text):
	"""Return a scanner object."""
	return Scanner(iterable_text)


#
# SCANNER
#
class Scanner(object):
	"""Scan unicode text one character at a time."""

	def __init__(self, iterable_text):
		"""Pass anything iterable that produces unicode characters."""
		self.current = charinfo(iter(iterable_text))
		self.__parts = []

	@property
	def c(self):
		"""Return current character data."""
		return self.current

	@property
	def cc(self):
		"""Move forward one and return the character data."""
		return self.current.next()

	#
	# SCAN
	#  - I'm thining something like this;
	#    haven't worked it out yet...
	#
	"""
	def scan(self):
		literal = []
		structure = []
		for c in self.cc:
			if c.bracket:
				bracket = c
				if c.bracket[0] == 'o':
					r.append(self.scan())
				elif c.bracket[0] == 'c':
					return r

			#elif: ...
			#  do something...
			#  return it...

			else:
				literal.append(c)
				return ''.join(literal)
	"""
