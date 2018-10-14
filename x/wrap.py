#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.
#


from trix import *
import inspect


class Wrap(object):
	"""Wrap an object."""
	
	def __init__(self, o, **k):
		"""Pass an object."""
		
		self.__obj = o
		self.__dir = {}
		self.__key = []
		self.__err = []
		self.more = {}
		
		# you can specify a set of attributes to wrap using attrs=[...]
		attrs = k.get('attrs', dir(o))
		
		# otherwise, it's all methods and instancemethods
		for n in attrs:
			#if not ("__" in n):
			try:
				attr = getattr(o, n)
				self.__dir[n] = attr
				self.__key.append(n)
				
				self.more[n] = {'type':type(attr)}
			except:
				self.__err.append(xdata(attr=n))
	
	
	def __call__(self, key, *a, **k):
		"""
		Call any executable object attribute.
		
		>>> w = Wrap(trix.ncreate('fs.dir.Dir'))
		>>> w('ls')
		"""
		return self.__dir[key](*a, **k)
	
	
	def __getitem__(self, key):
		"""
		Returns an attribute.
		
		>>> w = Wrap(trix.ncreate('fs.dir.Dir'))
		>>> w['ls']
		"""
		return self.__dir[key]
	
	@property
	def obj(self):
		return self.__obj
	
	@property
	def dir(self):
		return self.__dir
	
	@property
	def keys(self):
		return self.__key
	
	@property
	def errs(self):
		return self.__err

