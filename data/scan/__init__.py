#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under
# the terms of the GNU Affero General Public License.
#

from ..udata.charinfo import *
from ...util.stream.buffer import *


class Scanner(object):
	"""Scan unicode text one character at a time."""
	
	Escape = "\\"
	BufSize = 2048
	
	def __init__(self, iterable_text, **k):
		"""Pass anything iterable that produces unicode characters."""
		self.__escape = k.get('escape', self.Escape)
		self.__bufsz = k.get('bufsz', self.BufSize)
		self.__cinfo = charinfo(iter(iterable_text))
		next(self.__cinfo)
	
	@property
	def c(self):
		"""Return current character info object."""
		return self.__cinfo
	
	@property
	def cc(self):
		"""Move forward one and return the character info object."""
		return self.__cinfo.next()
	
	
	@property
	def bufsz(self):
		return self.__bufsz
	
	@property
	def esc(self):
		return self.__escape
	
	
	#
	# CONVENIENCE METHODS
	#
	
	# SCAN TO
	def scanto(self, c):
		"""Collect all text to the given codepoint `c`."""
		return self.collect(lambda ci: ci.c != c)
	
	
	# PASS WHITE
	def passwhite(self):
		"""Pass any existing white space."""
		self.ignore(lambda ci: ci.space)
	
	
	# PASS LINE-ENDING
	def passend(self):
		"""Pass existing white space, then any endline codepoints."""
		self.passwhite()
		self.ignore(lambda c: c.lineend)
		
	
	#
	# CALLBACK-METHODS
	#  - The following methods require a callback executable to select
	#    which characters to ignore or collect.
	#
	
	# IGNORE
	def ignore(self, fn):
		"""
		Pass all characters for which executable `fn` returns True. The
		iterator is now on the first character following ignored text.
		
		NOTE: If the current character doesn't match what `fn` is looking
		      for, the pointer is not moved.
		"""
		try:
			b = fn(self.c)
			while b:
				b = fn(self.cc)
		except StopIteration:
			pass
	
	
	# COLLECT
	def collect(self, fn):
		"""
		Collect each character that matches the criteria of `fn`. The 
		pointer is left directly after the last matching character.
		"""
		b = Buffer(mode='r', max_size=self.__bufsz)
		w = b.writer()
		try:
			while fn(self.c):
				if self.c.c != self.__escape:
					w.write(self.c.c)
				else:
					w.write(self.c.cc)
				self.cc
		except StopIteration:
			pass
		
		# read/return the whole buffer
		return b.read()
