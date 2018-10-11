#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.
#

class SockError(OSError):
	"""Exceptions thrown from `trix.util.sock`."""
	
	# args = (errno, strerror[, filename[, winerror[, filename2]]]
	def __init__(self, *a, **k):
		"""Wraps OS Error, with more detail from SockWrap methods."""
		
		OSError.__init__(self, *a)
		
		self.__krgs = k
		self.__args = list(a)
		self.__args.append(k)
	
	@property
	def info(self):
		return self.__krgs

