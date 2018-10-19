#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under
# the terms of the GNU Affero General Public License.
# 

#
# I'm not too sure how useful this might be. I have no use for it.
# Maybe it should be "let go". I guess it might make more sense in
# some cases, for some people, and, well, it's not really hurting
# anything just sitting here.
#

from . import *


class Command(Event):
	"""An Event that separates the command from the args."""
	
	def __init__(self, command, *a, **k):
		Event.__init__(self, *a, **k)
		self.__command = command
	
	@property
	def cmd(self):
		return self.__command
	
	@property
	def command(self):
		return self.__command
	
	def getdict(self):
		d = Event.getdict(self)
		d['command'] = self.command
		return d












