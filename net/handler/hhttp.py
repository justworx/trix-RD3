#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.
#

from . import *
from ...fmt import JDisplay
from time import gmtime, strftime


#
# HTTP (REQUEST PARSER)
#
class httpreq(object):
	def __init__(self, requestBytes):
		
		# lines received from the request
		self.bytes = requestBytes
		self.text = requestBytes.decode('utf_8')
		
		# array of request lines
		self.lines = L = requestBytes.splitlines()
		
		# produce a dict of utf8 keys : values
		self.request = L[0]
		self.headers = H = {}
		for l in L[1:]:
			if not l:
				break
			sp = l.split(b":", 1)
			hk = sp[0].decode("utf_8")
			try:
				try:
					H[hk] = sp[1].strip()
				except:
					H[hk] = b''
			except:
				pass



#
# HANDLE-HTTP
#
class HandleHttp(Handler):
	
	# INIT
	def __init__(self, sock, **k):
		k.setdefault('Connection', 'close')
		k.setdefault('Server', 'Nunayer-Bizwax/0.0.1')
		k.setdefault('Content-Type', 'text/html')
		
		self.__options = trix.kcopy(k, 'Connection Server Content-Type')
		
		Handler.__init__(self, sock, **k)
		
	
	# HANDLE DATA
	def handledata(self, data):
		"""Echo request."""
		try:
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
			head = head.encode('utf8')
			
			# Send content reply
			self.socket.send(b"%s\r\n\r\n%s" % (head, content))
		
		except BaseException as ex:
			self.socket.send(b"%s\r\n\r\n" % (head))
			self.socket.send(b"<html><body>\r\n")
			self.socket.send(b"<h1>500 Internal Server Error</h1>\r\n")
			self.socket.send(b"<pre>\r\n")
			self.socket.send(bytes(type(ex).__name__, 'utf_8'))
			self.socket.send(b": %s\r\n" % bytes(str(ex), 'utf_8'))
			self.socket.send(b"</pre>\r\n</body></html>\r\n\r\n")
			raise

	#
	# REPLY - The response text
	#
	def reply(self, req):
		content = """
		<html>
			<title>Default Response</title>
			<meta http-equiv="Content-Type" content="text/html; charset=utf_8" />
		</html>
		<body>
			<h1>Default Response</h1>
			<p>
				This is the default response generated by the HTTP handler
				class. To generate a real response, create a subclass of the
				`%s.%s` class and replace the `reply()` method. 
			</p>
			<p>
				Look for more information/documentation soon at:
				<br/>
				<a href="https://github.com/justworx/trix/"
					>https://github.com/justworx/trix/</a>
			</p>
		</body>
		</html>
		""" % (HandleHttp.__module__, HandleHttp.__name__)
		
		return content.encode("utf_8")
