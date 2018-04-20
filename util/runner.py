#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.
#


from .enchelp import * # trix

DEF_SLEEP = 0.1

class Runner(EncodingHelper):
	"""Manage an event loop, start, and stop."""
	
	def __init__(self, config=None, **k):
		"""Pass config and/or kwargs."""
		
		self.__jformat = trix.ncreate('fmt.JCompact')
		self.__running = False
		self.__csock = None
		self.__cport = None
		
		#
		# THIS NEEDS SOME ATTENTION
		#  - The lineq object should not be created unless there's a 
		#    cport, right?
		#  - Think about this...
		#
		self.__lineq = trix.ncreate('util.lineq.LineQueue')
		
		#trix.display([1, config, k])
		
		try:
			#
			# CONFIG
			#  - If this object is part of a superclass that's already set 
			#    a self.config value, then `config` and `k` are already part
			#    or all of it.
			#
			config = self.config
		except:
			#
			#  - If not, we'll need to create the config from args/kwargs.
			#    Creating a config dict, then - regardless of whether 
			#    `config` is from an existing self.config property - update
			#    it with `k` (directly below).
			#
			config = config or {}
		
		#trix.display([2, config, k])
		
		#
		# UPDATE CONFIG WITH `k`
		#  - Runner can't take a URL parameter unless it's part of a class
		#    that converts URL (or whatever other `config` type) to a dict
		#    before calling Runner's __init__. 
		#  - Therefore... don't catch this error; let it raise immediately
		#    so the developer will know there's something wrong here.
		#  - BTW: What the developer needs to do is make sure the config
		#         passed here from a base class is given as a dict.
		#
		config.update(k)
		
		#trix.display([3, config, k])
		
		# 
		# CONFIG - COPY
		#  - Runner should work as a stand-alone class, so....
		#  - Keep a copy in case this Runner object is created as itself
		#    (rather than as a super of some other class).
		#
		self.__config = config
		
		# 
		# ENCODING HELPER
		#  - Encoding for decoding bytes received over socket connections.
		# 
		EncodingHelper.__init__(self, config)
		
		#trix.display([4, config, k])
		
		# running and communication
		self.__sleep = config.get('sleep', DEF_SLEEP)
		
		# connect to calling process
		if "CPORT" in config:
			self.__cport = p = config["CPORT"]
			self.__csock = trix.ncreate('util.sock.sockcon.sockcon', p)
			try:
				self.__csock.writeline("%i" % trix.pid())
			except Exception as ex:
				trix.log("csock-write-pid", trix.pid(), type(ex), ex.args)
		
		#
		# Create a CallIO object, which calls .io() repeatedly and works 
		# safely, either inside a thread or normally. The purpose of
		# separating this functionality is to make sure that this object
		# is destroyed even if still running in a thread at the time of
		# deletion.
		#
		self.__callio = CallIO(trix.proxify(self))
	
	
	#
	# DEL
	#
	def __del__(self):
		"""Stop. Subclasses override to implement stopping actions."""
		try:
			try:
				self.stop()
			except Exception as ex:
				trix.log(
						"err-runner-delete", "stop-fail", ex=str(ex), 
						args=ex.args, xdata=xdata()
					)
			
			if self.__csock:
				try:
					#trix.log("runner-csock", "shutdown")
					self.__csock.shutdown(SHUT_RDWR)
				except Exception as ex:
					trix.log(
							"err-runner-csock", "shutdown-fail", ex=str(ex), 
							args=ex.args, xdata=xdata()
						)
		
		finally:
			self.__csock = None
			self.__proxy = None
	
	
	#
	# PROPERTIES
	#  - Runner is often one of a set of multiple base classes that may
	#    fail (and deconstruct) during init, so its properties need to
	#    be available even if Runner.__init__ has not yet been called.
	#  - This helps prevent raising of irrelevant Exceptions that might
	#    mask the true underlying error.
	#

	@property
	def csock(self):
		try:
			return self.__csock
		except:
			self.__csock = None
			return self.__csock
	
	@property
	def config(self):
		try:
			return self.__config
		except:
			self.__config = {}
			return self.__config
	
	@property
	def running(self):
		"""True if running."""
		try:
			return self.__running
		except:
			self.__running = None
			return self.__running
	
	@property
	def sleep(self):
		"""Sleep time per loop."""
		try:
			return self.__sleep
		except:
			self.__sleep = DEF_SLEEP
			return self.__sleep
	
	@sleep.setter
	def sleep(self, f):
		"""Set time to sleep after each pass through the run loop."""
		self.__sleep = f
	
	
	# START
	def starts(self):
		"""Run in a new thread; returns self."""
		self.start()
		return self
	
	def start(self):
		"""Run in a new thread."""
		
		try:
			self.__run_begin()
			trix.start(self.__callio.callio)
		except ReferenceError:
			self.stop()
		except Exception as ex:
			msg = "err-runner-except;"
			trix.log(msg, str(ex), ex.args, type=type(self), xdata=xdata())
			raise
	
		
	#
	# RUN
	#
	def run(self, threaded=False):
		"""Loop, calling self.io(), while self.running is True."""
		#
		# All of this exists in case Runner is running in the main thread.
		# The code must be duplicated in start/CallIO when threaded using
		# the `Runner.start` method. 
		#
		try:
			self.__run_begin()
			self.__callio.callio()
		except Exception as ex:
			msg = "Runner.run error stop;"
			trix.log(msg, str(ex), ex.args, type=type(self))
			raise
		finally:
			self.__run_end()
	
	def __run_begin(self):
		if self.running:
			raise Exception('already-running')
		self.__running = True
	
	def __run_end(self):
		self.__running = False
		self.__proxy = None
		self.stop()
	
	
	# IO
	def io(self):
		"""Override this method to perform repeating tasks."""
		if self.csock:
			
			# read the control socket and feed data to the line queue
			c = self.csock.read()
			self.__lineq.feed(c)
			
			while True:
				# read and handle a lines
				q = self.__lineq.readline()
				r = self.query(q)

				# package and send reply
				if r:
					r = dict(query=q, reply=None, error='unknown-query')
					self.csock.writeline(self.__jformat(r))
				else:
					break


	# QUERY
	def query(self, q):
		if q:
			q = q.strip()
			if q == 'ping':
				return dict(query=q, reply='pong')
			elif q == 'status':
				return dict(query=q, reply=self.status())
			elif q == 'shutdown':
				# stop, returning the new status
				self.stop()
				r = dict(query=q, reply=self.status())
				return r

	
	# STOP
	def stop(self):
		"""Stop the run loop."""
		trix.log("runner stop")
		self.__running = False
		self.__proxy = None
	
	# STATUS
	def status(self):
		return dict(
			ek = self.ek,
			running = self.running,
			sleep   = self.sleep,
			config  = self.config,
			cport   = self.__cport
		)
	
	# DISPLAY
	def display(self):
		trix.display(self.status())





class CallIO(object):
	"""
	Runner can't call trix.start to start or it won't stop unless 
	specifically told to (by calling, for example, `myrunner.stop()`.
	Use a CallIO object to call io() just as Runner.run would but from
	within a thread that holds its link to the Runner object by proxy.
	Then, when the object is destroyed in the main thread, it will no
	longer remain in the alternate thread.
	"""
	def __init__(self, runner):
		self.__runner = trix.proxify(runner)
	
	def callio(self):
		try:
			while self.__runner.running:
				self.__runner.io()
				time.sleep(self.__runner.sleep)
		except ReferenceError:
			pass




