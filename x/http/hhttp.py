#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under 
# the terms of the GNU Affero General Public License.
#

from time import gmtime, strftime
from trix.net.handler import *
from trix.x.http.httpreq import *
from trix.util import text

HHTTP_NCONFIG = 'x.http.hhttp.conf'


#
# HANDLE-HTTP
#
class HandleHttp(Handler):
	"""
	Replies with the default HTTP content handler - a message about 
	this class and how to customize it to suit your needs.
	"""
	
	__CONFIG = None
	
	# INIT
	def __init__(self, sock, **k):
		
		#
		# Connection should be flexible. I want 'keep-alive' to be an
		# option for javascript apps.
		#
		k.setdefault('Connection', 'close')
		k.setdefault('Server', 'trix/%s' % str(VERSION))
		k.setdefault('docroot', trix.innerfpath("x/content/"))
		
		#
		# YIKES...
		#  - This can't be set like this...
		#    The whole class needs to be reorganized.
		#  - need some mime action in here.
		#
		k.setdefault('Content-Type', 'text/html')
		
		self.__options = trix.kcopy(k, 'Connection Server Content-Type')
		self.__docroot = k.get('docroot')
		
		Handler.__init__(self, sock, **k)
	
	@property
	def config(self):
		try:
			return self.__CONFIG
		except:
			self.__CONFIG = trix.nconfig(HHTTP_NCONFIG)
			return self.__CONFIG
	
	@property
	def docroot(self):
		"""The root directory from which content may be read."""
		return self.__docroot	
	
	@property
	def options(self):
		"""Options passed to constructor (with some defaults)."""
		return self.__options	
	
	#
	# HANDLE DATA
	#
	def handledata(self, data):
		"""Echo request."""
		with thread.allocate_lock():
			try:
				head = ""
				
				# parse the http request
				req = httpreq(data)
				
				# Generate Content before headers (because length!)
				content = self.reply(req)
				clength = len(content)
				
				# Generate Headers
				gmt = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
				head = "\r\n".join([
					"HTTP/1.1 200 OK", 
					"Date: %s"           % (gmt),
					"Connection: %s"     % (self.__options['Connection']),
					"Server: %s"         % (self.__options['Server']),
					"Accept-Ranges: bytes",
					"Content-Type: %s"   % self.__options['Content-Type'],
					"Content-Length: %i" % (clength),
					"Last-Modified: %s"  % (gmt)
				])
				
				# Send content reply
				content = text.Text("%s\r\n\r\n%s" % (head, content))
				self.socket.send(content.bytes)
			
			except BaseException as ex:
				#
				# TO DO:
				#  - Move this to its own method
				#  - Use correct error codes
				#
				self.socket.send(b"%s\r\n\r\n" % (head.encode()))
				self.socket.send(b"<html><head>\r\n")
				self.socket.send(b'<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />\r\n')
				self.socket.send(b"<title>Error</title>\r\n")
				self.socket.send(b"<head><body>\r\n")
				self.socket.send(b"<h1>500 Internal Server Error</h1>\r\n")
				self.socket.send(b"<pre>\r\n")
				self.socket.send(type(ex).__name__.encode('utf_8'))
				self.socket.send(trix.formatter(xdata()).encode('utf_8'))
				self.socket.send(b": %s\r\n" % bytes(str(ex), 'utf_8'))
				self.socket.send(b"</pre>\r\n</body></html>\r\n\r\n")
				raise type(ex)(ex.args, xdata())
	
	
	#
	# FULL PATH
	#
	def fullpath(self, req):
		"""Return the full path to the requested file."""
		p = trix.path(self.docroot)
		if p.isfile():
			#print(self.docroot, 'is a file?')
			return p
		elif req.reqpath:
			#print(self.docroot,"+",self.reqpath,'=',p(self.reqpath).path,'?')
			p = p(req.reqpath) #merge
		return p
	
	
	#
	# FILE BYTES
	#
	def filebytes(self, req):
		"""Return contents of a file from self.docroot, or None."""
		docroot=self.docroot
		if not docroot:
			return None
		
		reqpath=req.reqpath
		try:
			p = trix.path(docroot)
			if p.isfile:
				return None
			
			elif reqpath:
				p = p(reqpath) #merge
				if p.isdir:
					indexfiles = ['index.html', 'index.htm']
					for idx in indexfiles:
						f = p.merge(idx)
						if f.exists:
							return f.reader(mode='rb').read()
		except Exception:
			raise Exception(xdata(docroot=docroot, reqpath=reqpath))
	
	
	#
	# REPLY - The response text
	#
	def reply(self, req):
		b = self.filebytes(req)
		if b:
			return tx.Text(b)
		else:
			return self.default_reply(req)
		
	
	def default_reply(self, req):
		
		# calculate full path (for display, below)
		p = self.fullpath(req)
		fullpath = p.path if p else ''
		
		content = self.__CONFIG['hhttp_default_content'] % (
				HandleHttp.__module__, HandleHttp.__name__, 
				"\r\n".join(req.lines),
				self.docroot, fullpath
			)
		
		return content


