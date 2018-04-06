#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.
#

from .. import * # trix

# Compensate for renamed symbols in python 3:
#  - MessageMerge is MM2 in python2, MM3 in python3.
#  - Never use MM2 or MM3 directly - use MessageMerge so it will work
#    in both 2 and 3.

class MM2(object):
	@classmethod
	def contenttype(cls, i): return i.gettype();
	@classmethod
	def maintype(cls, i): return i.getmaintype();
	@classmethod
	def subtype(cls, i): return i.getsubtype();
	@classmethod
	def param(cls, i, pname): return i.get(pname)#.getparam(pname)

class MM3(object):
	@classmethod
	def contenttype(cls, i): return i.get_content_type(); 
	@classmethod
	def maintype(cls, i): return i.get_content_maintype();
	@classmethod
	def subtype(cls, i): return i.get_content_subtype();
	@classmethod
	def param(cls, i, pname): return i.get_param(pname)


#  - urlreq is 'urllib2' in python2, urllib.request in python3

try:
	import urllib2 as urlreq
	MessageMerge = MM2

except:
	import urllib.request as urlreq
	MessageMerge = MM3



def parse(url, **k):
	"""Parse url and return urlinfo object."""
	try:
		return trix.ncreate('util.urlinfo.urlinfo', url, **k)
	except:
		from . import urlinfo
		return urlinfo.urlinfo(url, **k)


#
# FUNCTIONS
#

def open(url, *a, **k):
	"""
	Returns a UResponse object for the given url. Arguments are the 
	same as for urllib's urlopen() function.
	
	from net import url
	r = url.open(someUrl)
	"""
	return UResponse(url, *a, **k)


def head(url):
	"""
	Returns a UResponse with just the head for the given url.
	
	from net import url
	h = url.head(someUrl)
	print (h.info())
	"""
	request = urlreq.Request(url)
	request.get_method = lambda : 'HEAD'
	return UResponse(request)




#
# URL - DOWNLOAD
#

class UResponse(object):
	"""Response object for the url.open() function."""
	
	PMessage = None
	
	def __init__(self, *a, **k):
		self.__file = urlreq.urlopen(*a, **k)
	
	def __len__(self):
		return len(self.content) if self.__content else None
	
	
	def display(self):
		"""Print r.info()"""
		print (str(self.info()))
			
		
	def geturl(self):
		"""The actual URL of the resource retrieved."""
		return self.__file.geturl()
	
	def getcode(self):
		"""Response code."""
		return self.__file.getcode()
	
	def info(self):
		"""Message objects, as returned by python's urlopen()."""
		try:
			return self.__info
		except:
			self.__info = self.__file.info()
			return self.__info
	
	# INFO
	def param(self, name):
		"""Param, as from the info Message object."""
		return MessageMerge.param(self.info(), name)
	
	@property
	def content(self):
		"""Reads and holds the content until self is deleted."""
		try:
			return self.__content
		except:
			self.__content = self.__file.read()
			return self.__content
	
	@property
	def contenttype(self):
		"""The content type, as given by 'info'."""
		return MessageMerge.contenttype(self.info())

	@property
	def maintype(self):
		"""The main type, as given by 'info'."""
		return MessageMerge.maintype(self.info())

	@property
	def subtype(self):
		"""The sub-type, as given by 'info'."""
		return MessageMerge.subtype(self.info())
	
	@property
	def charset(self):
		"""
		Returns the specified charset as detected from BOM, in HTTP 
		headers, or a content specification (eg, meta tag) - in that
		order.
		"""
		try:
			return self.__charset
		except:
			e = trix.ncreate('util.encoded.Encoded', self.content)
			c = e.testbom()
			if not c:
				c = self.param('charset')
			if not c:
				bb = trix.ncreate('util.encoded.Encoded', self.content)
				c = bb.detect()
			self.__charset = e.pythonize(c)
			return self.__charset


