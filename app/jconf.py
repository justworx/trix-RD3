#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.
#


import ast
from ..util.dq import *
from ..util.enchelp import *
from ..fmt.jformat import *
from ..fs.file import *


class jconf(EncodingHelper):
	"""Json config file helper."""
	
	def __init__(self, path, default=None, **k):
		"""
		Pass config file path. If the file is not encoded "utf_8", you 
		must provide the encoding of the file (and optionally, errors)
		as keyword arguments.
		
		The config file is loaded imediately into memory and may be
		accessed using the self.obj property (which typically returns
		a dict or list object). If the file does not yet exist, an empty
		dict object is specified.
		
		NOTES:
		 * JSON is the default input format, but a file readable by 
		   `ast.literal_eval` may also be given as keyword arg `default`.
		   This provides an easy way to initialize a config file with
		   default contents.
		 * If `default` argument is given, its path points to an existing
		   file. The contents of the file (along with. any subsequent 
		   alterations) will replace any data in the file at `self.path` 
		   when the `self.save()` method is called.
		
		REMEMBER:
		 * The object loads both json and ast, but can only write JSON.
		 * The default file is  never written to by this class.
		"""
		
		k.setdefault('encoding', 'utf_8')
		EncodingHelper.__init__(self, **k)
		
		# basic variables
		self.__obj = None
		self.__path = path
		self.__def = default
		
		#
		# Read and parse config file, coppied from a default, if the
		# "default" kwarg specified a path.
		#
		# NOTE: kwargs get passed to the load method only on the first
		#       call, here from the constructor. After this, the default,
		#       if it exists, will have been read and the config will
		#       have been read (in the given encoding) and written in 
		#       utf8-encoded bytes.
		# ALSO: The self.__load() method sets the self.obj property.
		#
		self.__load(**k)
		
		# start with selection object on self.__obj
		self.__sel = self.__obj
		
	@property
	def dconfig(self):
		return self.__def
	
	@property
	def path(self):
		"""File path to this config file."""
		return self.__path
	
	@property
	def obj(self):
		"""The object loaded from this config file."""
		return self.__obj
	
	@property
	def sel(self):
		"""
		Reference another object within the self.obj. See self.select().
		"""
		return self.__sel
	
	
	# RELOAD
	def reload(self):
		"""Reload the last saved version of the config file."""
		self.__load()
	
	
	# SAVE
	def save(self, **k):
		"""Save the current self.obj to the json config file."""
		
		fmt = k.get('format', "display").lower()
		if fmt == 'display':
			conf = JDisplay().format(self.obj)
		elif fmt == 'compact':
			conf = JCompact.format(self.obj)
		elif fmt in ['json', None]:
			conf = JSON().format(self.obj)
		else:
			raise Exception('invalid-format-spec', xdata(
					use1=["display", 'compact', 'json', None]
				))
		
		
	
	
	
	#
	# MANIPULATION UTILS
	#
	
	# query/display
	def query(self, spec=None):
		"""
		Pass a list of nested keys (string) or offsets (int) leading to
		an object within self.obj. Pass None (or exclude argument) to
		reset selection to self.obj.
		
		NOTE: This method uses `util.dq` to retrieve objects within an
		      object. Always pass a list object as the `spec` argument.
		      Passing a delimited string will still work, but you will
		      probably, sooner or later, get unexpected results unless  
		      you *really* understand the "dirty version" of the dq 
		      class's path specification.
		"""
		return dq(self.obj, spec) if spec else self.obj
	
	def display(self, spec=None):
		"""Print this object to the terminal in JSON display format."""
		trix.display(self.query(spec))
	
	
	# select/displays
	def select(self, spec=None):
		"""Set the selection `sel` to the given item within `obj`."""
		self.__sel = self.query(spec)
	
	def displays(self, spec=None):
		"""Like `display`, but on the selected (`self.sel`) data."""
		trix.display (dq(self.sel, spec) if spec else self.sel)
	
	
	
	
	#
	# LOAD (on init)
	#
	def __load(self, default=None, **k):
		
		try:
		
			#
			# If constructor kwarg 'default' is given, read from that.
			# File will always be stored and saved at path `self.path`.
			#
			fpath = k.get('default', self.path)
			
			# In first call to load (from constructor), keyword arguments
			# are passed. If encoding and default are specified in kwargs,
			# they are used here. After the first call, `self.reload()`
			# may be used to restore self.obj to it's last-saved condition,
			# but it will have been previously saved in utf8 encoding and
			# the default (if it existed) will not be needed as it's been 
			# written to a newly created version of the config. 
			k = k or self.ek
			
			# 1 - read `path` file text; 'touch', if no such file.
			self.txt = Path(self.__path, affirm="touch").reader(**k).read()
			
			# 2 - now there's a `path` file, but it may be empty
			if not self.txt.strip():
				#
				# there's nothing in the config file...
				#
				
				# if there's no default file, return and empty dict
				if not self.__def:
					outf = File(self.path, encoding="utf_8", affirm='touch')
					outf.write("{}")
					self.__obj = {}
					return {}
				
				else:
					# A) read the default file's contents.
					self.txt = File(self.__def, encoding="utf_8").read()
					
					# B) write the default config to the file
					outf = File(self.path, encoding="utf_8", affirm='touch')
					outf.write(self.txt)
					
		
			# 3 - load json to the data object, `self.__obj`
			# try with ast (in case loading a default given in ast).
			try:
				self.__obj = ast.literal_eval(self.txt)
			except:
				compile(self.txt, fpath, 'eval') #try to get a line number
				raise
		
		# DEBUGGING!
		except IsADirectoryError as ex:
			raise type(ex)(ex.args, xdata(
				fpath=fpath, k=k, txt=self.txt, path=self.path, 
				dfile=self.__def
			))
		
		except BaseException as ast_ex:
			# fallback on json, which will work for both "default" and
			# for config files passed as the constructor argument.
			try:
				self.__obj = json.loads(self.txt)
			except BaseException as json_ex:
				raise Exception ("config-read-error", xdata(
					path = fpath, pathk = k,
					json = {"type" : type(json_ex), "args" : json_ex.args},
					ast = {"type" : type(ast_ex), "args" : ast_ex.args}
				))
