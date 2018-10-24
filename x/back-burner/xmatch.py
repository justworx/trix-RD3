#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.
#

import fnmatch


class xmatch(object):
	"""Like fnmatch, but works on list items and dict keys, too."""
	
	@classmethod
	def match(cls, obj, pattern, search=None):
		# list
		try:
			r = []
			for item in obj:
				if fnmatch.fnmatch(item, pattern):
					r.append(item)
			return r
		except:
			pass
		
		# dict
		try:
			r = {}
			if search=='key':
				for k in obj:
					if fnmatch.fnmatch(k, pattern):
						r[k] = obj[k]
			elif search='value':
				for k in obj:
					if fnmatch.fnmatch(obj, pattern):
						r[k] = obj[k]
			else:
				for k in obj:
					if fnmatch.fnmatch(obj, key):
						r[k] = obj[k]
					elif fnmatch.fnmatch(obj, pattern):
			return r
		except:
			pass
		
		# string
		try:
			return fnmatch.fnmatch(obj, pattern)
		except:
			return fnmatch.fnmatch(str(obj), pattern)
		
		return None
	
	
	def __init__(self, pattern):
		self.pattern = pattern
	
	def __call__(self, obj):
		self.match(self.pattern, obj, search=None)

