#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under
# the terms of the GNU Affero General Public License.
#

from .charinfo import *
from ...util.stream.buffer import *

def scanner(iterable_text):
	"""Return a scanner object."""
	return Scanner(iterable_text)


#
# SCANNER
#
class Scanner(object):
	"""Scan unicode text one character at a time."""
	
	Escape = '\\'
	BufSize = 2048
	
	def __init__(self, iterable_text):
		"""Pass anything iterable that produces unicode characters."""
		self.current = charinfo(iter(iterable_text))
		self.__parts = []

	@property
	def c(self):
		"""Return current character info object."""
		return self.current

	@property
	def cc(self):
		"""Move forward one and return the character info object."""
		return self.current.next()
		
	
	#
	# SCAN
	#  - I'm thinking something like this;
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
	
	def scanto(self, c, **k):
		"""Scan to the next occurance of character `c`."""
		k.setdefault('max_size', self.BufSize)
		b = Buffer(mode='r', **k)
		w = b.writer()
		while self.cc.c != c:
			if c != self.Escape:
				# write the character
				w.write(self.c.c) 
			else:
				# skip escape char; write the next char
				w.escape_char(self.cc.c)
		
		return b.read()
	
	
	def escape_char(self, c):
		#
		# Encountering escape char should send us here, where escape 
		# sequences can be overridden by subclasses.
		#
		return c
