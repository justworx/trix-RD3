#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.
#

DEF_HOST = '127.0.0.1'
DEF_BUFFER = 4096 * 4
DEF_LINEEND = "\r\n"
DEF_FAMILY = 'AF_INET'
DEF_TYPE   = 'SOCK_STREAM'
DEF_PROTO  = 0

SOCK_TIMEOUT = 0.00001 # read/accept timeout
SOCK_CTIMEOUT = 9      # connection timeout


from ..util.enchelp import *
from ..util.urlinfo import *
#from ..enchelp import *
#from ..urlinfo import *
import select



class sockbase(EncodingHelper):
	"""Common socket features."""
	
	
	def __init__(self, config, **k):
		"""Pass `config` as dict, address data, or url."""
		config.update(k)
		EncodingHelper.__init__(self, config)
		self.__config = config
	
	
	@property
	def config(self):
		return self.__config
	
	
	def status(self):
		return {
			'ek' : self.ek
		}
	
	def display(self):
		trix.display(self.status())






#
# ---- SOCKWRAP -----
#
class sockwrap(sockbase):
	"""Contains a socket."""
		
	def __init__(self, config=None, **k):
		"""Pass `config` dict containing a pre-connected socket."""
		
		sockbase.__init__(self, config, **k)
		
		# store the actual socket object here
		self.__realsock = config['socket']
		
		# These are needed by all socket connections
		self.__buflen = self.config.get('buflen', DEF_BUFFER)
		self.__newl = self.config.get('newl', DEF_LINEEND)

	
	@property
	def socket(self):
		return self.__realsock
	
	@property
	def buflen(self):
		return self.__buflen
	
	@property
	def newl(self):
		return self.__newl
		
	@property
	def addr(self):
		"""Returns local address as tupel (addr,port)."""
		return self.socket.getsockname()
		
	@property
	def peer(self):
		"""Returns remote address as tupel (addr,port)."""
		return self.socket.getpeername()
	
	@property
	def port(self):
		"""Return this socket's port."""
		return self.addr[1]
	
	
	# PROPS WITH SETTERS
	@property
	def timeout(self):
		"""Returns timeout value."""
		return self.socket.gettimeout()
	
	@timeout.setter
	def timeout(self, f):
		"""Set timeout value."""
		self.socket.settimeout(f)
	
	
	# WRITE
	def write(self, text, **k):
		"""
		Encode text to bytes (by encoding specified to constructor) and 
		send. Default encoding is trix.DEF_ENCODE.
		"""
		return self.send(text.encode(**self.extractEncoding(k)))
	
	
	# WRITELINE
	def writeline(self, text, **k):
		self.write("%s%s" % (text, self.newl), **k)
	
	
	# READ
	def read (self, sz=None, **k):
		"""Decode received data and return it as text."""
		try:
			bdata = self.recv(sz or self.buflen)
		except socket.timeout:
			return ''
		
		if bdata:
			return bdata.decode(**self.ek)
			try:
				return bdata.decode(**self.ek)
			except UnicodeDecodeError:
				print ("#")
				print ("# sockwrap.read: UnicodeDecodeError; dt:" + time.strftime("%Y-%m-%d %H:%M:%S"))
				print (b"# BYTES: " + bdata)
				print ("#")
				return ""
		return bdata
	
	
	#
	# SEND
	#
	def send(self, data):
		"""
		Send `data` bytes.
		
		ERRORS (and how to handle them):
		 * socket.timeout : In the event of socket.timeout errors, retry
		   sending until you succeed or are ready to give up.
		 * socket.error : On socket.error exceptions, the socket is 
		   shutdown, so you have to reconnect and renegotiate the
		   transmition in whatever way is appropriate to your situation.
		 * For other exception types check the `python` xdata key for
		   clues to help debug the problem.
		"""
		try:
			if not self.socket:
				raise Exception('err-send-fail', xdata(detail='socket-closed',
						config=self.config
					))
			
			if data:
				try:
					return self.socket.send(data)
				except (socket.timeout, socket.error):
					raise
				except Exception as ex:
					raise Exception('err-send-fail', xdata(
						reason='socket-send-error', python=str(ex)
					))
		
		except ReferenceError:
			#
			# The socket has shutdown and been deleted. Don't whack out any
			# __del__ methods with a ReferenceError... just ignore this.
			#
			pass
	
	
	# RECV
	def recv(self, buflen):
		"""
		Return any received data, or None if no data has been received.
		"""
		if not self.socket:
			raise Exception('err-recv-fail', xdata(detail='socket-closed',
					config=self.config
				))
		
		s = self.socket
		if s:
			try:
				try:
					# POLL - DON'T WAIT FOR TIMEOUT
					R,W,X = select.select([s],[],[s],0)
				except Exception as ex:
					# If this system doesn't support select.select(), convert
					# to using self.socket.recv directly (for future calls).
					self.recv = self.socket.recv
				
				# receive
				if R:
					return s.recv(buflen)
				if X:
					raise SIOError(x)
			
			except socket.timeout:
				return ''
			
			except socket.error as ex:
				error = 'err-recv-fail'
				errno = None
				errstr = ''
				xreason = ''
				try:
					if isinstance(ex, basestring):
						errstr = ex
					else:
						errno = ex[0]
						if errno == 10058:
							errstr = "Recv attempt after peer disconnect."
							xreason = 'recv-after-disconnect'
						elif errno == 10054:
							errstr = "Peer brutishly disconnected. (Server)"
							xreason = 'peer-brutishly-disconnected'
							#xdetail = 'whatever-that-means'
						elif errno == 10053:
							errstr = "Connection forcibly closed by remote host."
							xreason = 'host-closed-connection'
				except:
					pass
				
				#
				# Apparently converting `ex` string can cause an exception,
				# so we need to be careful not to lose any valid info here.
				#
				try:
					EX = str(ex)
				except:
					EX = ""
				
				# now we won't lose whatever `ex` was (if it was)
				raise type(ex)(ex.args, xdata(
						error=error, errno=errno, errstr=errstr, xreason=xreason, 
						xtype=str(type(ex)), config=self.config, EX=EX
					))
				
			except Exception:
				raise


	# SHUTDOWN
	def shutdown(self):
		"""Shutdown the socket."""
		try:
			self.socket.shutdown(socket.SHUT_RDWR)
		except:
			pass
		finally:
			self.__socket = None
	
	
	# STATUS
	def status(self):
		s = sockbase.status(self)
		s.update({
				'peer' : self.peer,
				'addr' : self.addr,
				'port' : self.port,
				'newl' : self.newl,
				'buflen' : self.buflen,
				'timeout' : self.timeout
			})
		return s








