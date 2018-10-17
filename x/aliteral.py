# THIS IS TOTALLY EXPERIMENTAL

import ast

class parseargs(object):
	def __init__(self, text):
		self.__text = text
		self.__rslt = []
	
	@property
	def text(self):
		return self.__text
	
	def parse(line):
		for c in line:
			if c in ['"', "'"]:
				self.__rslt.append(parsequote(c))
			elif c in 
				