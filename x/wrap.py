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
	
	Wrap defines only __init__, __getattr__, and __call__ methods. All
	public methods of the wrapped object are available to be called by
	passing the string name of a wrapped object's property, method, or
	attribute.
	
	>>> w = Wrap(Dir())
	>>> w('path')
	>>> w('cd', '..')
	>>> w('ls')
	
	Wrap's __getattr__ method makes all the methods of the wrapped
	object available to be called directly as though they were methods
	of the Wrap object itself, too.
	
	>>> w = Wrap([1,2,3])
	>>> w.append(4)
	>>> w.o               # [1, 2, 3, 4]
	"""
	
	def __init__(self, o):
		"""Pass an object or module as the `o` argument."""
		
		# store object and inspector
		self.o = o
		self.i = Inspect(o)
		
		# store keys and attributes
		self.__keys = []
		self.__attrs = dir(self.o)
		for a in self.__attrs:
			if not ("__" in a):
				attr = getattr(self.o, a)
				self.__keys.append(a)
	
	def __call__(self, key, *a, **k):
		"""
		Call any executable object attribute.
		
		>>> w = Wrap(trix.ncreate('fs.dir.Dir'))
		>>> w('ls')
		"""
		if key in self.i.methods:
			return self.i.methods[key](*a, **k)
		elif key in self.i.functions:
			return self.i.functions[key](*a, **k)
		elif key in self.i.properties:
			return self.i.properties[key].fget(self.o, *a)
		elif key in self.__keys:
			"""
			print (key)
			print (self.__attrs)
			print (self.__attrs.index(key))
			"""
			return getattr(self.o, key)
			return self.__attrs[self.__attrs.indexof(key)]
		else:
			raise KeyError(key)
	
	
	def __getattr__(self, name):
		return getattr(self.o, name)

