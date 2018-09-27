#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under
# the terms of the GNU Affero General Public License.
#

import sys, time, traceback, json
try:
	import thread
except:
	import _thread as thread


AUTO_DEBUG = True
DEF_CONFIG = "~/.config/%s"
DEF_LOGLET = "./loglet"
DEF_ENCODE = 'utf_8'
DEF_INDENT = 2
VERSION    = 0.0000


class trix(object):
	"""Utility, debug, import; object, thread, and process creation."""
	
	__m  = __module__
	__mm = {}
	
	Logging = 0 #-1=print; 0=None; 1=log-to-file
	
	# ---- object creation -----
	
	# INNER PATH	
	@classmethod
	def innerpath(cls, innerPath=None):
		"""
		Prefix `innerPath` with containing packages.
		
		Return a string path `innerPath` prefixed with any packages that
		contain this module. If the optional `innerPath` is None, the path
		to (and including) this package is returned.
		"""
		p = '.%s' % (innerPath) if innerPath else ''
		if cls.__m:
			return "%s%s" % (cls.__m, p)
		else:
			return innerPath
	
	
	# MODULE
	@classmethod
	def module (cls, path):
		"""
		Returns a module given a string `path`. Specified module may be 
		external to the package in which this class is defined.
		"""
		try:
			# If the `path` module has already been imported, return it.
			return cls.__mm[path]
		
		except KeyError:
			
			# import the module and add it to cls.__mm
			mod = __import__(path)
			
			# split the module path into a list
			pathList = path.split('.')
			
			# accumulate module heirarchy p1.p2.p3...
			# ...preset the first item.
			pa = [pathList[0]]
			
			# The root module should be preset in cls.__mm before beginning
			# the loop.
			cls.__mm[pathList[0]] = cur = mod
			
			# append each additional path element's module
			for pe in pathList[1:]:
				
				# Append each path element to pa list. The first time through
				# pe will be "p1.p2" (because p1 is already preset, above).
				# Each additional pass will add the next path element.
				pa.append(pe)
				
				# Reset the `cur`	variable to the module named by the current
				# path element `pe`. 
				cur = cur.__dict__[pe]
				
				# Now set the current accumulated path (pa) as a dot-separated
				# string key in the cls.__mm dict, with the current module as
				# the value.
				if not pe in cls.__mm:
					cls.__mm[".".join(pa)] = cur
			
			# return the module
			return cur	
	
	
	# N-MODULE
	@classmethod
	def nmodule(cls, innerPath):
		"""Like `module`, but pass the inner path instead of full path."""
		return cls.module(cls.innerpath(innerPath))
	
	
	# CREATE
	@classmethod
	def create(cls, path, *a, **k):
		"""
		Create and return an object specified by argument `path`. 
		
		The dot-separated path must start with the path to the desired
		module. It must be suffixed with a name of a class defined in the
		specified module. (Eg, 'package.subpackage.module.ClassName')
		
		Any additional arguments and keyword args will be passed to the
		class's constructor.
		"""
		p = path.split(".")
		m = p[:-1] # module
		o = p[-1]  # object
		
		try:
			if m:
				mm = cls.module(".".join(m))
				T  = mm.__dict__[o]
			else:
				T = __builtins__[o]
		
		except KeyError:
			raise KeyError('create-fail', xdata(path=path,
					mod=".".join(m), obj=o
				))
		
		try:
			return T(*a, **k)
		except BaseException as ex:
			raise type(ex)(xdata(path=path, a=a, k=k, obj=o))
		
	
	# N-CREATE - create an object given path from inside trix
	@classmethod
	def ncreate(cls, innerPath, *a, **k):
		"""
		Create and return an object specified by argument `innerPath`.
		The dot-separated path must start with the path to the desired
		module *within* this package (but NOT prefixed with the name of
		this package. It must be prefixed with a name of a class defined
		in the specified module. Eg, 'subpackage.theModule.TheClass
		
		Any additional arguments and keyword args will be passed to the
		class's constructor.
		
		USE: The ncreate() method is used from within this package. For 
		     normal (external) use, use the create() method.
		"""
		a = a or []
		k = k or {}
		return cls.create(cls.innerpath(innerPath), *a, **k)
	
	
	# VALUE - return a value (by name) from a module
	@classmethod
	def value(cls, pathname, *args, **kwargs):
		"""
		Returns an object as specified by `pathname` and additional args.
		
		Returns a module, class, function, or value, as specified by the
		string argument `pathname`. If additional *args are appended, 
		they must name a class, method, function, or value defined within 
		the object specified by first argument. A tupel is returned.
		
		eg..
		trix.value('socket',"AF_INET","SOCK_STREAM")
		"""
		try:
			mm = mc = cls.module(pathname)
		except:
			# If `pathname` points to a module or function, split it and 
			# load its containing module.
			pe = pathname.split('.')
			
			# only pop the last item if there's more than one element
			nm = pe.pop() if len(pe) > 1 else None
			
			# get the module
			mm = cls.module('.'.join(pe))
			
			# Get the last object specified by `pathname `; This object must
			# be either a module or a class, not a function or other value.
			# If no other args are specified, this is the final result.
			mc = mm.__dict__[nm] if nm else mm
		
		# If there are no *args, return the last [module or class] object
		# specified by `pathname`.
		if not args:
			return mc
		
		# if args are specified, forget about the mod/cls item and just
		# return any requested values from it.
		rr = []
		for v in args:
			try:
				rr.append(mc.__dict__[v])
			except KeyError:
				if 'default' in kwargs:
					return kwargs['default']
				return ()
			except NameError:
				# TO DO:
				# Make this work when `v` is a module. It does work if the
				# module `v` would specify is already loaded, but not if it's
				# not... which is inconsistent... which bothers me.
				raise
		
		# If one *args value was specified, return it. If more than one
		# was specified, return them as a tuple.
		if len(rr) == 1:
			return rr[0]
		return tuple(rr)
	
	
	# N-VALUE
	@classmethod
	def nvalue(cls, pathname, *a, **k):
		"""Like `value`, but pass the inner path instead of full path."""
		return cls.value(cls.innerpath(pathname), *a, **k)
	
	
	
	# ---- process/thread creation -----
	
	# POPEN
	@classmethod
	def popen (cls, *a, **k):
		"""
		Open a subprocess and return a Popen object created with the given
		args and kwargs. This functions exactly as would calling the popen
		function directly, except that stdout and stderr are enabled by 
		default.
		
		The return value is a Popen object. Use its communicate() method
		to read results of the command.
		
		KWARGS REFERENCE:
		bufsize=0, executable=None, stdin=None, stdout=None, stderr=None, 
		preexec_fn=None, close_fds=False, shell=False, cwd=None, env=None,
		universal_newlines=False, startupinfo=None, creationflags=0
		"""
		try:
			m = cls.__sp
		except:
			m = cls.__sp = cls.module("subprocess")
		
		# set defaults and run the process
		k.setdefault("stdout", m.PIPE)
		k.setdefault("stderr", m.PIPE)
		return m.Popen(*a, **k)
	
	
	# PID
	@classmethod
	def pid(cls):
		"""Return the id for this process."""
		try:
			return cls.__pid
		except:
			import os
			cls.__pid = os.getpid()
			return cls.__pid
	
	
	# PROCESS
	@classmethod
	def process(cls, path, *a, **k):
		"""
		Pass a class `path` and any needed args/kwargs. A Process object
		is returned. Call the Process object's `launch` method passing a
		method name (string) and any additional args/kwargs (or no params,
		if the class constructor starts processing).
		"""
		# REM! `path` is the module.class to launch within the `Process`.
		return cls.ncreate("util.process.Process", path, *a, **k)
	
	
	# N-PROCESS
	@classmethod
	def nprocess(cls, innerPath, *a, **k):
		"""Like `process`, but given remote object's `innerPath`."""
		#
		# The `innerPath` arg is expanded to be the full module.class 
		# path that will be launched by `cls.process()`.
		#
		return cls.process(cls.innerpath(innerPath), *a, **k)
	
	
	# START - Start new thread 
	@classmethod
	def start (cls, x, *a, **k):
		"""
		Start executable object `x` in a new thread, passing any given 
		*args and **kwargs.
		"""
		try:
			thread.start_new_thread(x, a, k)
		except:
			try:
				import thread
			except:
				import _thread as thread 
			thread.start_new_thread(x, a, k)
	
	
	# ---- general -----
	
	# PROXIFY
	@classmethod
	def proxify(cls, obj):
		try:
			return cls.create('weakref.proxy', obj)
		except BaseException:
			return obj
	
	
	# J-PARSE
	@classmethod
	def jparse(cls, jsonstr, **k):
		"""Parse json to object."""
		try:
			return json.loads(jsonstr)
		except TypeError:
			k.setdefault('encoding', DEF_ENCODE)
			return json.loads(jsonstr.decode(**k))
		
	
	# K-COPY
	@classmethod
	def kcopy(cls, d, keys):
		"""
		Copy `keys` from `d`; return in a new dict.
		
		Creates a subset of dict keys in order to select only desired (or 
		allowed) keyword args before passing to functions and methods. 
		Argument `keys` may be passed as a space-separated string. If the
		dict object contains non-string keys, pass `keys` as a list.
		"""
		try:
			keys=keys.split()
		except:
			pass
		return dict([[k,d[k]] for k in keys if k in d])
	
	
	# K-POP
	@classmethod
	def kpop(cls, d, keys):
		"""
		Remove `keys` from `d`; return in a new dict.
		
		Remove and return a set of `keys` from given dict. Argument `keys`
		may be passed as a space-separated string. If the dict object 
		contains non-string keys, pass `keys` as a list. 
		
		Missing keys are ignored.
		
		NOTE: The dict `d` that you pass to this method is affected.
		      Specified keys will be removed and returned in a separate
		      dict.
		"""
		try:
			keys=keys.split()
		except AttributeError:
			pass
		r = {}
		for k in keys:
			if k in d:
				r[k] = d[k]
				del(d[k])
		return r
	
	
	# PATH
	@classmethod
	def path(cls, *a, **k):
		"""Return a new fs.Path object with given args and kwargs."""
		try:
			return cls.__FPath(*a, **k)
		except:
			# requires full module path, so pass through innerpath()
			cls.__FPath = cls.module(cls.innerpath('fs')).Path
			return cls.__FPath(*a, **k)
	
	
	
	# ---- display/debug -----
	
	# DEBUG
	@classmethod
	def debug(cls, debug=True, showtb=True):
		"""Enable/disable debugging/traceback."""
		Debug.debug(debug,showtb)
	
	
	# FORMATTER (default, JDisplay)
	@classmethod
	def formatter(cls, *a, **k):
		"""Return `data` in display format."""
		fmt = k.pop('fmt', 'fmt.JDisplay')
		return cls.ncreate(fmt, *a, **k)
	
	
	# DISPLAY - Util. JSON is the main data format within the package.
	@classmethod
	def display(cls, data, *a, **k):
		"""Print json data in display format."""
		cls.formatter(*a, **k).output(data)

	
	# TRACE-BK
	@classmethod
	def tracebk(cls):
		"""Return current exception's traceback as a list."""
		tb = sys.exc_info()[2]
		if tb:
			try:
				return list(traceback.extract_tb(tb))
			finally:
				del(tb)
	
	
	# X-DATA
	@classmethod
	def xdata(cls, data=None, **k):
		"""Package extensive exception data into a dict."""
		return xdata(cls, data, **k)
	
	
	
	
	# ---- LOGGING -----
	
	# LOG
	@classmethod
	def log(cls, *a, **k):
		"""Returns Loglet for this process. Pass args/kwargs to log."""
		if cls.Logging < 0:
			with thread.allocate_lock():
				a = list(a)
				a.append(k)
				cls.display(a)
		elif cls.Logging > 0:
			with thread.allocate_lock():
				try:
					cls.__log(*a, **k)
				except:
					cls.__log = cls.ncreate('util.loglet.Loglet', cls.__m)
					cls.__log(*a, **k)
		



