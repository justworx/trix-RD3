#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under
# the terms of the GNU Affero General Public License.
#

import unicodedata

from ... import *
from ...util.xiter import *


#
# CHAR-INFO
#
class charinfo(xiter):
	"""Provides extended information for current unicode character."""

	def __init__(self, iterable_text):
		"""Pass unicode text, iter, or generator."""
		xiter.__init__(self, iter(iterable_text))
		self.c = None

	def __next__(self):
		try:
			self.c = xiter.__next__(self)
			return self
		except TypeError:
			raise TypeError(ex.args, xdata(
					itertext=iterable_text, itertype=type(iterable_text)
				))

	def __str__(self):
		return self.c


	#
	# unicodedata
	#
	@property
	def name(self):
		"""Return unicodedata.name."""
		try:
			return unicodedata.name(self.c)
		except:
			return None

	@property
	def decimal(self):
		"""Return unicodedata.decimal."""
		try:
			return unicodedata.decimal(self.c)
		except ValueError:
			return None

	@property
	def digit(self):
		"""Return unicodedata.digit."""
		try:
			return unicodedata.digit(self.c)
		except ValueError:
			return None

	@property
	def numeric(self):
		"""Return unicodedata.numeric."""
		try:
			return unicodedata.numeric(self.c)
		except ValueError:
			return None

	@property
	def category(self):
		"""Return unicodedata.category."""
		return unicodedata.category(self.c)

	@property
	def bidirectional(self):
		"""Return unicodedata.bidirectional."""
		return unicodedata.bidirectional(self.c)

	@property
	def combining(self):
		"""Return unicodedata.combining."""
		return unicodedata.combining(self.c)

	@property
	def east_asian_width(self):
		"""Return unicodedata.east_asian_width."""
		return unicodedata.east_asian_width(self.c)

	@property
	def mirrored(self):
		"""Return unicodedata.mirrored."""
		return unicodedata.mirrored(self.c)

	@property
	def decomposition(self):
		"""Return unicodedata.decomposition."""
		return unicodedata.decomposition(self.c)


	#
	# data.udata
	#
	@property
	def block(self):
		"""Return the name of the block containing this character."""
		return udata.block(self.c)

	@property
	def bracket(self):
		"""Return bracket data."""
		return udata.bracket(self.c)

	@property
	def props(self):
		"""Return properties associated with this character."""
		return udata.properties(self.c)


	# INFO
	def info(self):
		"""Return a dict with all attributes of the current character."""
		result = dict(
			#
			# from unicodedata module
			#
			name             = self.name,
			decimal          = self.decimal,
			digit            = self.digit,
			numeric          = self.numeric,
			category         = self.category,
			bidirectional    = self.bidirectional,
			combining        = self.combining,
			east_asian_width = self.east_asian_width,
			mirrored         = self.mirrored,
			decomposition    = self.decomposition,

			#
			# from trix.data.udata
			#
			block   = self.block,
			bracket = self.bracket,
			props   = self.props,

			#
			c = self.c
		)

		return result


	# DISPLAY
	def display(self, value=None, **k):
		"""Display all info on the current character."""

		if value:
			trix.display(value, **k)

		else:
			#
			# Display is all about development/debugging in this class,
			# so I'm going to go ahead and default "sort_keys".
			#
			k.setdefault('sort_keys', True)

			#
			# EXTRA INFO
			#  - Add some extra info, for visual only.
			#  - This is important (at least to me) so I can understand the
			#    codes for bidiname and catname without looking them up
			#    manually.
			#  - When using the `info` property data while processing a
			#    string, I'll use the code rather than the name... I don't
			#    think it's needed for the dict `info()` returns.
			#
			info = self.info()

			bidiname = udata.propalias().bidi(info['bidirectional'])
			if bidiname:
				info['_bidiname'] = bidiname

			catname = udata.propalias().cat(info['category'])
			if catname:
				info['_catname'] = catname

			#
			# #
			# # WHAT IS LINEBREAK?
			# #  - How do I get this 'linebreak' value?
			# #  - I still haven't seen it in actual practice.
			# #  - Maybe it's nothing to do with parsing text.
			# #  - I'll leave this here for a while, just in case.
			#
			# linebreak = udata.propalias.linebreak(info['linebreak'])
			# if linebreak:
			#   info['linebreakname'] = linebreak
			#

			info['__char__'] = [str(info['c'])]

			trix.display(info, **k)
