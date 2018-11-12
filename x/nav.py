#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.
#


from trix import *
from trix.util.dq import *
from trix.util.xiter import *


"""
#
# THIS FAILS - HERE FOR DEBUGGING
#
python3

d = {
	"abc" : "abcdefg!",                   #test scalar first
	"li"  : [1, 2, {"bucklemy": "shoe"}], #test list, dict-in-list
}

from trix.x.nav import * 
n = Nav(d)
g = iter(n.navgen())

x = next(g)
x.path()
"""		


class xnaviter(xiter):
	"""Recursive dict/list iterator."""
	
	def __init__(self, nav):
		"""Pass the nav object."""
		
		xiter.__init__(self, nav)
		pass
		# omg i'm so lost
		#  - xnaviter must return some kind of node - I'd thought the 
		#    Nav object itself, on its current selection; that may be
		#    right...
		#  - charinfo was easy because it iterated through a simple list
		#    of characters (that is, a string) and wrapped each char in
		#    itself to provide access to methods related to that char.
		#  - i'd thought that xnaviter could return itself as charinfo
		#    does, but now it seems that - because of the various ways
		#    paths can be followed - it must also, somehow, handle the
		#    direction of iteration: horizontally (rightward) to the leaf 
		#    of each dict/list node, or vertically (downward).
		#  * Well in the current case, it's definitely horizontal
		#    navigation I'm interested in. The iterator must return only
		#    scalar values (wrapped in a nav node, of course) starting
		#    with the first/top, continuing through any scalars (and
		#    following any non-scalar items rightward... and backing out
		#    one level at a time, drilling into non-scalar nodes... rinse
		#    and repeat... 
		#  * Maybe it's that each node returns Nav.. check `scalar` if
		#    the leaf is what you want, but still have access to the 
		#    whole deal...
		#  ! Well, that's a place to start. Let's see what happens.
		#
	
	

class Nav(object):
	"""Navigate through large dict structures."""
	
	def __init__(self, obj):
		"""Pass a dict object."""
		self.o = obj # root object
		self.s = obj # selection, start at root
		self.p = []  # path - starts empty (at root)
		self._f = trix.ncreate("fmt.JCompact")
	
	
	def __iter__(self):
		try:
			return iter(self.s.keys())
		except:
			return range(0, len(self.s))
	
	def __next__(self):
		return self
	
	
	def navgen(self):
		# yield self on current self.s
		yield (self)            
		
		# loop through self.s keys, yielding the items
		while True:
			print ("#", ki) # key/int offsets for dict/list
			
			try:
				# select/jield the next key
				
				#
				# This throws an error when moving inward to the contained
				# dict or list. For dict, the key `ki` probably doesn't exist
				# here, and even if it did, we're still iterating through the
				# containing dict, which thows everything off.
				#
				# I'll need to come up with something really spectacular to 
				# pull this one off :-/
				#
				self.select(ki)
				
				
				print ("#", ki)
				
				yield (self)
			
			except StopIteration:
				# once a leaf node is reached, 
				self.back()
				
		
	
	
	@property
	def scalar(self):
		return is_scalar(self.s)
	
	@property
	def kk(self):
		"""Return list of keys."""
		return list(self.keys())
	
	
	def dq (self, pathlist, *a):
		"""
		Query data at any path.
		
		Pass a list with path elements, or pass each path element as an
		individual argument.
		"""
		return dq(self.o, pathlist, *a)
	
	
	def keys(self):
		"""Returns current selection keys."""
		return self.s.keys()
	
	
	# --- selection ---
	
	def select(self, *keys):
		"""Select a new object from current dict keys."""
		p = self.p
		s = self.s
		for key in keys:
			try:
				self.s = self.s[key]
				self.p.append(key)
				return self.p
			except:
				self.p = p
				self.s = s
				raise
	
	def back(self):
		"""Navigate back to the current object's parent."""
		self.p.pop()
		self.s = self.dq(self.p)
		return self.p
	
	def top(self):
		"""Set selection to root object."""
		self.s = self.o
	
	
	# ---- info/display -----
	
	def display(self):
		"""Print the path to the current selection."""
		r = []
		for item in self.p:
			ijson = self._f.format(item)
			r.append(ijson)
		print ("/%s : %s"%('/'.join(r),type(self.dq(self.p)).__name__))
	










def is_scalar(x):
	"""Return true if `x` is scalar (including strings)."""
	if isinstance(x, basestring):
		return True
	try:
		iter(x)
		return False
	except TypeError:
		return True

