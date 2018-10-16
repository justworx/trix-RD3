#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under
# the terms of the GNU Affero General Public License.
#

from ...util.runner import *


class Service(Runner):
	"""
	Application Service container.
	
	Services are loaded individually as they're called for. Once it's
	loaded, the service will stay in memory.
	"""
	
	# all services stored with the class object; key=Service()
	__Services = {}
	
	
	
	# INIT
	def __init__(self, serviceid):
		
		self.__serviceid = serviceid
		
		if not serviceid in self.__Services:
			if not self.available(serviceid):
				raise KeyError("No Such Service", xdata(
					err="err-service-fail", detail='no-such-service'
				))
			
			# get service-specific config
			sconf = self.config[serviceid]
			objconf = sconf["nconfig"]
			objserv = sconf["ncreate"]
			
			# create the object to handle requests, generate replies
			config = trix.nconfig(objconf)
			self.__object = trix.ncreate(objserv)
	
	
	@property
	def serviceid(self):
		return self.__serviceid
	
	@property
	def config(self):
		try:
			return self.__config
		except:
			self.__Config = trix.nconfig("x/service/service.conf")
			trix.display(self.__Config)
			print (":", self.serviceid)
			self.__config = self.__Config['services'][self.serviceid]
			trix.display(self.__config)
			return self.__config
	
	
	
	def available(self, serviceid): 
		return serviceid in self.config.keys()
