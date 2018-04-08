#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.
#


from .. import *


class Bag(object):
	"""A count of items by name."""
	
	def __init__(self, T):
		"""Pass the type of object this bag holds."""
		try:
			self.__d = Bag.defaultdict(T)
		except:
			Bag.defaultdict = trix.value("collections.defaultdict")
			self.__d = Bag.defaultdict(T)
			
	
	def __getitem__(self, key):
		return self.__d[key]
	
	def __setitem__(self, key, value):
		self.__d[key] = value

	
	@property
	def dict(self):
		return dict(self.__d)
	
	def put(self, key, value):
		self.__d[key] = value
	
	def get(self, key):
		return self.__d[key]
	
	def add(self, key, x):
		try:
			self.__d[key] += x
		except KeyError:
			self.__d[key] = x
