#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.
#


from .. import *


class Chain(object):
	"""Holds a value; provides methods to manipulate that value."""
	
	def __init__(self, v=None):
		self.v = v
	
	def __call__(self, *a):
		"""Return a new Chain (or Param) object with given arguments."""
		return type(self)(*a)
	
	def proc(self, fn, *a, **k):
		"""
		Set this object's self.v to the result of the callable argument
		`fn`. All args and kwargs are passed on to the callable. Use this 
		when you want to set self.v to the callable's result.
		"""
		self.v = fn(*a, **k)
		return self
	
	def pad(self, mlen, val=''):
		"""
		Pad a sequence with `val` items to a minimum length of `mlen`.
		""" 
		val = val if len(str(val)) else ' '
		while len(self.v) < mlen:
			self.v.append(val)
		return self
		
	def set(self, v):
		self.v = v
		return self
	
	def setx(self, x, v):
		self.v[x] = v
		return self
	
	def split(self, *a, **k):
		"""
		Split this value by the string given as the first argument, or
		by the default, if no arguments are given. Keyword args will be
		applied to the str.split() method.
		"""
		self.v = self.v.split(*a, **k)
		return self
	
	def join(self, c, *a, **k):
		"""
		Join list items by character `c`. If no additional arguments are
		given, all items in list `self.v` are joined. If additional args
		are given, they must be integers that give offsets from self.v to 
		join.
		
		NOTE: All list values are cast as unicode before being joined.
		"""
		x = self.v
		u = unicode
		vv =  [u(x[i], **k) for i in a] if a else [u(v, **k) for v in x]
		self.v = u(c, **k).join(vv)
		return self




#
# PARAM
#
class Param(Chain):
	"""
	Param methods manipulate or evaluate data; usually the self.v value
	is involved. All methods work with either self.v, or in some cases,
	an optional second argument to use instead of self.v.
	
	Comparison methods eq, neq, gt, ge, lt, and le all require one
	argument and accept an optional second argument (which defaults to
	self.v).
	
	Methods inherrited from Chain always return `self`, so that calls 
	can be chained through a lambda, whereas Param methods typically, 
	if not always, return value resulting from the method. It may take
	a while to what you're getting back as you chain calls together, 
	but once you get it, it's a powerful tool for use in lambdas.
	"""
	def __init__(self, v=None, i=None):
		self.v = v
		self.i = i
	
	def __getitem__(self, key):
		return self.v[key]
	
	def __str__(self):
		return str(self.v)
	
	def __unicode__(self):
		try:
			return unicode(self.v)
		except:
			return self.v.decode(DEF_ENCODE)
	
	@property
	def iv(self):
		return (self.i, self.v)
	
	@property
	def vi(self):
		return (self.v, self.i)
	
	@property
	def type(self):
		"""Return the type of the current value."""
		return type(self.v)
	
	@property
	def len(self):
		"""Return the length of the current value."""
		return len(self.v)
	
	@property
	def re(self):
		try:
			return self.__re
		except:
			self.__re = __import__('re')
			return self.__re
	
	# COMPARISON
	def eq(self, v, *a):
		"""
		Comparison: Return True if comparison value `v` == self.v; if an  
		optional second argument is given, compares to that instead.
		"""
		return v == (a[0] if a else self.v)
	
	def ge(self, v, *a):
		"""Comparison: greater than/equal to;"""
		return v >= (a[0] if a else self.v)
	
	def gt(self, v, *a):
		"""Comparison: greater than;"""
		return v > (a[0] if a else self.v)
	
	def le(self, v, *a):
		"""Comparison: less than/equal to;"""
		return v <= (a[0] if a else self.v)
	
	def lt(self, v, *a):
		"""Comparison: less than;"""
		return v < (a[0] if a else self.v)
	
	@property
	def true(self):
		return True
	
	@property
	def false(self):
		return False
	
	
	
	def fn(self, fn, *a, **k):
		"""
		Return the result of the callable argument `fn`. All args and 
		kwargs are passed on to the callable. Use this when you want to 
		return a function result rather than setting self.v to the result.
		"""
		return fn(*a, **k)
	
	
	def merge(self, x, b):
		try:
			x.extend(b)
		except:
			x.append(b)
		return x
