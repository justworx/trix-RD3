#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.
#

import fnmatch


class xmatch(object):
	def __init__(self, pattern):
		self.pattern = pattern
	
	def __call__(self, obj):
		self.match(obj)
	
	@classmethod
	def match(cls, obj, pattern=None):
		pattern = pattern or self.pattern
		try:
			# string
			return fnmatch.fnmatch(obj, pattern)
		except:
			pass
		
		try:
			# list
			r = []
			for item in obj:
				if fnmatch.fnmatch(item, pattern):
					r.append(item)
			return r
		except:
			pass
		
		try:
			# dict key
			r = {}
			for k in obj:
				if fnmatch.fnmatch(k, pattern):
					r[k] = obj[k]
			return r
		except:
			pass
		
		return None

