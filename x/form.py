#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.
#

from ..util.xinput import *
from trix.app.jconf import *


class Form(object):
	"""Command-line data entry form."""
	
	def __init__(self, config=None, **k):
		"""
		Pass config dict that contains a "desc" dict and a "keys" list.
		The "desc" dict is required. It must contain a set of 
		{name:description} pairs with the following parameters:
			* field (required) is the field title
			* desc (optional) may provide additional description/detail.
			* type (default "str") can be set to typecast the given value,
				Eg,.
				{
					# name field
					"name" : {
						"field" : "Full Name",
						"desc" : "First Middle Last"
					},
					
					# age field
					"age"  : {
						"field" : "Age",
						"desc" : "How old are you?",
						"type " : "float"
					}
				}
		
		The "keys" list is the order in which the discriptions are shown, 
		then followed by an input prompt. If a keys list is not provided,
		questions are ordered by the result of desc.keys().
		
		If configured "mode" is "json", each line entered must be json
		formatted and return dict elements will be typed. Remember, in
		this case, that json encoding rules apply. Eg., strings must be
		enclosed in "double-quotes", etc...
		"""
		
		config = config or {}
		
		try:
			config.update(**k)
		except AttributeError:
			if config:
				config = jconf(config, **k).obj
			else:
				config = k
		
		LF = config.get("format", "{}") #default: print as-is
		self.__format = LF
		
		self.__title = self.preptext(config.get('title', ""))
		self.__about = self.preptext(config.get("about", ""), formats=LF)
		self.__fields = config.get("fields", {})
		self.__keys   = config.get("keys", sorted(config.keys()))
		self.__prompt = config.get("prompt", "--> ")
		self.__mode = config.get('mode', '')
		self.__cancel = config.get('cancel', "Form Cancel.")
		
		#
		# Need to preptext each field's description. Too tired now.
		# for field in self.__fields; something like this...
		#
		#	desc = self.preptext(field.get("desc", ''))
		#	self.__fields[field]['desc'] = desc
		#
	
	@property
	def title(self):
		return self.__title
	
	@property
	def about(self):
		return self.__about
		
	@property
	def fields(self):
		return self.__fields
	
	@property
	def keys(self):
		return self.__keys
	
	@property
	def prompt(self):
		return self.__prompt
	
	
	def format(self, ftype):
		"""Pass format key. Eg, 'form-title', 'form-about', etc..."""
		return self.__format[ftype]
	
	
	def field(self, fieldname):
		return self.__fields[fieldname]
	
	
	#
	# FILL
	#
	def fill(self):
		"""
		Accepts input for each description in `self.desc`, as ordered by
		`self.keys`.
		
		Returns a dict containing field-names as keys and input values is 
		returned. All values are unicode, and converted to 'NFC' normal
		form.
		"""
		try:
			return self.__fill()
		except EOFError:
			if self.__cancel:
				print ("\n%s\n" % self.__cancel)
			return None
	
	
	# __FILL
	def __fill(self):
		
		if self.title:
			fmt = self.format("form-title")
			print(fmt.format(self.title))
		
		if self.about:
			fmt = self.format("form-about")
			print(fmt.format(self.about))
		
		r = {}
		f = self.fields
		
		for key in self.keys:
			
			xf = f.get(key)['field']                   # field name
			xd = self.preptext(f.get(key).get('desc')) # field desc
			xm = f.get(key).get('mode', '')            # field mode
			xt = f.get(key).get('type', 'str')         # field type
			
			# show the Field Name / Description
			print ("{0} ({1})\n - {2}".format(xf, xt, xd))
			
			x = xinput(self.prompt)
			if 'json' in [self.__mode, xm]:
				x = trix.jparse(x)
			elif xt != 'str':
				xtype = trix.nvalue(xt)
				print (xtype)
				x = xtype(x)
			
			r[key] = x
			print('')
		
		return r
	
	
	#
	# This DOES NOT WORK! The formatting of title and about are whack.
	# I'll turn it into an object tomorrow and break things up into 
	# more managable sections.
	#
	@classmethod
	def preptext(cls, text, maxlen=69, **k):
		"""Repaginates text lines to be less than a certain length."""
		
		xformats = k.get('formats', {})
		
		# line prefix 
		line_prefix = xformats.get("line-prefix", '')
		
		plength = len(line_prefix)
		maxlen -= plength
		
		words = text.strip().split()
		
		lines = [] # all lines
		cline = [] # current line
		chars = 0  # current line char count
		
		# pref controls whether the lines after the first line are
		# prefixed with formats['line-prefix']
		firstline = True
		
		for word in words:
			
			# get line-length after new word is appended
			chars += len(word)+1
			
			# if line length won't exceed maxlen, append the next word
			if chars <= maxlen:
				cline.append(word)
			
			# if it would exceed maxlen...
			else:
				
				# if this is the first line, simply append the joined words
				if firstline:
					lines.append(" ".join(cline))
					firstline = False # ...and set firstline to True
				
				# if this is NOT the firstline, add the prefix to the line
				else:
					lines.append(line_prefix + " ".join(cline))
				
				# there's still the current word to deal with; add it to
				# cline as the first word in the next line...
				cline = [word]
				
				# and restart the char length with the word's length+1
				chars = len(word)+1
		
		# get the last line
		if cline:
			lines.append(" ".join(cline))
		
		return '\n'.join(lines) + '\n'



