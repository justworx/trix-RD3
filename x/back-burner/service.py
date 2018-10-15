#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under
# the terms of the GNU Affero General Public License.
#

from ..util.runner import *


class Service(Runner):
	"""
	Services that must be shared among various classes/threads.
	
	This class is exists as a way to allow access to the same sqlite3
	database across various threads.
	"""
	
	Services = {}
	
	@classmethod
	def startservice(cls, servicename, config):
		"""Place a Service object in the Service.Services dict."""
		
		# grr.. i'll have to think about how to implement this...
	
	
	
	def __init__(self, servicename):
		"""A service object."""
		
		if not servicename in self.Services:
			raise Exception ("service-not-found")
		
		self.__servicename = servicename
		self.__clientlist = []
	
	def addclient(self, client):
		pass
	
		




class ServiceClient(object):
	def __init__(self, serviceName):
		pass


