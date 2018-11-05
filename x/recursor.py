#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under 
# the terms of the GNU Affero General Public License.
#


class recursor(object):
	"""Recursively step through dict or list objects."""
	
	def __init__(self, obj, **k):
		"""Pass a dict or list object."""

		self.__o = obj
	
	
	
	def keys(self)
		"""
		Returns dictkeys if obj is dict, else a range of list item
		offsets.
		"""
		try:
			return self.__o.keys()
		except:
			pass
		
		try:
			return range(0, len(self.__o)
		except:
			pass
		
		raise ValueError("Obj must be list- or dict-like.")
	
	
	def gen(self):
		for x in self.keys():
			yield [x, self.__o[x]]
			
			#
			# NO... this isn't what needs to be yielded... an object with
			# all the relevant data, methods, and properties must be 
			# yielded... something like xiter would do.
			#

