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
	
	Services = {}
	ServConf = "x/service/service.conf"
	
	def __init__(self):
		self.__config = trix.nconfig(self.ServConf)
		self.__qpairs = []
		
	def client(self, serviceName):
		"""Pass a service configuration file path or dict."""
		try:
			# create an client for an existing service object
			serviceObject = self.Services[service]
			return ServiceClient(ServiceTransaction(serviceObject))
		except KeyError:
			try:
				# since it's not in the Services dict, add it...
				sconf = self.__config.get('services', {})
				Services[service] = trix.ncreate(sconf[service])
				
				# create (and pass) return a queue pair for `qpairs`
				return ServiceClient(Ser))
			except KeyError:
				raise KeyError("err-service-fail", xdata(
					detail="service-client-fail", reason="service-not-found",
					available=self.Services.keys(), requested=service
				))
		
		# If we got this far, there's at least one item in services,
		# so we'd better start a thread to reply to requests.
		self.start()


class Service(Runner):
	
	def __init__(self, servicename, configdict):
		
	
	def io(self):
		for qin, qout in self.__qpairs:
			try:
				# transaction is everything sent
				transaction = self.__qin.get():
				if transaction:
					args = t[0]
					krgs = t[1]
		
		



class ServiceClient(object):
	def __init__(self, io_queues):
		"""Receives a list of Queue objects for requests/replies."""
		self.__qin = io_queues[0]l
		self.__qout = io_queues[1]
	

