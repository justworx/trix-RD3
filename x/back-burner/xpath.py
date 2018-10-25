#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under
# the terms of the GNU Affero General Public License.
#

from ..util import matheval

try:
	from html.parser import HTMLParser
except:
	from HTMLParser import HTMLParser


class xpath(HTMLParser):
	"""Partial X-Path Implementation; Simple path expressions."""
	def __init__(self, query, **k):
		EncodingHelper.__init__(**k)
		self.__query = query
		self.__data = []
		self.__path = []
		self.__pathi = {}
	
	#def __pathx(self, tag)
	
	def handle_startendtag(self, attrs):
		self.__path.append(tag)
		self.__data = []
		self.check(attrs)
		self.__path.pop()
	
	def handle_starttag(self, tag, attrs):
		self.__path.append(tag)
		self.__data = []
		self.check(attrs)

	def handle_endtag(self, tag):
		self.__path.pop()
	
	def handle_data(self, data):
		self.__data.append(data)
	
	def check(self, attrs):
		pass
	




class xpathparse(object):
	
	def __init__(self, query):
		"""Parse an xpath query string."""
		self.__query = query
		self.__qdata = None
	
	
	def parse(self):
		self.__qlist = q = self.__query.strip()
		self.__plist = q.split('/')
		return self._parse_brackets()
	
	
	
	
	def _parse_brackets(self):
		for i,pe in enumerate(self.__plist):
			bopen = pe.find('[')
			if bopen < 0:
				self.__plist[i]=[pe, None]
			else:
				bclose = pe.find(']')
				if bclose < 0:
					raise Exception("err-xpath-parse", xdata(
							detail='syntax-error', reason="unclosed-bracket", i=i,
							query=self.__query, pathlist=self.__plist, element=pe 
						))
				
				# get the "expr" text, between opening and closing brackets
				b1 = pe[:bopen]
				b2 = pe[bopen+1:bclose]
				
				# update the path-list
				self.__plist[i]=[b1,self._parse_expression(b2) or b2]

		return self.__plist
	
	
	
	def _parse_expression(self, x):
		
		# maybe it's a number
		try:
			return float(x)
		except ValueError:
			pass
		
		# try matheval
		try:
			# replace 
			a = x.split()
			r = dict(div='/', mod='%')
			for i,v in enumerate(a):
				if v in a:
					a[i] = r
			return matheval.eval(x)
		except Exception as ex:
			print (type(ex), ex.args)
			pass
	

	#DEF_CMP_OPS = "<>=!"
	def _parse_comparison(self, x):
		pass
		
	#DEF_CMP_OPS = "!= <= >= < > = !".split() 
	CMP = {
		"!=" : operator.ne,
		"<=" : operator.le,
		">=" : operator.gt,
		"<"  : operator.lt,
		">"  : operator.gt,
		"="  : operator.eq,
		"!"  : operator.is_not
	}
	
	BOOL = {
		"not" : operator.is_not, # <------------------------- CHECK THIS!
		"and" : operator.and_,
		"or" : operator.or_
	}



