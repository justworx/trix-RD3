#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.
#

from .xinspect import *


class Wrap(object):
	"""
	Wrap an object.
	
	Wrap is useful when you want to call an object by passing the value
	of its attributes. Pass the text value of a function, method, or
	attribute, along with any args/kwargs where applicable.
	
	>>> w = Wrap(Dir())
	>>> w('path')
	>>> w('cd', '..')
	>>> w('ls')
	
	NOTE:   Wrap won't work with basic, built-in objects such as
	        str, dict, and list.
	"""
	
	def __init__(self, o):
		"""Pass an object or module as the `o` argument."""
		self.__o = o
		self.__i = Inspect(o)
	
	def __call__(self, key, *a, **k):
		"""
		Call any executable object attribute.
		
		>>> w = Wrap(trix.ncreate('fs.dir.Dir'))
		>>> w('ls')
		"""
		if key in self.__i.methods:
			return self.__i.methods[key](*a, **k)
		elif key in self.__i.functions:
			return self.__i.functions[key](*a, **k)
		elif key in self.__i.properties:
			return self.__i.properties[key].fget(self.__o, *a)
		elif key in self.keys:
			return self.attrs[key]
		else:
			raise KeyError("Executable Not found: %s" % key)
	
	@property
	def o(self):
		return self.__o
	
	@property
	def i(self):
		return self.__i
		
	@property
	def keys(self):
		try:
			return self.__keys
		except:
			self.__keys = []
			for a in self.attrs:
				if not ("__" in a):
					attr = getattr(self.__o, a)
					self.__keys.append(a)
			return self.__keys
	
	@property
	def attrs(self):
		try:
			return self.__attrs
		except:
			self.__attrs = dir(self.__o)
			return self.__attrs
