#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under 
# the terms of the GNU Affero General Public License.
#


from ... import *


class cline(object):
	"""Command-line plugin."""
	
	@classmethod
	def handle(cls):
		cls.app = sys.argv[0]
		cls.cmd = sys.argv[1] if len(sys.argv) > 1 else ''
		if cls.cmd:
			#
			# Creating the command actually runs the command.
			# All plugins must be named the same as their module.
			#
			#print ("app.cline.%s.%s" % (cls.cmd, cls.cmd))         # DEBUG!
			trix.ncreate("app.cline.%s.%s" % (cls.cmd, cls.cmd))

	
	def __init__(self):
		"""Parse and store args, kwargs, and flags."""
		self.args = []
		self.flags = ''
		self.kwargs = {}
		
		args = sys.argv[2:]
		for a in args:
			if a[:2]=="--":
				kv = a[2:].split("=")
				self.kwargs[kv[0]] = kv[1] if len(kv)>1 else True
			elif a[:1] == '-':
				self.flags += a[1:]
			else:
				self.args.append(a)
		
		#trix.display([self.args, self.flags, self.kwargs])       # DEBUG!
		return
	
	def help(self):
		"""Print help for subclasses."""
		print (type(self).__doc__)
	
	
	#def display(self):
	#	trix.display([cls.app, cls.cmd, self.

