#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under
# the terms of the GNU Affero General Public License.
#


from . import *


class IRCLog(IRCPlugin):
	"""Log IRC chat conversations."""
	
	def __init__(self, config=None, *a, **k):
		"""Pass logging config; encoding and logfile."""
		
		IRCPlugin.__init__(self, config, *a, **k)
		
		self.logfile = self.config.get('logfile', LOG_PATH)
		self.lend    = self.config.get('logendl', LOG_ENDL)
		
		p = trix.path(self.logfile, affirm='touch')
		print ("\n\n# log_path: %s\n#\n" % p.path)
		
		w = p.wrapper(**self.ek)
		self.writer = w.writer()
		self.writer.seekend()
	
	
	
	def __del__(self):
		try:
			# make sure the log gets flushed when this object closes.
			if self.writer:
				self.writer.flush()
		except:
			pass
	
	
	
	def handle(self, e):
		ts = time.strftime("%Y:%m:%d %H:%I:%S")
		log_line = "%s\t<%s>\t%s%s" % (ts, e.nick, e.text, self.lend)
		self.writer.write(log_line)
	
	
	
	def update(self):
		# flush new entries to the log file
		self.writer.flush()
		




