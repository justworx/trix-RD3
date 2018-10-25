#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.
#

from .bag import *
from ..data.udata import *
from ..util.encoded import *

class encdet(Encoded):
	"""Try to detect encoding based on statistics. SLOW. UNRELIABLE."""
	
	#
	# INIT
	#
	def __init__(self, bytestr):
		self.__errors = {}
		self.__bytestr = bytestr
		self.__testlist()
	
	
	def __iter__(self):
		return iter(self.__result)
	
	
	def __getitem__(self, key):
		return self.__result[key]
	
	
	@classmethod
	def encgen(cls):
		LL = list(ENCODINGS)
		for L in LL:
			if L not in ENCODINGS_W_BOM:
				yield L
	
	
	@property
	def bytes(self):
		return self.__bytestr
	
	
	@property
	def result(self):
		return self.__result
	
	
	def errors(self):
		trix.display(self.__errors)
	
	
	def display(self, value=None, **k):
		trix.display(value or self.__result, **k)
		
	
	
	def __testlist(self):
		
		# store each encoding's result
		self.__result = d = {}
		
		# loop through each encoding that does not contain a BOM
		for enc in iter(self.encgen()):
			try:
				# decode self.bytes by the given encoding
				text = self.bytes.decode(enc)
				
				# if that does not error, get the length...
				tlen = len(text)
				
				# fill the bags
				charct = Bag(int)
				blockct = Bag(int)
				for u in text:
					charct.add(u, 1)
					blockct.add(block(u), 1)
				
				#
				d[enc] = dict(
						tex=text[:45]+"...", blockct=len(blockct.dict),
						sz=tlen, counts=charct.dict, blocks=blockct.dict
					)
			except Exception as ex:
				#raise
				self.__errors[enc] = dict(err=str(ex), args=ex.args)
	
	
	
	def __codepointct(self, text):
		
		# count the instances of each codepoint
		d = {}
		for u in text:
			try:
				d[u] = d[u] + 1
			except KeyError:
				d[u] = 1
		
		"""
		# sort the values by count, descending
		dc = {}
		for k in d:
			try:
				dc[d[k]] = dc[d[k]] + k
			except:
				dc[d[k]] = k
		
		return dc
		"""
		return d
