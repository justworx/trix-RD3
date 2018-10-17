#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under
# the terms of the GNU Affero General Public License.
#

from ...util.runner import *
from ...util.xqueue import *
from ...util.wrap import *


class Services(Runner):
	"""
	Container for various services.
	
	Services warp a single object and make use of it to perform 
	actions and return results.
	"""
	
	# INIT
	def __init__(self, config=None, **k):
		
		config = config or trix.nconfig("x/service/service.conf")
		if not config:
			raise Exception ("Services: Config required.")
		
		Runner.__init__(self, config, **k)
		
		self.__services = {}
		
		serviceConfDict = config['services']
		for sid in serviceConfDict:
			s = serviceConfDict[sid]
			
			# get the object config and create the object
			sconfig = s['nconfig']
			screate = s['ncreate']
			
			# create the Service object's contained object
			sobject = trix.ncreate(screate, sconfig)
			
			# create, store, and start the service object
			self.__services[sid] = Service(sid, sobject)
		
		# Start running the Services io loop (in a thread!)
		self.start()
		
	
	@property
	def services(self):
		return self.__services.keys()
	
	def io(self):
		# give each service a chance to handle messages
		for s in self.__services:
			self.__services[s].handle_io()
	
	def connect(self, serviceid):
		#
		# all you have to do is add a queue pair to the id'd service
		# and send the same queue pair to the connection object, then,
		# of course, call the services's `handle_io` method
		# frequently.
		#
		if not serviceid in self.__services:
			raise KeyError("No such service.", xdata(
					error="err-connect-fail", message="no-such-service",
					serviceid=serviceid
				))
			
		# Get the service we're connecting to...
		s = self.__services[serviceid]
		
		#
		# The ServiceConnect gets REAL Queues, so when they go away 
		# (eg, when the ServiceConnect object is deleted) the server 
		# will know it (because of a Reference Error) and will remove
		# the pair form its list.
		#
		realQPair = p = [Queue(), Queue()]
		
		# add the queue proxy pair to the requested Service object
		s.addqueues([trix.proxify(p[0]), trix.proxify(p[1])])
		
		# create and return a ServiceConnect object
		return ServiceConnect(s.serviceid, realQPair)



class Service(object):
	"""
	A single service object, which handles requests.
	"""
	def __init__(self, serviceid, sobject):
		
		self.__starttime = time.time()
		self.__serviceid = serviceid
		self.__object = sobject
		self.__qpairs = []
	
	
	@property
	def serviceid(self):
		return self.__serviceid
	
	@property
	def uptime(self):
		return time.time() - self.__starttime
	
	
	def addqueues(self, qpair):
		"""To be called by the owning Services object."""
		self.__qpairs.append(qpair)
	
	def handle_io(self):
		"""To be called only by the owning Services object."""
		for queues in self.__qpairs:
			try:
				qin, qout = queues
				
				request = qin.get()
				result = self.handle_messages(request)
				
				# send the request list back with the result appended
				request.append(result)
				
				# send the result back in the out-queue (which is the 
				# client's in-queue) with the result appended.
				qout.put(request)
			except Empty:
				pass
				
	def handle_messages(self, cmd, *args, **k):
		if cmd == 'info':
			return dict(
					service=self.serviceid, uptime=self.uptime, 
					target=repr(self.__object)
				)
	
	
#
# YOU ARE HERE:
#  - There's a bug somewhere between request and replies.
#  - There's no Exception (raised) but nothing comes back
#    to ServiceConnect.replies()
#



class ServiceConnect(object):
	"""Client connection to a single Service object."""
	
	def __init__(self, serviceid, queues):
		
		# the same queues in the opposite order; what's in for the 
		# service is out for the client (and vice versa)
		self.__qout, self.__qin = queues
		self.__sid = serviceid
	
	
	@property
	def serviceid(self):
		return self.__sid
	
	
	def request(self, command, *a, **k):
		"""
		Send a request to the Service object.
		
		Each request is a list with time, command, args list and kwargs
		dict, to be passed to the Service's object - the method named
		by `command` will receive a the passed list of arguments and the
		dict of keyword arguments.
		
		#
		# UNDER CONSTRUCTION... BUT FOR NOW...
		#
		The result (or None) will be appended to the list and returned
		in ServiceConnect.__qin.
		
		It's possible the result should be left out if there is none,
		and the dict should be checked each time.
		
		And... what happens with errors?
		"""
		self.__qout.put([time.time(), command, a, k])
	
	
	def replies(self):
		"""Return a list of reply objects."""
		r = []
		try:
			while True:
				r.append(self.__qin.pop())
		except Empty:
			pass
		return r


	
	