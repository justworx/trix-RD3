#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under
# the terms of the GNU Affero General Public License.
#


from ...util.runner import *
from ...util.xqueue import *
from ...util.wrap import *
from ...app.event import *


SERVICES_NCONFIG = "app/service/service.conf"


#
# --------- SERVICES -----------------
#
class Services(Runner):
	"""
	Container for various services.
	
	Services warp a single object and make use of it to perform 
	actions and return results.
	"""
	
	# INIT
	def __init__(self, config=None, **k):
		
		config = config or trix.nconfig(SERVICES_NCONFIG)
		if not config:
			raise Exception ("Services: Config required.")
		
		Runner.__init__(self, config, **k)
		
		self.__services = {}
		
		serviceConfDict = config['services']
		for sid in serviceConfDict:
			s = serviceConfDict[sid]
			
			# get the object config and create the object
			sconfig = s.get('nconfig')
			screate = s['ncreate']
			
			# create the Service object's contained object
			sobject = trix.ncreate(screate, sconfig)
			
			# create, store, and start the service object
			self.__services[sid] = Service(sid, sobject)
		
		# Start running the Services io loop (in a thread!)
		self.start()
		
	
	# SERVICES - SERVICES
	@property
	def services(self):
		return self.__services.keys()
	
	
	# SERVICES - IO
	def io(self):
		# give each service a chance to handle messages
		for s in self.__services:
			self.__services[s].handle_io()
	
	
	# SERVICES - CONNECT
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
	
	



#
# --------- SERVICE IO -----------------
#
class ServiceIO(object):
	pass





#
# --------- SERVICE -----------------
#
class Service(ServiceIO):
	"""
	A single service object, which handles requests.
	"""
	def __init__(self, serviceid, sobject):
		ServiceIO.__init__(self)
		
		self.__starttime = time.time()
		self.__serviceid = serviceid
		self.__object = sobject
		self.__wrapper = Wrap(sobject)
		self.__qpairs = []
	
	
	@property
	def serviceid(self):
		return self.__serviceid
	
	@property
	def uptime(self):
		return time.time() - self.__starttime
	
	
	# SERVICE - ADD QUEUES
	def addqueues(self, qproxypair):
		"""To be called by the owning Services object."""
		self.__qpairs.append(qproxypair)
	
	
	# SERVICE - HANDLE IO
	def handle_io(self):
		"""To be called only by the owning Services object."""
		
		for queues in self.__qpairs:
			try:
				qin, qout = queues
				
				# pop an event request from the Queue
				e = qin.get_nowait()
				
				# execute the command
				e.reply = self.handle_request(e)
				
				# Set the reply and return the event to the caller via the
				# out-queue (which is the client's in-queue).
				qout.put(e)
			
			except Empty:
				pass
			except ReferenceError:
				self.__qpairs.remove(queues)
			except Exception:
				e.error = xdata(qin=qin,qout=qout,e=e.dict)
	
	
	# SERVICE - HANDLE REQUEST
	def handle_request(self, e):
		
		# if there's no command, return a somewhat random info dict
		if not e.argc:
			return dict(
					service=self.serviceid, uptime=self.uptime, 
					target=repr(self.__object)
				)
		
		try:
			return self.__wrapper(*e.argv, **e.kwargs)
		except Exception as ex:
			raise type(ex) ('err-service-fail', xdata(
					message="service-request-fail", event=e.dict
				))





#
# --------- SERVICE CONNECT -----------------
#
class ServiceConnect(ServiceIO):
	"""Client connection to a single Service object."""
	
	def __init__(self, serviceid, queues):
		ServiceIO.__init__(self)
		
		#
		# The same queues in the opposite order; what's in for the 
		# service is out for the client (and vice versa). These are
		# the real queues - Service only holds proxies.
		#
		self.__qout, self.__qin = queues
		self.__sid = serviceid
	
	@property
	def serviceid(self):
		return self.__sid
	
	
	# SERVICE-CONNECT - REQUEST
	def request(self, command, *a, **k):
		"""
		Send a request to the Service object. Retrieve results from 
		command.reply;
		"""
		#
		# queue an event whose result will eventually be set by a call
		# to Service.handle_io; the result can be retrieved by calling
		# self.replies.
		#
		c = Event(command, *a, **k)
		self.__qout.put(c)
	
	
	# SERVICE-CONNECT - REPLIES
	def replies(self):
		"""
		Return a list of event objects; Check their reply for results.
		"""
		r = []
		try:
			while True:
				r.append(self.__qin.get_nowait())
		except Empty:
			pass
		return r
