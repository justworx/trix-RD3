#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under
# the terms of the GNU Affero General Public License.
#

from ...util.runner import *


class Services(object):
	"""
	Application services container.
	
	Services are loaded individually as they're called for. Once it's
	loaded, the service will stay in memory.
	"""
	
	ServConf = "x/service/service.conf"
	
	def __init__(self):
		self.__config = trix.nconfig(self.ServConf)
		self.__qpairs = {}
		self.__services = {}
	
	
	# CLIENT
	def client(self, serviceName):
		"""Pass a service configuration file path or dict."""
		try:
			# create an client for an existing service object
			svcObject = self.__services[serviceName]
			
			# create (and store locally) 
			svcIoPairs = [Queue(), Queue()]
			self.__qpairs[serviceName].append(svcIoPairs)
			
			# return the client
			return ServiceClient(serviceName, svcObject, svcIoPairs)
		
		except KeyError:
			# The specified service isn't in the self.__services list
			try:
				# get config, create, and add the service object
				svcConfig = self.__config.get('services', {})
				svcObject = trix.ncreate(svcConfig[service])
				
				# add pairs for this service
				svcIoPairs = [Queue(), Queue()]
				self.__qpairs[serviceName].append(svcIoPairs)
				
				# create and return the service
				Services[service]=Service(serviceName,svcObject,svcIoPairs)
				
				# create (and pass) return a queue pair for `qpairs`
				return ServiceClient(Ser))
			except KeyError:
				raise KeyError("err-service-fail", xdata(
					detail="service-client-fail", reason="service-not-found",
					available=self.__services.keys(), requested=service
				))
		
	
	# IO
	def io(self):
		for s in self.__services:
			self.Services[s].io()




class Service(Runner):
	"""
	This object is stored in the Services.__services dict under
	`servicename`. The `configdict` argument comes from the config
	file under the `servicename` key.
	"""
	def __init__(self, servicename, serviceobject, servicequeues):
		self.__servicename = servicename
		self.__serviceobj  = serviceobject
		self.__queues      = servicequeues
	
	def io(self):
		for qin, qout, qerr in self.__queues:
			try:
				req = qin.get()
				if req:
					self.qout.put(self.handle_io(req))
			except:
				



class ServiceClient(object):
	"""
	The `ServiceClient` object is returned to the caller when the
	`Services.client()` method is called.
	"""
	def __init__(self, io_queues):
		"""Receives a list of Queue objects for requests/replies."""
		self.__qin = io_queues[0]l
		self.__qout = io_queues[1]
	

