#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.
#


from trix import *


class Wrap(object):
	"""Wrap an object."""
	
	@classmethod
	def create(cls, path, *a, **k):
		return cls(trix.create(path, *a, **k))
	
	@classmethod
	def ncreate(cls, innerPath, *a, **k):
		return cls(trix.ncreate(innerPath, *a, **k))
	
	def __init__(self, o, **k):
		"""Pass an object, or pass a 'create' or 'ncreate' kwarg."""
		
		self.__obj = o
		self.__dir = {}
		
		attrs = k.get('attrs', dir(o))
		for n in attrs:
			if not ("__" in n):
				attr = getattr(o, n)
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
	
