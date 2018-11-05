#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.
#

from trix.util.xiter import *


class Sensor(object):
	"""
	Analyze text data.
	
	But How?
	
	Create a new xiter subclass - something like charinfo, and maybe
	even based on charinfo, but with a lot more matching properties 
	that can be used in various sensory queries.
	
	Create a set of additional xiter-based subclasses that handle each 
	of a set of comparison categories...
	
	...I'm thinking... 
	
	Maybe I need to learn how to do it by doing it.
	"""
	pass



class xsensor(xiter): 
	"""
	OK - Idea 1... Pass a unicode text (file contents, whatever) and 
	scan through it calling on subclasses at appropriate times...
	"""
	
	def __init__(self, text, *queries, **k):
		pass
		# ...I'm thinking again...


class xs_char(xsensor): pass
class xs_text(xsensor): pass
class xs_line(xsensor): pass
class xs_doc (xsensor): pass


