#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.
#


#
# I don't think this thing is very useful at all, but it's kinda
# neat and cool and fun, so I'm going to keep it here a while.
#


import time
from ..util.xinput import *


DEF_PROMPT = '> '
DEF_GUIDE = "Ctrl-c to exit."


class Prompt(object):
	"""
	Prompt lets you read, set, and otherwise manipulate values within 
	a structural object such as dict or list. 
	"""
	
	def __init__(self, o, config=None, **k):
		"""
		Pass a python object. Optionally, pass config with keys that
		specify the objects to use for handling actions:
		 * input  - default: prompt.PromptInput
		 * parse  - default: prompt.PromptParse
		 * handle - default: prompt.PromptHandle
		 * output - default: prompt.PromptOutput
		
		Call the 'prompt' method to start handling commands.
		"""
		
		config = config or {}
		config.update(k)
		
		self.__target = o
		self.__input = config.get('input', PromptInput())
		self.__parse = config.get('parse', PromptParse())
		self.__handle = config.get('handle', PromptHandle(self, o))
		self.__output = config.get('output', PromptOutput())
		
		T = type(o)
		self.__input.ident = "%s.%s" % (T.__module__, T.__name__)

	
	@property
	def target(self):
		"""Target object to which commands apply."""
		return self.__target
	
	@property
	def input(self):
		return self.__input
	
	@property
	def output(self):
		return self.__output
	
	@property
	def parse(self):
		return self.__parse
	
	@property
	def handle(self):
		return self.__handle
	
	def prompt(self, guide=DEF_GUIDE):
		"""Read and handle input from terminal or python interpreter."""
		result = None
		if guide:
			self.output(guide)
		try:
			# loop until ctrl-c
			while True:
				line = self.input()
				
				# this needs to come after line so that the final result
				# will be returned if ctrl-c is pressed
				result = None
				
				# parse and handle command
				if line.strip():
					command = self.parse(line)
					try:
						result = self.handle(command)
					except Exception as ex:
						print ("PROMPT EXCEPTION")
						trix.display(str(type(ex)), ex.args, xdata(
								line=line, command=command
							))
						print ("/PROMPT EXCEPTION")
						#raise
						
					# show the result of each command
					if result != None:
						self.output (result) 
				
		except KeyboardInterrupt:
			# print to get to the next line
			print()
			
		# return the result of the last command
		return result









class PromptHandle(object):
	def __init__(self, prompt, target, **k):
		self.target = target
		self.prompt = prompt
		
	def __call__(self, cmd):
		return self.handle(cmd)
	
	def handle(self, cmd, *a, **k):
		prop = getattr(self.target, cmd['cmd'])
		args = cmd['args']
		try:
			r = prop(*args)
		except TypeError:
			r = prop
		return r




class PromptInput(object):
	def __init__(self, prompt=DEF_PROMPT, **k):
		self.__prompt = k.get('prompt', prompt)
	
	def __call__(self):
		try:
			return xinput(self.prompt)
			#return textinput(self.prompt)
		except EOFError:
			time.sleep(1) # relief for win8+/py2 interpreter bug
	
	@property
	def prompt(self):
		return self.__prompt
	
	@prompt.setter
	def prompt(self, prompt):
		self.__prompt = prompt
		self.__resetprompt()
	
	@property
	def ident(self):
		return self.__ident
	
	@ident.setter
	def ident(self, id):
		self.__ident = id if id else ''
		self.__resetprompt()
		
	def __resetprompt(self):
		self.__prompt = "%s%s" % (self.__ident, self.__prompt)



class PromptText(object):
	
	def __call__(self):
		a = []
		try:
			while True:
				a.append(xinput(self.prompt))
		except KeyboardInterrupt:
			pass
		
		return a





class PromptOutput(object):
	def __call__(self, x):
		print (x)





class PromptParse(object):
	"""Incredibly simple line parser."""
	def __call__(self, line):
		r = {}
		cl = line.lstrip().split()
		r['cmd'] = cl[0]
		r['args'] = cl[1:]
		return r


