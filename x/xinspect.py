#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under
# the terms of the GNU Affero General Public License.
#


import inspect


class Inspect(object):
	"""Covers the python `inspect` module."""
	
	def __init__(self, o):
		self.__o = o
	
	def get(self, predicate=None):
		return inspect.getmembers(self.__o, predicate)
	
	def functions(self):
		return self.get(inspect.isfunction)
	
	def classes(self):
		return self.get(inspect.isclass)
	
	def methods(self):
		return self.get(inspect.ismethod)
	
	def properties(self):
		r = {}
		classes = self.classes()
		for cls in classes:
			ts = str(cls[0])          # type string
			md = cls[1].__module__    # module path
			nm = cls[1].__name__      # class name
			fp = "%s.%s" % (md, nm)   # full mod/class path
			
			# inspect for properties in c1 using lambda
			lx = lambda o: isinstance(o,property)
			pp = inspect.getmembers(cls[1], lx)
			
			# turn the `pp` pairs into key=values in a dict
			pd = {}
			for item in pp:
				pd[item[0]] = item[1]
			
			# add class to the return dict
			r[nm] = dict(
					typestring = ts, 
					modulepath = md, 
					modulename = nm, 
					fullmodpath= fp, 
					properties = pd,
					classobject= cls[1]
				)
		return r
	
	def generators(self):
		return self.get(inspect.isgenerator)
	
"""
python3
from trix.x.xinspect import *
from trix.app.form import *

obj = Form({}, about="Testing!")
ii = Inspect(obj)
pp = ii.properties()
trix.display(pp)

po = pp['Form']['pp'][0][1]
po.fget(obj)

#trix.display(ii.methods())

"""
