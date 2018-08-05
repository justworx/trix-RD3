#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under
# the terms of the GNU Affero General Public License.
#

from . import *
from trix.net.connect import *
from trix.util.runner import *
from trix.util.enchelp import *
import re


IRC_DEBUG = 1  # debug level default: 1
PLUG_UPDT = 15 # update plugins every 15 seconds


#
# ---- CONNECT -----
#
def connect(config, **k):
	"""
	Pass config dict or string path to config json file. Connects to 
	IRC network and returns an IRCConnect object (see below).
	"""
	
	# get configuration
	if isinstance(config, str):
		conf = trix.path(config).wrapper(encoding='utf_8').read()
		conf = trix.jparse(conf)
	elif isinstance(config, dict):
		conf = config
	else:
		raise ValueError("err-invalid-config", xdata(
				detail="bad-config-type", require1=['dict','str'],
				Note="Requires a dict or string path to json file"
			))
	
	# create and return the connect object
	return IRCConnect(conf, **k)



#
# ---- DEBUG -----
#
def debug (*a):
	for item in a:
		print ("# %s" % str(item))




# ------------------------------------------------------------------
#
# IRC CONNECT
#
# ------------------------------------------------------------------

class IRCEvent(object):
	"""
	Parses lines of text received from the IRC server. Separates 
	each line into the following member variables:
	
	line   : full line as received
	orig   : text portion of line, with formatting
	text   : deformatted text
	target : recipient channel/nick
	prefix : sender nick!user@[host]
	host   : irc host
	user   : irc user
	nick   : irc nick
	uid    : user@host
	irccmd : the IRC-specific command (eg. NICK, JOIN, etc...)
	
	For example: 
	```
	    if evt.uid == 'myuser@my-host-mask':
	        channelOrUser = self.target
	        executeCommand(channelOrUser, *evt.argv)
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
			self.irccmd = mm[1]
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





# ------------------------------------------------------------------
#
# IRC CONNECT
#
# ------------------------------------------------------------------

class IRCConnect(Connect, Runner):
	"""
	IRC Connection object.
	
	IRCConnect creates and maintains one connection to one irc network
	server. The functionality is limited to connecting and replying to
	PING lines. All other activity is handled by plugins.
	"""
	
	def __init__(self, config=None, **k):
		
		self.show = None
		self.debug = IRC_DEBUG
		
		# read config
		config = config or {}
		config.setdefault('encoding', DEF_ENCODE)
		config.update(k)
		
		# check config
		if self.debug > 0:
			trix.display(config)
		
		# config
		host = config['host']
		port = config['port']
		nick = self.nick = config['nick']
		
		# config (optional; defaults to: nick)
		user = self.user = config.get('user', self.nick).lower()
		ident = self.ident = config.get('ident', self.nick)
		
		#
		# plugin support
		#
		
		# if config lists any plugins, they'll be stored here
		self.plugins = {}
		
		# check for plugins that need to be created from config
		if 'plugins' in config:
			plug_conf = config.get('plugins', {})
			
			# loop through each name in the plug_conf dict
			for pi_name in plug_conf: 
				createpath = plug_conf[pi_name]['plugin'] # for `create`
				pluginname = pi_name
				pi_config  = plug_conf[pi_name]
				
				print("# plugin config: %s" % pi_name)
				trix.display(plug_conf)
				
				pi = trix.create(createpath, pi_config, self)
				self.plugins[pi_name] = pi
		
		#
		# initialize superclasses
		#  - Runner repeatedly calls the event loop `io`
		#  - Connect opens a connection to the server immediately
		#
		Runner.__init__(self, config, **k)
		Connect.__init__(self, (host, port))
		
		#
		# connection
		#
		user_line = "USER "+nick+' '+user+' '+host+' :'+ident
		nick_line = "NICK "+nick
		
		self.writeline(user_line)
		self.writeline(nick_line)
		
		if self.debug:
			print ("# user_line: %s" % user_line)
			print ("# nick_line: %s" % nick_line)
		
		#
		# start running so that io() gets called frequently
		#
		if k.get('run'):
			self.show = k.get('show', self.debug)
			if self.debug:
				print ("# Running %s" % (nick))
			Runner.run(self)
		else:
			if self.debug:
				print ("# Starting %s!%s@%s" % (nick, user, host))
			self.show = k.get('show', True)
			Runner.start(self)
		
		# 
		self.pi_update = time.time()
		self.pi_interval = config.get('pi_interval', PLUG_UPDT)
	
	
	#
	# IO
	#
	def io(self):
		
		# read all received text since last io;
		# might be multiple lines (or empty).
		intext = self.read()
		
		# if new lines exist...
		if intext:
			
			# split them...
			inlines = intext.splitlines()
			
			# ...and handle each line.
			for line in inlines:
				
				if line[0:4] == 'PING':
					if self.debug:
						print ("# ping")
					RESP = line.split()[1] # handle PING
					self.writeline('PONG ' + RESP)
					if self.debug:
						print ("# pong")
				else:
					self.on_message(line)  # handle everything besides PINGs
				
		# every now-n-then, call the plugins' `update` method
		if time.time() > (self.pi_update + self.pi_interval):
			
			# update to wait another `interval` seconds.
			self.pi_update = time.time()
			
			#print ("# plugins update; " + str(time.time()))
			for pname in self.plugins:
				try:
					self.plugins[pname]
					p.update()
				except Exception as ex:
					if self.debug:
						print("#")
						print("# Plugin Update Failed. Removing: %s" % pname)
						print("# Error: %s" % str(ex))
						print("#")
					del(self.plugins[pname])
	
	
	#
	# ON MESSAGE
	#
	def on_message(self, line):
		
		e = IRCEvent(line)
		
		# showing text
		if self.show or self.debug:
			print (e.text)
		
		# debugging 
		if self.debug > 1:
			trix.display(e.dict)
		
		# let each plugin handle each event (but not PINGs)
		for pname in self.plugins:
			p = self.plugins[pname]
			p.handle(e)
	
	
	#
	# STATUS
	#
	def status(self):
		s = {}
		s['ircconf'] = self.config
		s['runner'] = Runner.status(self)
		return s
