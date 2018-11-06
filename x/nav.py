#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.
#

from trix import *
from trix.util.dq import *


class Nav(object):
	"""Navigate through large dict structures."""
	
	def __init__(self, obj):
		"""Pass a dict object."""
		self.o = obj # root object
		self.s = obj # selection, start at root
		self.p = []  # path - starts empty (at root)
		self._f = trix.ncreate("fmt.JCompact")
	
	
	def dq (self, pathlist, *a):
		"""
		Query data at any path.
		
		Pass a list with path elements, or pass each path element as an
		individual argument.
		"""
		return dq(self.o, pathlist, *a)
	
	
	def path(self):
		"""Print the path to the current selection."""
		r = []
		for item in self.p:
			ijson = self._f.format(item)
			r.append(ijson)
		print ("/%s : %s"%('/'.join(r),type(self.dq(self.p)).__name__))
	
	
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
	



