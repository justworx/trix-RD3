#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.
#

from . import *


def query(**k):
	"""Optional kwargs: select, where, and blocks."""
	ScanQuery(k.get('text'), k.get('blocks')).table(**k)


class ScanQuery(Scanner):
	"""Select info (eg., category, props, etc...) for characters."""

	Titles = 'c block bidi bracket cat num dec dig name props'
	
	@classmethod
	def chargen(self, blocknames=None):
		bnames = blocknames or udata.blocknames()
		blocks = udata.blocks()
		for block in bnames:
			rng = blocks[block]
			for c in range(*rng):
				yield (unichr(c))
	
	
	def __init__(self, text=None, blocknames=None):
		"""Pass text to query, or None (the contents of each block)."""
		text = text or self.chargen()
		Scanner.__init__(self, text)
	
	
	def query(self, **k):
		"""Pass keyword args to match. Eg., category='Po', etc..."""
		
		# select clause - a space-separated string listing titles
		titles = k.get('select', self.Titles).upper()
		
		# where clause - a lambda
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
						# There must be a better way to handle this...
						# ...happening every time will cause a slowdown.
						
						c = self.c.c
						if t == 'c':
							r.append(self.c.c)
						elif t == 'block':
							r.append(self.c.block)
						elif t in ['bidi', 'bidirectional']:
							r.append(self.c.digit)
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
					
					#
					# if fn returns True, add the char and properties, ordered
					# by the title
					#
					rr.append(r)
		except StopIteration:
			return rr

	
	def table(self, **k):
		rr = self.query(**k)
		trix.ncreate('fmt.Grid').output(rr)
	
	
	

def test():
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
	charinfo(c).next().display()

"""

CHAR    CATEGORY    BIDIRECTIONAL           PROPS
\n      Cc Control  B  Paragraph_Separator  Pattern_White_Space 
\r      Cc Control  B  Paragraph_Separator  Pattern_White_Space 

\t      Cc          S  Segment_Separator    Pattern_White_Space
,       Po          CS Common_Separator     Terminal_Punctuation
|       Sm          ON Other_Neutral        Pattern_Syntax
;       Po          ON Other_Neutral        Terminal_Punctuation
:       Po          CS Common_Separator     Terminal_Punctuation

"       Po          ON Other_Neutral        Quotation_Mark
'       Po          ON Other_Neutral        Quotation_Mark
     
<space> Zs; Space_Separator; WS White_Space; Pattern_White_Space

"""
	