#
# CONVENIENCE
#
create    = trix.create
debug     = trix.debug
display   = trix.display
innerpath = trix.innerpath
jparse    = trix.jparse
kcopy     = trix.kcopy
kpop      = trix.kpop
log       = trix.log
module    = trix.module
ncreate   = trix.ncreate
nmodule   = trix.nmodule
nprocess  = trix.nprocess
nvalue    = trix.nvalue
path      = trix.path
pid       = trix.pid
popen     = trix.popen
process   = trix.process
proxify   = trix.proxify
start     = trix.start
tracebk   = trix.tracebk
value     = trix.value





#
# LOADER (and NLoader)
#
class Loader(object):

	def __init__(self, module, value=None, loader=trix.module):
		"""
		Pass module name (string) and function name (string). Loading of
		module is deferred until the first call.
		"""
		self.__L = loader
		self.__M = module
		self.__V = value
	
	def __repr__(self):
		T = type(self)
		aa = (
			T.__name__, self.__L.__name__, self.__M, repr(self.__V)
		)
		return "<%s trix.%s('%s', %s)>" % aa
	
	@property
	def module(self):
		"""Return the module object as specified to construcor."""
		try:
			return self.__module
		except AttributeError:
			self.__module = self.__L(self.__M) # use loader
			return self.__module
	
	@property
	def value(self):
		"""Return the value specified to construcor."""
		try:
			return self.__value
		except AttributeError:
			self.__value = self.module.__dict__[self.__V]
			return self.__value

	def __call__(self, *a, **k):
		"""Load the specified method/function and return its result."""
		self.__call__ = self.value
		return self.__call__(*a, **k)

	def __getitem__(self, x):
		"""Get any member (function, value, etc...) from the module."""
		return self.module.__dict__[x]


