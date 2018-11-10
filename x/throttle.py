#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.
#


from trix import *


class Throttle(object):
	"""A generic throttle mechanism."""
	
	def __init__(self, **k): 
		self.__textlen = k.get("textlen", 256)
		self.__maxlen  = k.get("maxlen", 512)
		
	
	def feed(self, data):
		try:
			return self.__feed(data)
		except AttributeError:
			
			# The feeder has not yet been created, so create it
			self.__ftype = type(data)
			
			try:
				c = trix.ncreate('trix.data.cursor.Cursor', data)

	
#
# i can't think. one more file in the "can't think" pile.
# hopefully my brain will come back soon.
#
