#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.
#

from trix.data.cursor import *
from trix.util.wrap import *

class pq(Wrap):
	"""
	UNDER CONSTRUCTION! EXPERIMENTAL!
	
	Pass a list or dict object. The given object will be wrapped by a
	util Wrap object, so the pq object should behave pretty much like
	the type passed to it, except it carries the operation forward 
	through a chain of calls.
	
	>>> from trix.x.pq import *
	>>> q = pq([1,2,3,4,5])
	
	# use wrapped dict functions to affect the object
	>>> q.append(9)
	
	# use the `o` property to access the object directly
	>>> q.o # [1, 2, 3, 4, 5, 9]
	
	"""
		
	def __init__(self, o):
		"""Pass object `o` to the constructor.""" 
		Wrap.__init__(self, o)
	
	def __call__(self, fn, *a, **k):
		"""
		Return a new pq object containing the result of the given lambda,
		function, or other executable object.
		
		>>> q = pq([1,2,3])
		>>> qr = q(reversed)(list).o
		>>> qr
		[3, 2, 1]
		"""
		return pq(fn(self.o, *a, **k))
	
	
	
	# --- manipulation ---
	
	def each(self, fn, *a, **k):
		"""
		Passes a data Param to executable `fn` for each item.
		
		>>> def test(p):
		...   print(p.i, p.v) # print index, value
		... 
		>>> q = pq([1,2,3])
		>>> q.each(test)
		0 1
		1 2
		2 3
		"""
		c = Cursor(self.o)
		try:
			while True:
				c.fetch()
				fn(c.fetch.param, *a, **k)
		except StopIteration:
			pass
		return self
	
	
	def select(self, fn, *a, **k):
		"""
		Passes a data Param to executable `fn` for each item. Stores a
		list of results and returns that list wrapped as a pq object.
		"""
		c = Cursor(self.o)
		try:
			r = []
			while True:
				c.fetch()
				r.append(fn(c.fetch.param, *a, **k))
		except StopIteration:
			pass
		return pq(r)
	
	
	def update(self, fn, *a, **k):
		"""
		Pass executable object `fn`, which receives a Param object and 
		any args/kwargs passed to this method. The executable must alter
		the received Param (if necessary) and return it.
		>>> from trix.x.pq import *
		>>> q = pq([1,2,3,4,5])
		>>> q.update(lambda p: p.set(p.v*10))
		>>> q.o
		[10, 20, 30, 40, 50]
		"""
		c = Cursor(self.o)
		try:
			while True:
				p = None
				c.fetch()
				p = fn(c.fetch.param, *a, **k)
				self.o[p.i] = p.v
		except StopIteration:
			pass
		except Exception as ex:
			raise type(ex)(xdata(p=p.iv, a=a, k=k))



