#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under
# the terms of the GNU Affero General Public License.
#


from trix.app.plugin import *


class Dir(Plugin):
	"""Directory exploration via console."""
	
	COMMANDS = {
		'ls' : lambda d,*a: d.ls(*a),
		'cd' : lambda d,*a: d.cd(*a) or d.path		
	}
	
	def __init__(self, pname, owner, config, **k):
		Plugin.__init__(self, pname, owner, config, **k)
		
		p = config.get('path', '.')
		self.__dir = trix.path(p).dir()
	
	
	#
	# HANDLE
	#	
	def handle(self, e):
	
		cmd = e.argvl[0]
		if cmd in self.COMMANDS:
			x = self.COMMANDS[cmd]
			a = e.argv[1:]
			r = x(self.__dir, *a)
			self.reply(e, ", ".join(r))
		
		