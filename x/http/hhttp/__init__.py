#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under 
# the terms of the GNU Affero General Public License.
#

from time import gmtime, strftime
from trix.net.handler import *
from trix.x.http.httpreq import *
from trix.util import urlinfo, mime

HHTTP_NDEFAULTS = 'x.http.hhttp.conf'


#
# HANDLE-HTTP
#
class HandleHttp(Handler):
	"""
	Replies with the default HTTP content handler - a message about 
	this class and how to customize it to suit your needs.
	"""
	
	# INIT
	def __init__(self, sock, **k):
		Handler.__init__(self, sock, **k)
		
		# path to the example content files
		exampleDir = trix.innerfpath("x/http/hhttp/example/") #<-- PATH!
		
		# webroot is an fs.Path object
		self.webroot = trix.path(exampleDir)
	
	
	#
	# HANDLE DATA
	#
	def handledata(self, data, **k):
		
		try:
			#1 Parse Headers
			self.request = httpreq(data)
			
			#2 Parse URL
			self.uinfo = urlinfo.urlinfo(self.request.reqpath)
			self.uquery = self.uinfo.query
			self.reqpath = trix.path(self.uinfo.path) # keep this Path
			
			trix.display(dict(uinfo=self.uinfo, uquery=self.uinfo.query,
				reqpath=self.reqpath.path))
			
			#3 Check file path - apply default 'index.html' if necessary
			if self.webroot.isdir():
				filepath = self.webroot.merge('index.html')
			else:
				filepath = self.webroot.merge(self.reqinfo.path)
			
			print ('handledata - filepath', filepath)
			
			#4 Check mime type
			self.contentType = mime.Mime(filepath).mimetype
			
			print ('handledata - contentType', self.contentType)
			
			#5 Load File Content
			content = trix.path(filepath).reader(encoding='utf8').read()
			print ('handledata - content', content)
			
			#6 Generate Headers
			clength = len(content.encode('utf_8'))
			
			self.Server = 'trix/%s' % str(VERSION)
			self.Connection = 'keep-alive'
			
			#7 Write the response header and
			gmt = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
			head = self.head('200', clength)
			"""
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
			"""
			
			#7 Send End Bytes
			self.write(head + "\r\n\r\n" + content + "\r\n\r\n")
			
		except BaseException as ex:
			trix.display (["ERROR", ex, xdata()])
			self.writeError("500", xdata())
			raise
	
	
	def head(self, result, clength):
		"""Return the head for the response."""
		gmt = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
		head = "\r\n".join([
			"HTTP/1.1 %s OK"     % result, 
			"Date: %s"           % (gmt),
			"Connection: %s"     % (self.Connection),
			"Server: %s"         % (self.Server),
			"Accept-Ranges: bytes",
			"Content-Type: %s"   % self.contentType,
			"Content-Length: %i" % (clength),
			"Last-Modified: %s"  % (gmt) # this should be the file mod date
		])
		return head
		
	
	
	
	def writeError(self, errcode, xdata=None):
		"""
		Write an error response given `errcode` and optional `xdata`.
		"""
		b = trix.ncreate('util.stream.buffer.Buffer', encoding='utf_8')
		w = b.writer()
		
		w.writeline("<html><head>\r\n")
		w.writeline('<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />\r\n')
		w.writeline("<title>Error</title>\r\n")
		w.writeline("<head><body>\r\n")
		
		if errcode == '404':
			w.writeline("<h1>404 File Not Found Error</h1>\r\n")
		else:
			w.writeline("<h1>500 Internal Server Error</h1>\r\n")
		
		w.writeline("<pre>\r\n")
		w.writeline(type(ex).__name__.encode('utf_8'))
		w.writeline(": %s\r\n" % (str(ex), 'utf_8'))
		
		if xdata:
			w.writeline(trix.formatter(xdata).encode('utf_8'))
		
		w.writeline("</pre>\r\n</body></html>\r\n\r\n")
		
		# SEND the error page.
		head = self.head(errcode, w.tell())
		self.socket.send("%s\r\n\r\n" % (head.encode('utf_8')))
		
		# read the response from the Buffer, b
		self.socket.write(b.read())
		