# N-LOADER
class NLoader(Loader):
	def __init__(self, module, value=None):
		"""Init loader with the trix.nmodule loader."""
		Loader.__init__(self, module, value, loader=trix.nmodule)


#
# COMPATABILITY
#

# common python 2/3 typedefs
try:
	basestring
except:
	#
	# The following are defined if basestring is undefined (before 
	# python 2.3, and for python 3 and higher). These values make the
	# important distinction between unicode and byte values/strings.
	# These designations are important in some rare cases.
	#
	basestring = unicode = str
	unichr = chr
	
	# Convence for development.
	if AUTO_DEBUG:
		try:
			try:
				from importlib import reload
			except:
				from imp import reload
		except:
			pass



#
# For implementations with unicode support compiled without wide 
# character support, this allows comparison of wide characters. 
# This should solve many problems on pre-python3 Windows systems.
#
try:
	unichr(0x10FFFF) # check wide support
except:
	import struct
	def unichr (i):
		return struct.pack('i', i).decode('utf-32')



#
# This supports python versions before 2.6 when the bytes type was 
# introduced.
#
try:
	bytes
except:
	# this only happens pre-version 2.6
	bytes = str



#
# EXTENDED DEBUGGING
#  - This package provides extensive debugging information in raised
#    exceptions, so a little extra formatting is needed to help make
#    sense of some of the things that might go wrong.
#
class xdata(dict):
	"""Package extensive exception data into a dict."""

	def __init__(self, data=None, **k):

		# argument management
		data = data or {}
		data.update(k)

		# create and populate the return dict
		self['xdata'] = data
		self.setdefault('xtime', time.time())

		# If this is a current exception situation,
		# record its values
		try:
			tblist = None
			xtype, xval = sys.exc_info()[:2]
			tblist = trix.tracebk()
			if xtype or xval or tblist:
				self['xtype'] = xtype
				self.__xtype  = xtype
				self['xargs'] = xval.args
				if tblist:
					self['xtracebk'] = list(tblist)
		finally:
			if tblist:
				del(tblist)
				tblist = None



