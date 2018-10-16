#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under
# the terms of the GNU Affero General Public License.
#

from ...util.runner import *


class Services(Runner):
	"""
	Container for various services.
	
	Services warp a single object and make use of it to perform 
	actions and return results.
	"""
	
	# INIT
	def __init__(self, config):
		self.__services = {}
		for s in config['services']:
			nconfig = s['nconfig']
			ncreate = s['ncreate']
			sobject = trix.ncreate(nconfig)
			self.__service[s] = Service(s, sobject)
			
	@property
	def services(self):
		return self.__services.keys()
	
	def io(self):
		# give each service a chance to handle messages
		for s in self.__services:
			self.__services[s].handle_io()
	
	def connect(self, serviceid):
		



class Service(object):
	"""
	A single service object, which handles requests.
	"""
	def __init__(self, serviceid, sobject):
		
		self.__serviceid = serviced
		self.__connects = []
		self.__object = sobject
	
	def handle_io(self):
		for connected in self.__connects:
			try:
				qin, qout = connected
				
				qout.put(self.handle_messages(qin.get()))
				
				
	def handle_messages(self, cmd, *args, **k):
				
	
	def client(self, 
		# a pair of queues - received data and result data
		self.__qin, self.__qout = self.__queues
	
	




class ServiceConnect(object):
	"""Client connection to a single Service object."""
	
	def __init__(self, serviceid, config, queues):
		
		# the same queues in the opposite order; what's in for the 
		# service is out for the client (and vice versa)
		self.__qout, self.__qin = queues
		self.__sid = serviceid
	
	
	@property
	def serviceid(self):
		return self.__sid
	
	
	def request(self, command, *a, **k):
		self.__qout.put(time.time(), command, a, k)
	
	
	def replies(self):
		"""Return a list of reply objects."""
		r = []
		try:
			while True:
				r.append(self.__qout.pop())
		except:
			pass
		return r


	
	