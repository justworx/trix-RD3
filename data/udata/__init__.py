#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under
# the terms of the GNU Affero General Public License.
#

from ... import *
from .blocks import BLOCKS
from .brackets import BRACKETPAIRS
from .proplist import PROPERTIES
import struct, bisect



class udata(object):
	
	Cache = 'util.cache.Cache'
	CTime = 30
	CSize = 512
	
	@classmethod
	def cache(cls):
		try:
			return cls.__CACHE
		except:
			cls.__CACHE = trix.ncreate(
					cls.Cache, timeout=cls.CTime, maxsize=cls.CSize
				)
			return cls.__CACHE
	
	#
	# BRACKETS
	#
	@classmethod
	def bracket(cls, c):
		"""
		Tuple with open/close indicator and the bracket matching `c`.
		
		# EXAMPLE:
		>>> udata.bracket('(')
		('o', ')')
		"""
		i = ord(c)
		x = bisect.bisect_left(BRACKETPAIRS, [i])
		try:
			BP = BRACKETPAIRS[x]
			return (BP[2], unichr(BP[1])) if (BP and BP[0]==i) else None
		except IndexError:
			return None
	
	#
	# BLOCKS
	#
	@classmethod
	def block(cls, c):
		"""
		Name of the block containing char `c`.
		
		# EXAMPLE:
		>>> udata.block('c')
		'Basic Latin'
		"""
		i = ord(c)+1
		x = bisect.bisect_left(BLOCKS, [[i]])
		B = BLOCKS[x-1]
		return B[1]
	
	@classmethod
	def blocks(cls):
		"""Dict with block-name keys and range list values."""
		try:
			return cls.__blocks
		except AttributeError:
			cls.__blocks = {}
			for b in BLOCKS:
				cls.__blocks[b[1]] = b[0]
			return cls.__blocks

	@classmethod
	def blocknames(cls):
		"""List of all blocknames."""
		return cls.blocks().keys()
	
	#
	# PROPERTIES
	#
	@classmethod
	def properties(cls, c):
		"""List of all properties of the given char `c`."""
		try:
			return cls.cache().get(c)
		except KeyError:
			r = []
			for k in PropList.keylist():
				if PropList(k).match(c):
					r.append(k)
					cls.cache().set(c, r)
			return r
	
	# PROP-LIST
	@classmethod
	def proplist(cls, *a, **k):
		"""
		PropList object with the given arguments.
		
		EXAMPLES:
		>>> x = udata.proplist('ASCII_Hex_Digit')
		>>> x.match('a')
		True
		
		>>> # the PropList.keylist class method lists available properties
		>>> udata.PropList.keylist()
		"""
		return PropList(*a, **k)
	
	# PROP-ALIAS
	@classmethod
	def propalias(cls):
		"""Return a propalias object."""
		#
		# this should probably be wrapped in with query.py
		#
		try:
			return cls.__propalias
		except AttributeError:
			cls.__propalias=trix.nvalue('data.udata.propalias','propalias')
			return cls.__propalias
	
	#
	# SAFECHR
	#  - Need to test the removal of this. I think the forced definition
	#    (or redefinition) of `unichr` in trix fixes the need for it; if
	#    so, the `unichr(i)`, below is always going to work.
	#
	#@classmethod
	#def safechr(cls, i):
	#	"""
	#	A workaround to prevent ValueError on narrow builds when creating
	#	characters with a codepoint over 0x10000.
	#	"""
	#	try:
	#		return unichr(i)
	#	except ValueError:
	#		return struct.pack('i', i).decode('utf-32')
	#




class PropList(object):
	
	__KEYS = sorted([k for k in PROPERTIES.keys()])
	__ITEMS = [PROPERTIES[k] for k in __KEYS]
	
	@classmethod
	def __item(cls, key):
		"""Private, to protect __ITEMS from manipulation."""
		return cls.__ITEMS[bisect.bisect_left(cls.__KEYS, key)]
	
	@classmethod
	def keylist(cls):
		"""Returns a copy of __KEYS."""
		return cls.__KEYS[:]
	
	@classmethod
	def indexof(cls, key):
		"""Find index of given key."""
		return bisect.bisect_left(cls.__KEYS, key)
	
	# INIT
	def __init__(self, *a, **k):
		"""
		Pass a list of key strings, or keyword items, a list of integers.
		"""
		ii = k.get('items', [])
		for pname in a:
			if not pname in ii:
				ix = self.indexof(pname)
				if ix < 0:
					raise ValueError('udata-propname-invalid', pname)
				ii.append(ix)
		
		self.__items = ii
		if not self.__items:
			raise ValueError('udata-proplist-empty') #base.xdata()
	
	@property
	def items(self):
		"""Return a list (of integers) this object represents."""
		return self.__items
	
	@property
	def keys(self):
		"""Return a list (of strings) this object represents."""
		try:
			return self.__keys
		except:
			kk = []
			for i in self.__items:
				kk.append(self.__KEYS[i])
			self.__keys = kk
			return self.__keys
	
	
	# MATCH
	def match(self, c):
		"""
		Return True if the given unichr matches one of the properties
		this object was created to represent.
		"""

		#
		# NOTE: This method is sometimes slow depending on the number of
		#       comparisons required. Use match() with a PropList object
		#       that has the minimum set of keys that meet your needs.
		#
		x = ord(c)
		isinst = isinstance # 6% faster
		
		# loop through each proplist this object was created to represent
		for listid in self.__items:
			proplist = self.__ITEMS[listid]
			for i in proplist:
				if ((x==i) if isinst(i,int) else x>=i[0] and x<=i[1]): # +1%
					return True
		return False


