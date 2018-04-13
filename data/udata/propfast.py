#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under
# the terms of the GNU Affero General Public License.
#

from . import *


#
# PROPFAST
#  - Fast property lookups.
#
class propfast(object):
	"""Fast codepoint property lookup."""
	
	Keys = sorted([k for k in PROPERTIES.keys()])
	
	
	@property
	def blocks(self):
		"""The data for all blocks/properties."""
		return self.__fblocks
	
	
	def display(self, **k):
		"""Display query results in a fmt.Grid."""
		# loop through block names
		for blockname in sorted(self.__fblocks.keys()):
			
			# Print block name in all-caps
			print ("\n\n#\n# %s\n#" % (blockname.upper()))
			
			# loop for prop list
			bp = []
			for propname in self.__fblocks[blockname]:
				for items in self.__fblocks[blockname][propname]:
					bp.append([propname, ":", items])
			
			# show it in a grid
			if bp:
				trix.display(bp, fmt='fmt.Grid', **k)
		
	
	
	def get(self, c):
		"""Loop through each property list for `c` property matches."""
		
		# result storage
		rr = []
		
		# find the block that contains the given codepoint
		cblock = udata.block(c)
		
		# store the dict of all blocks/properties locally (for speed)
		FB = self.__fblocks
		
		# store the dict `bprops` locally (for speed)
		bprops = FB[cblock]
		
		# gotta use int, not chr
		x = ord(c)
		
		# localize callables for speed improvement
		isinst = isinstance
		
		# loop through proplists; collect matching properties in `rr`
		for propname in self.Keys:
			try:
				proplist = bprops[propname]
				for i in proplist:
					if ((x==i) if isinst(i,int) else x>=i[0] and x<=i[1]):
						rr.append(propname)
			except KeyError:
				pass
		return rr
	
	
	
	
	#
	# GEN
	#
	@classmethod
	def gblocks(cls):
		"""Block name generator."""
		for b in udata.blocknames():
			yield (b)
	
	
	
	
	#
	# INDEXING
	#

	def __init__(self):
		"""Build the index."""
		self.__fblocks = {}
		self.__addblocks()
		self.__addprops()
	
	
	
	def __addblocks(self):
		for block in self.gblocks():
			self.__fblocks[block] = {}
	
	
	
	def __addprops(self):
		
		for block in self.__fblocks.keys():
			
			# get the range for this block
			br = udata.blocks()[block]
			brange = range(br[0],br[1]+1)
			
			#
			# Loop through each property name; add a custom property list
			# just for this particular block.
			#
			for propname in self.Keys: #PROPERTIES.keys():
				self.__fblocks[block][propname] = []
				proplist = PROPERTIES[propname]
				for prop in proplist:
					try:
						p1 = prop[0]
						pn = prop[1]
						if (p1 in brange) and (pn in brange):
							self.__fblocks[block][propname].append(prop)
					except:
						if prop in brange:
							self.__fblocks[block][propname].append(prop)
				
				# don't hang on to empty property sets
				if not self.__fblocks[block][propname]:
					del(self.__fblocks[block][propname])
	