#
# ---- SOCKCON -----
#

class sockcon(sockwrap):
	"""Creates a socket conenction."""
	
	def __init__(self, config=None, **k):
		
		# parse config... store as dict
		config or {}
		try:
			# if config is a dict, update with kwargs then create a 
			# urlinfo object.
			config.update(k)
			uinfo = urlinfo(config)
		except:
			# if config is NOT a dict, the urlinfo object must be created
			# first, and a config dict is generated from that result.
			uinfo = urlinfo(config)
			config = uinfo.dict
			config.update(k)
		
		# make sure connection params include a host
		if not uinfo.get('host'):
			uinfo['host'] = DEF_HOST
		
		# connect, and set the socket in config (so that sockwrap can
		# access it when sockwrap.__init__ is called).
		s = self.__connect(config, uinfo)
		config['socket'] = s
		
		# store urlinfo object for reference
		self.__urlinfo = uinfo
		
		# pass the config (complete with socket) up to sockwrap
		sockwrap.__init__(self, config, **k)

	
	
	def status(self):
		return dict(
			sockbase = sockbase.status(self),
			sockwrap = dict(
				addrinfo = self.addrinfo(),
				urlinfo = self.__urlinfo
			)
		)
	
	# ADDR-INFO
	def addrinfo(self, **k):
		return self.__urlinfo.addrinfo(**k)
	
	
	# CONNECT
	def __connect(self, config, uinfo):
		
		# setup...
		ctimeout = config.get('ctimeout', SOCK_CTIMEOUT)
		
		try:
			aainfo = uinfo.addrinfo()
		except socket.gaierror as ex:
			raise type(ex)(ex.args, xdata(error="err-connect-fail",
					config=config, url=uinfo, k=k
				))
		
		#
		# Loop through possible addresses trying each until a successful
		# connection is made.
		#
		s = None
		ok = False
		errs = []
		starttm = time.time()
		for ainfo in aainfo:
			i = 0
			try:
				s = socket.socket(ainfo[0], ainfo[1], ainfo[2])
				if config.get('wrap'):
					s = trix.module('ssl').wrap_socket(s)
				s.settimeout(ctimeout)
				s.connect(ainfo[4])
				
				#
				# RETURN SOCKET OBJECT
				#  - This method is private so that only the constructor may
				#    call for a socket.
				#  - The socket must not be stored here, or anywhere except
				#    the `sockprop` class (by way of `sockwrap`, which also
				#    does NOT store the object directly!)
				#
				return s
			
			except Exception as ex:
				errs.append(
						dict(xtype=type(ex), a=ex.args, ainfo=ainfo
					)) 
		
		raise Exception("err-connect-fail", xdata(
			aainfod=[cls.__ainformat(a) for a in aainfo], 
			starttm=starttm, endtime=time.time(), ctimeout=ctimeout,
			uidict=uinfo.dict, a=(config), socket=repr(s), 
			errs=errs
		))
		
		
	
	
	@classmethod
	def __ainformat(self, ainfo):
		#
		# Utility for reporting errors that may occur in `__connect`.
		#
		return {
			"family" : ",".join(sockname(ainfo[0], "AF_")),
			"kind"   : ",".join(sockname(ainfo[1], "SOCK_")),
			"proto"  : ainfo[2],
			"cannon" : ainfo[3],
			"addr"   : ainfo[4]
		}

