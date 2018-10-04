#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.
#


from ..fmt import FormatBase


class Lines(FormatBase):
	"""Format line width and output."""
	
	DefLengths = 69
	DefFormats = {
		"title" : "#\n# {}\n#",
		"about" : "# {}",
		"list1" : " * ",
		"listn" : "   "
	}
	
	def __init__(self, formats=None, maxlen=None, **k):
		"""Pass max line-width and `formats` dict."""
		
		formats = formats or {}
		if not formats:
			for key in self.DefFormats:
				formats[key] = self.DefFormats[key]
		
		FormatBase.__init__(self, maxlen, formats, **k)
		
		self.__formats = formats
		self.__flength = {}
		self.__maxlen  = maxlen or self.DefLengths
	
	@property
	def formats(self):
		return self.__formats
	
	@property
	def maxlen(self):
		return self.__maxlen
	
	def format(self, format_key, text, **k):
		return self.__formats[format_key].format(text)
	
	def formatlen(self, format_key):
		try:
			return self.__flength[format_key]
		except KeyError:
			fblank = self.format(format_key, "")
			flines = fblank.splitlines()
			fmax = 0
			for line in flines:
				flen = len(line)
				if flen > fmax:
					fmax = flen
			self.__flength[format_key] = flen
			return fmax
	
	
	def lines(self, text):
		"""
		Return a list of lines paginated lines within length self.maxlen.
		"""
		words = text.strip().split()
		
		lines = [] # all lines
		cline = [] # current line
		chars = 0  # current line char count
		
		for word in words:
			
			# get line-length after new word (plus space) is appended
			chars += len(word)+1
			
			# if line length won't exceed maxlen, append the next word
			if chars <= self.maxlen:
				cline.append(word)
			
			# if it would exceed maxlen...
			else:
				lines.append(" ".join(cline))
				
				# there's still the current word to deal with; add it to
				# cline as the first word in the next line...
				cline = [word]
				
				# and restart the char length with the word's length+1
				chars = len(word)+1
		
		# get the last line
		if cline:
			lines.append(" ".join(cline))
		
		# return list of text lines
		return lines
		
		
		
