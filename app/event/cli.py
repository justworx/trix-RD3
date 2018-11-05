#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.
#

import ast
from . import *
from ...data.scan import *

class LineEvent(Event):
	"""A Command-based event; Splits arguments using Scanner."""
	
	ARGPARSE = [
		lambda x: int(float(x)) if float(x)==int(float(x)) else float(x),
		lambda x: trix.jparse(x),
		lambda x: ast.literal_eval(x),
		lambda x: str(x)
	]
	
	@classmethod
	def argparse(cls, x):
		"""
		Type cast string `x` to int, float, dict, or list, if possible,
		or return the original string.
		"""
		errors = []
		for L in cls.ARGPARSE:
			try:
				return L(x)
			except Exception as ex:
				errors.append(xdata())
		
		# if all attempts to parse argument fail, raise an exception
		raise Exception("parse-fail", errors=errors)
	
	
	def __init__(self, commandline, **k):
		"""
		Pass full command line text, plus optional kwargs. The command
		line is scanned for string, int, float, list, and dict structures
		and an array of type-cast values is returned.
		
		Otherwise, it's just like Event, with first argument being the
		command, followed by individual arguments.
		
		>>> e = LineEvent('do [1, "two", {3:{4: "the number four"}}]')
		>>> e.arg(0)          # 'do'
		>>> e.arg(1)[2][3][4] # 'the number four'
		"""
		
		s = Scanner(commandline)
		a = s.split()
		r = []
		try:
			for x in a:
				r.append(self.argparse(x))
			
			Event.__init__(self, *r, **k)
		
		except Exception as ex:
			raise type(ex)(xdata(line=commandline, args=a, r=r))

