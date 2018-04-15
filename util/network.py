#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under
# the terms of the GNU Affero General Public License.
#

from .. import *
import socket
try:
	import queue
except:
	import Queue as queue



class Host(object):
	"""Network information."""
	
	def __init__(self, host=None):
		
		# host, fqdn
		self.__host = host or socket.gethostname()
		self.__fqdn = socket.getfqdn(self.__host)
		self.__dbg = []
		
		
		# hostx
		try:
			self.__hostx = socket.gethostbyname_ex(self.__host)
			self.__name = self.__hostx[0]
			self.__alias = self.__hostx[1]
			self.__addrs = self.__hostx[2]
		except Exception as ex:
			self.__dbg.append(dict(hostx=["err", type(ex), ex.args]))
			self.__hostx = None
			self.__name = None
			self.__alias = None
			self.__addrs = None
		
		
		# get ip address
		try:
			self.__ip = self.__hostx[2]
		except Exception as ex:
			self.__ip = ''
		
		
		# split hostname by dots (eg, laptop.local, www.somesuch.com)
		try:
			self.__parts = self.hostx[2].split('.')
		except Exception as ex:
			self.__parts = []
		
		
		# check parts
		check = []
		#if len(parts) == 1:
		try:
			selflocal = "%s.local" % self.__host
			self.__local = socket.gethostbyname_ex(selflocal)
		except Exception as ex:
			#print("self-local error", ex)
			self.__local = None
		
		"""
		# <host>.local
		hostlocal = "%s.local" % self.__host
		try:
			self.__local = socket.gethostbyname_ex(self.__host)
		except:
			self.__local = None
		"""
	
	# STATUS
	def status(self):
		return dict(
			ip = self.ip,
			six = self.six,
			fqdn = self.fqdn,
			host = self.host,
			name = self.name,
			hostx = str(self.hostx),
			parts = str(self.parts),
			local = str(self.__local)
		)
	
	
	# DISPLAY
	def display(self, **k):
		trix.display(self.status(), **k)
	
	
	# PORT-SCAN
	def portscan(self):
		"""
		Pass an integer representing the highest port to scan, two ints
		representing the range of ports to scan (lowest first, then high),
		or pass nothing to scan the full range of ports (1-65536).
		"""
		r = []
		for port in range(0, 2**16):
			try:
				s = socket.socket()
				s.connect((self.host, port))
				r.append(port)
			except (OSError, socket.error) as ex:
				pass
			except Exception as ex:
				raise
		return r

	@property
	def six(self):
		"""True if ipv6 is available, else False."""
		return socket.has_ipv6
	
	@property
	def ip(self):
		return self.__ip
		
	@property
	def parts(self):
		return self.__parts
		
	@property
	def host(self):
		return self.__host
		
	@property
	def fqdn(self):
		return self.__fqdn
	
	@property
	def hostx(self):
		return self.__hostx
	
	@property
	def local(self):
		return self.__local
	
	@property
	def selflocal(self):
		return self.__local
	
	@property
	def name(self):
		return self.__name
	
	@property
	def alias(self):
		return self.__alias
	
	@property
	def addrs(self):
		return self.__addrs
	
	"""
	def addri(self):
		pass
		#return self.__local
	"""
	

class portscan(object):
	
	#
	# Play with these values (making them come out to 65536).
	# Might find a faster set of values.
	#
	REP = 32   # 256 | 4     512 1024 2048 4096 8192 | 16   32   64   128
	PER = 2048 # 256 | 16384 128 64   32   16   8    | 4096 2048 1024 512
	
	def __init__(self, host=None):
		self.__host = host or "localhost"
		self.__qresults = queue.Queue()
		self.__qerrors = queue.Queue()
		self.__started = 0
		self.__finished = 0
		self.__scanning = False
		self.__starttime = None
		self.__endtime = None
	
	def __del__(self):
		del(self.__qresults)
		del(self.__qerrors)
	
	@property
	def results(self):
		"""Wait for results from worker threads."""
		try:
			return self.__results
		except:
			self.wait()
			self.__results = sorted(self.__readqueue(self.__qresults))
			return self.__results
	
	@property
	def scantime(self):
		try:
			return self.__scantime
		except:
			if not self.__endtime:
				self.wait()
			self.__scantime = self.__endtime - self.__starttime
			return self.__scantime
	
	@property
	def errors(self):
		try:
			return self._errors
		except:
			self.wait()
			self.__errors = self.__readqueue(self.__qresults)
			return self.__errors
	
	
	def scan(self):
		"""Start scanning ports."""
		if self.__starttime != None:
			raise Exception ("err-already-scanned")
		
		self.__starttime = time.time()
		self.__scanning = True
		for i in range(0, self.REP):
			self.__started += 1
			trix.start(self.__scanrange, i, self.__qresults)
	
	
	def wait(self):
		"""Wait for scanning to complete."""
		while self.__finished < self.__started:
			time.sleep(0.1)
		self.__endtime = time.time()

	
	def __scanrange(self, i, q):
		
		host = self.__host
		start = i*self.PER
		end = start+self.PER
		#print (i, start, end)
		for p in range(start, end):
			try:
				socket.socket().connect(('localhost',p))
				q.put(p)
			except (OSError, socket.error) as ex:
				pass
			except Exception as ex:
				self.__qerrors.put([type(ex), ex.args])
		
		self.__finished += 1
	
	
	def __readqueue(self, q):
			r = []
			try:
				while True:
					r.append(q.get_nowait())
			except queue.Empty:
				pass
			return r
