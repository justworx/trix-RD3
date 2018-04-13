#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.
#

from . import *

def query(**k):
	"""
	This function (in addition to being pretty nifty) is a tool to help 
	us find the information we need to build efficient scanning methods.
	
	The idea is to select character info (eg., category, props, etc...) 
	matching keyword argument specifications.
	
	KWARGS:
	 * select : A list of `charinfo` properties to select.
	            Eg, select="char numeric decimal digit" 
	 * blocks : A list of blocks to query. 
	            Eg, blocks=['Basic Latin', 'Gothic']
	 * where  : A callable object that returns True for objects that 
	            should be selected, else False.
	            Eg, where=lambda c: c.numeric != None
	 
	 * text   : The `text` kwarg may be specified instead of 'blocks'
	            to query info from a given string (or other iterable).
	            Eg, text="Text I'm having trouble parsing!" 
	
	Either `blocks` or `text` may be specified, not both. If neither is
	specified, all characters from all blocks are checked for matches.
	
	```python3
	from trix.data.scan.scanquery import *
	query(
	    select="block char numeric decimal digit",
	    blocks=['Basic Latin', 'Gothic'],
	    where =lambda c: c.num != None 
	  )

	```
	
	The complete list of property names is:
	[
		'char', 'c', 'block', 'bidi', 'bidirectional', 'bracket', 'cat', 
		'category', 'num', 'numeric', 'dec', 'decimal', 'dig', 'digit',
		'name', 'props', 'properties','bidiname','catname'
	]
	
	Several of these are aliases (a space-saving measure for lambdas):
	 - bidi = bidirectional
	 - cat = category
	 - char = c
	 - dec = decimal
	 - dig = digit
	 - num = numeric
	 - props = properties
	
	"""
	ScanQuery(**k).table(**k)




class ScanQuery(Scanner):
	"""Select unicode data properties. See `scanquery.query()` help."""
	
	# default fields to query
	Titles = 'block char bidi bracket cat num dec dig name props'
	
	@classmethod
	def chargen(self, **k):
		bnames = k.get('blocks') or udata.blocknames()
		blocks = udata.blocks()
		for block in bnames:
			rng = blocks[block]
			rng[1] += 1
			try:
				for c in range(*rng):
					yield (unichr(c))
			except ValueError:
				if c > 0x10FFFF:
					raise StopIteration()
	
	
	def __init__(self, **k):
		"""Pass text to query, or None (the contents of each block)."""
		text = k.get('text') or self.chargen(**k)
		Scanner.__init__(self, text)
	
	
	def query(self, **k):
		"""Pass keyword args to match. Eg., category='Po', etc..."""
		
		# select clause - a space-separated string listing titles
		titles = k.get('select', self.Titles).upper()
		
		# where clause - a lambda or other callable
		fn = k.get('where')
		
		tt = [] # title list
		rr = [] # result lists
		
		# titles are taken from the select clause, but all-caps
		rr.append(titles.split())
		
		titles = titles.lower().split()
		try:
			while True:
				if (self.cc and (not fn)) or fn(self.c):
					r = []
					
					for t in titles:
						#
						# TO DO:
						#  - There must be a better way to handle this...
						#    ...happening every time might make it slow :-/
						#
						c = self.c.c
						if t in ['char','c']:
							r.append(self.c.c)
						elif t == 'block':
							r.append(self.c.block)
						elif t in ['bidi', 'bidirectional']:
							r.append(self.c.bidirectional)
						elif t == 'bracket':
							r.append(self.c.bracket)
						elif t in ['cat', 'category']:
							r.append(self.c.category)
						elif t in ['num', 'numeric']:
							r.append(self.c.numeric)
						elif t in ['dec', 'decimal']:
							r.append(self.c.decimal)
						elif t in ['dig', 'digit']:
							r.append(self.c.digit)
						elif t == 'name':
							r.append(self.c.name)
						elif t in ['props', 'properties']:
							r.append(" ".join(self.c.props))
						
						elif t == 'bidiname':
							r.append(self.c.bidiname)
						elif t == 'catname':
							r.append(self.c.catname)
						
						# extra, for clarity...
						elif t == 'ord':
							s = "%x" % ord(self.c.c)
							r.append("0x%s" % s.upper())
					
					# add the row to results
					rr.append(r)
					
		except StopIteration:
			return rr
		
		except Exception:
			raise Exception(xdata())

	
	def table(self, **k):
		rr = self.query(**k)
		trix.ncreate('fmt.Grid').output(rr)
	
	
	

def charloop():
	"""
	Loop, display the character properties for given string. Enter an
	empty string (or use Ctrl-c) to	exit. 
	
	NOTE: Results can be long... use single characters or short strings.
	"""
	x = input("--> ")
	while x:
		s = Scanner(x)
		try:
			while s.cc:
				s.c.display()
		except:
			pass
		x = input("--> ")



def char(c):
	"""Display the properties of a single character."""
	charinfo(c).next().display()

