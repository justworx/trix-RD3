#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.
#



from . import *
import re



class IRCEvent(object):
	"""
	Parses lines of text received from the IRC server. Separates 
	each line into the following member variables:
	
	line   : full line as received
	orig   : text portion of line, with formatting
	text   : deformatted text
	target : recipient channel/nick
	prefix : sender's nick!user@[host]
	host   : sender's host
	user   : sender's user
	nick   : sender's nick
	uid    : sender's user@host
	irccmd : the IRC-specific command (eg. NICK, JOIN, etc...)
	
	For example: 
	```
	    if evt.uid == 'myuser@my-host-mask':
	        channelOrUser = self.target
	        try:
	        	executeCommand(channelOrUser, *evt.argv)
	        except:
	        	
	```
	"""
	
	REX = re.compile(r'\x03(?:\d{1,2},\d{1,2}|\d{1,2}|,\d{1,2}|)')
	
	@classmethod
	def stripFormat(cls, s):
		"""Strip color/formating codes from text."""
		s = s.replace('\x02', '').replace('\x16', '')
		s = s.replace('\x1f', '').replace('\x1F', '')
		return cls.REX.sub('', s).replace('\x0f', '').replace('\x0F', '')
	
	
	def __init__(self, line_text):
		"""
		Parse a single line of as received from the server into the
		appropriate member variables.
		"""
		
		line = line_text.strip()
		mm = line.split(' ', 3) # split the line
		ML = len(mm)            # get line length
		
		# manipulate the data
		if mm[0][0:1]==':':
			mm[0] = mm[0][1:]
		if ML>2 and mm[2][0:1]==':':
			mm[2] = mm[2][1:]
		if ML>3 and mm[3][0:1]==':':
			mm[3] = mm[3][1:]
		self.mm = mm
		
		# set up properties
		self.line   = line # full line as received
		self.orig   = ''   # text portion of line
		self.text   = ''   # deformatted text
		self.target = ''   # recipient channel/nick
		self.prefix = ''   # sender nick!user@[host]
		self.host   = ''   # irc host
		self.user   = ''   # irc user
		self.nick   = ''   # irc nick
		self.uid    = ''   # user@host (for auth)
		
		self.irccmd = None # Placeholder for the IRC-specific command
		
		# parse the event text
		if ML>3 and mm[3]:
			self.text = mm[3]
		if ML == 2:
			self.text = mm[1]
			self.irccmd = mm[0]
		else:
			self.prefix=mm[0]
			x = mm[0].split('!',1)
			if len(x)==1:
				self.nick=''
				self.user=''
				self.host=x[0]
			else:
				self.nick=x[0]
				x = x[1].split('@',1)
				self.user=x[0]
				if len(x)>1:
					self.host=x[1]
			
			if len(mm) > 1:
				self.irccmd = mm[1]
			else:
				irc.debug(
					"Strange Line", "Strange Command", self.line
					)
			if len(mm) > 2:
				self.target = mm[2]
			
			self.uid ='%s@%s' % (self.user, self.host)
		
		if self.text:
			self.orig = self.text
			self.text = self.stripFormat(self.text)
		
	@property
	def argv(self):
		return self.text.split(' ')
	
	@property
	def argc(self):
		return len(self.argv)
	
	@property
	def dict(self):
		"""Debugging utility - returns dict."""
		return {
			'line'   : self.line,
			'orig'   : self.orig,
			'text'   : self.text,
			'target' : self.target,
			'prefix' : self.prefix,
			'host'   : self.host,
			'user'   : self.user,
			'nick'   : self.nick,
			'uid'    : self.uid,
			'irccmd' : self.irccmd,
			'argv'   : self.argv,
			'argc'   : self.argc
		}
