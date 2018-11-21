#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.
#


"""
The solution to many problems may be in giving trix the ability to 
run as an application. Of course, it will still be usable as a 
programming library. It's just that the app-like features would also
be usable as applications, or features of trix-as-an-app.

First, trix-as-an-app would need a server by which cline commands
could (if their function required) pass information and control the
app in various ways. A "start" command might cause trix-as-an-app to
begin running. This would allow for easy "backgrounding" using &

    nohup python3 -m trix start &

I don't know how that might be accomplished on Windows, or whether 
it's even possible. Guess I need a windows expert for that.

ANYWAY...
Command-line (cline) call would remain the same except that features
meant to run a while could be started and added to a list of running
action items that share time allocated by a Runner(). Other cline 
features might stop, or otherwise alter such items.

Ideally an HTTP interface would be available, as well as some (better
than the existing) version of Console, for use on remote servers via
ssh.

So... not that the idea's been typed, it must be done. Here we go:
"""


from .. import *


class app(object):
	"""
	Using trix as an application.
	"""
	
	ConfigDir = DEF_CONFIG + "/trix/app"
	
	@classmethod
	def configdir(cls):
		"""Returns an `fs.Dir` object, the application config dir."""
		try:
			return cls.__configdir
		except:
			cls.__configdir = trix.path(cls.ConfigDir)
			return cls.__configdir
		
	@classmethod
	def configpath(cls, fpath):
		"""
		Pass the file path within the app config directory - usually 
		just a filename. Returns full file path.
		"""
		return cls.configdir.merge(fpath)
	
	@classmethod
	def jconfig(cls, fpath, **k):
		"""
		Pass a file path within the app config directory. Returns the
		a jconfig file containing the configuration.
		
		Keyword argument `default` or `ndefault` may specify the file 
		path (or inner path) to default content in case the config file 
		does not yet exist.
		
		The affirm kwarg defaults to 'touch'.
		"""
		k.setdefault('affirm', 'touch')
		return trix.jconfig(cls.configpath(fpath, **k))
	
	
	@classmethod
	def config(cls):
		"""Loads and stores application config."""
		try:
			return cls.__appconf
		except AttributeError:
			cls.__jconfig = cls.jconfig("app.conf")
			cls.__appconf = cls.__jconfig.obj
			return cls.__appconf
		
	
	@classmethod
	def start(cls):
		appconfig = cls.confpath.path
		cls.jconfig = trix.jconfig(appconfig, default=cls.defconfig)



