#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.
#


# --- TEXT EVENT ---

class TextEvent(object):
	"""
	Package a single line of text into an event structure.
	
	Properties:
		line : full line as received
		text : alias for line
		argv : list of arguments [text.split()]
		argc : count(argv)
		argvl: same as argv, but all lower-case
		argvc: same as argc, but all capital letters
		dict : all of the above, in a dict.
	
	The line of text is split on spaces. The self.argv property returns
	a list of all the words. The first word is typically considered to
	be a command while following words are its arguments. 
	
	NOTE:
	Subclasses may separate args from other data, as is the case of 
	`trix.net.irc.irc_event.IRCEvent`. However, even in that case the
	conceptual command - intended for a bot - is the first item
	in IRCEvent.argv and subsequent items in `argv` are the command's
	parameters. Other items of - something like "meta-data" - are
	stored in additional "irc-only" properties (eg, the irccmd which
	is the server's "PRIVMSG" or "NOTICE" command), but the received
	text works just like here in TextEvent: The conceptual command 
	is the first item in argv and the rest are that command's 
	parameters.
	
	NOTE ALSO:
	While self.line and self.text are always the same for TextEvent,
	they may be different in subclasses. In IRCEvent, the `line`
	value may include irc formatting codes (eg., bold, italic, or
	colors, etc..), but text will always be deformatted. Therefore,
	self.text should be called in cases where machine-processing 
	does not require the use of formatting, while self.line should
	be used if that format info is needed.
	"""
	
	def __init__(self, cline):
		"""
		Pass one line of text that is to be processed as a command. 
		"""
		self.__line = cline
		self.__reply = None
	
	@property
	def line(self):
		"""The full line of text, as given to the constructor."""
		return self.__line
	
	@property
	def text(self):
		"""The full line of text, as given to the constructor."""
		return self.__line
	
	@property
	def argc(self):
		"""
		Argument count. (The number of space-separated words in `text`.)
		"""
		try:
			return self.__argc
		except:
			self.__argc = len(self.argv)
			return self.__argc
	
	@property
	def argv(self):
		"""
		Each individual word stored as a list item.
		"""
		try:
			return self.__argv
		except:
			self.__argv = self.text.split(' ')
			return self.__argv
	
	@property
	def argvc(self):
		"""Arg-v all-caps."""
		try:
			return self.__argvc
		except:
			self.__argvc = []
			for a in self.argv:
				self.__argvc.append(a.upper())
			return self.__argvc
	
	@property
	def argvl(self):
		"""Arg-v all lowercase."""
		try:
			return self.__argvl
		except:
			self.__argvl = []
			for a in self.argv:
				self.__argvl.append(a.lower())
			return self.__argvl
	
	@property
	def dict(self):
		"""Debugging utility - returns dict."""
		return {
			'line'  : self.line,
			'text'  : self.text,
			'argc'  : self.argc,
			'argv'  : self.argv,
			'argvc' : self.argvc,
			'argvl' : self.argvl,
			'reply' : self.reply
		}
	
	
	@property
	def reply(self):
		return self.__reply
	
	@reply.setter
	def reply(self, data):
		self.__reply = data
