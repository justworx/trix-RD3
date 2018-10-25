#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under
# the terms of the GNU Affero General Public License.
#

class Counter(object):
	"""Count things."""
	
	def __init__(self, id=None):
		self.__id = id
		self.clear()
	
	@property
	def id(self):
		return self.__id
	
	@property
	def counts(self):
		return self.__counts
	
	def clear(self):
		self.__counts = {}
	
	def feed(self, x):
		try:
			self.__counts[x] += 1
		except KeyError:
			self.__counts[x] = 1

