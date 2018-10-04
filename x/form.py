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
		
		self.__title = self.preptext(config.get('title', ""))
		self.__about = self.preptext(config.get("about", ""))
		self.__fields = config.get("fields", {})
		self.__keys   = config.get("keys", sorted(config.keys()))
		self.__prompt = config.get("prompt", "--> ")
		self.__mode = config.get('mode', '')
		
		#
		# Need to preptext each field's description. Too tired now.
		# for field in self.__fields; something like this...
		#
		#	desc = self.preptext(field.get("desc", ''))
		#	self.__fields[field]['desc'] = desc
		#
		
		config = config or {}
		
		try:
			config.update(**k)
		except AttributeError:
			if config:
				config = jconf(config, **k).obj
			else:
				config = k
		
		self.__title = self.preptext(config.get('title', ""))
		self.__about = self.preptext(config.get("about", ""))
		self.__fields = config.get("fields", {})
		self.__keys   = config.get("keys", sorted(config.keys()))
		self.__prompt = config.get("prompt", "--> ")
		self.__mode = config.get('mode', '')
		
		"""
		# Need to preptext each field's description. Too tired now.
		for field in self.__fields:
			desc = self.preptext(field.get("desc", ''))
			self.__fields[field]['desc'] = desc
		"""
	
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
		
		r = {}
		for key in self.keys:
			if self.title:
				print("%s: %s" % (key, self.title))
			if self.about:
				print(" - %s" % (self.about))
			
			x = xinput(self.prompt)
			if self.__mode == 'json':
				x = trix.jparse(x)
			
			r[key] = x
			print()
		
		return r
	
	
	
	@classmethod
	def preptext(cls, text, maxlen=69): #dude
		"""Repaginates text lines to be less than a certain length."""
		
		words = text.strip().split()
		
		lines = [] # all lines
		cline = [] # current line
		chars = 0  # current line char count
		
		for word in words:
			chars += len(word)+1
			if chars <= maxlen:
				cline.append(word)
			else:
				lines.append(" ".join(cline))
				cline = [word]
				chars = len(word)+1
		
		# get the last line
		if cline:
			lines.append(" ".join(cline))
		
		return '\n'.join(lines)



