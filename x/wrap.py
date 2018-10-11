#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.
#


from trix import *


class Wrap(object):
	"""Wrap an object."""
	
	def __init__(self, o, **k):
		"""Pass an object, or pass a 'create' or 'ncreate' kwarg."""
		
		self.__obj = o
		self.__dir = {}
		
		# you can specify a set of attributes to wrap using attrs=[...]
		attrs = k.get('attrs', dir(o))
		
		# otherwise, it's all methods and instancemethods
		for n in attrs:
			if not ("__" in n):
				attr = getattr(o, n)
				self.dir[n] = attr
				if type(attr).__name__ in ['method', 'instancemethod']:
					self.dir[n] = attr
	
	def __call__(self, key, *a, **k):
		return self[key](*a, **k)
	
	def __getitem__(self, key):
		return self.dir[key]
	
	@property
	def obj(self):
		return self.__obj
	
	@property
	def dir(self):
		return self.__dir
	
	@property
	def keys(self):
		return self.__dir.keys()
	
	"""
	def _alt_load(self, o):
		attrs = k.get('attrs', dir(o))
		for n in attrs:
			b = (n[:2] == "__" in n) and (n[-2:] == "__")
			if b or not ("__" in n):
				attr = getattr(o, n)
				self.dir[n] = attr
	"""	
	