#
# DEBUG HOOK
#
def debug_hook(t, v, tb):
	
	with thread.allocate_lock():

		# catch errors in the debug hook and disable debugger
		try:
			
			# KEYBOARD ERROR
			if isinstance(v, KeyboardInterrupt):
				print ("\n\n", t, "\n\n")

			else:
				print (t)

				# SYNTAX ERROR
				if isinstance(v, SyntaxError):
					print(" ->", str(type(v)))

				#
				# DISPLAY ARGS
				#
				if v.args:
					try:
						trix.display(v.args, sort_keys=1)
					except Exception:
						args = [str(a) for a in v.args]
						print ("[")
						if len(v.args)==1:
							print (" ", str(v.args))
						else:
							for a in v.args:
								try:
									print("  %s" % str(a))
								except:
									print ("  ", a)
						print ("]")

				#
				# TRACEBACK
				#  - show traceback, if enabled
				#
				if tb and Debug.showtb():
					print ("Traceback:")
					traceback.print_tb(tb)
				print ('')
			
		#
		# EXCEPTION IN EXCEPTION HANDLER
		#
		except BaseException:
			print ("\n#\n# DEBUG HOOK FAILED!")
			try:
				xxtype, xxval = sys.exc_info()[:2]
				print ("# - Debug Hook Err: %s %s\n#" % (xxtype, str(xxval)))
			except:
				pass
			
			# turn off debugging and re-raise the exception
			debug(False)
			print ("# - Debug Hook is Disabled.")
			raise
		finally:
			if tb:
				del(tb)
				tb = None


#
# DEBUG
#
class Debug(object):
	__DEBUG = False
	__TRACE = False
	__SYSEX = sys.excepthook
	
	@classmethod
	def debug(cls, debug=True, showtb=False, **k):
		cls.__DEBUG = bool(debug)
		cls.__TRACE = bool(showtb)
		if cls.__DEBUG:
			sys.excepthook = debug_hook
		else:
			sys.excepthook = cls.__SYSEX
	
	@classmethod
	def debugging(cls):
		return cls.__DEBUG
	
	@classmethod
	def showtb(cls):
		return cls.__TRACE



if AUTO_DEBUG:
	Debug.debug(1,1)


