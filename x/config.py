#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.
#


import ast, json
from ..fs.file import *
from ..fs.dir import Dir
from ..fmt import JDisplay


class Config(Dir, EncodingHelper):
	"""
	This thing is a lot of fun, but it's not very intuitive and not at
	all business as usual. I've had it here a good long while and never
	had the gumption to use it, so I'll set it aside (in trix.x) for 
	now and try to come up with something better.
	"""
	
	DefPath = "~/.config/"
	
	def __init__(self, path=None, **k):
		"""
		Pass optional `path` to base config directory. If None, defaults
		to '~/.config/' plus trix.innerpath() converted to directory path.
		"""
		k.setdefault('encoding', DEF_ENCODE)
		EncodingHelper.__init__(self, **k)
		
		mpath = trix.innerpath().replace('.','/')
		dpath = path or "%s%s" % (self.DefPath, mpath)
		k['affirm'] = 'makedirs'
		Dir.__init__(self, dpath, **k)
		
		self.__mpath = mpath
		self.__dpath = dpath
		self.__config = {}
	
	
	def __str__(self):
		return JDisplay().format(self)
	
	# CONTAINS - for dict-like behavior
	def __contains__(self, key):
		return key in self.__config
	
	# DEL ITEM - for dict-like behavior
	def __delitem__ (self, key):
		del(self.__config[key])
		
	# GET ITEM - for dict-like behavior
	def __getitem__(self, key):
		return self.__config[key]
	
	# SET ITEM - for dict-like behavior
	def __setitem__(self, key, value):
		self.__config[key] = value
	
	# ITER
	def __iter__(self):
		return iter(sorted(self.__config.keys()))
	
	# LEN
	def __len__(self):
		return len(self.__config)
	
	# KEYS
	def keys(self):
		"""List of config files open in this object."""
		return list(self.__config.keys())
	
	def update(self, path, d):
		"""Update the configuration for the given path."""
		self.config[path].update(d)
	
	def setdefault(self, path, key, value):
		"""
		Set the default value for the given path/key to `value`, where
		`path` is the path to a file within the config directory and `key`
		is (or becomes) a key in that config dict. 
		"""
		self.config.setdefault(path, {})
		self.config[path].setdefault(key, value)
	
	def get(self, key, default=None):
		"""Works like dict.get()"""
		return self.__config.get(key)
	
	
	@property
	def config(self):
		"""
		Returns the full config dict. Each open config file is included,
		it's path (within the config directory) is the key to a dict with
		the configuration data.
		"""
		return self.__config
	
	@property
	def modpath(self):
		"""
		The module path, ending with 'trix', prefixed by a dot-separated
		list of packages that contain the trix package.
		"""
		return self.__mpath
	
	@property
	def dirpath(self):
		"""
		The directory path (full or partial) as given to the constructor.
		"""
		return self.__dpath
	
	
	# FILE PATH
	def filepath(self, path):
		"""
		Returns the given `path` merged with this object's directory path.
		"""
		return Path(self.dirpath).merge(path)
		#return "%s/%s" % (self.dirpath, path)
	
	
	# DISPLAY
	def display(self, value=None, **k):
		"""Display the full config dict as returned by `self.config`."""
		trix.display(value or self.config, **k)
	
	
	
	
	
	def open(self, path):
		"""
		Pass the path to a config file within the config directory. It 
		will be loaded into into a dict accessible by the `self.config` 
		property.
		"""
		fpath = self.filepath(path)
		try:
			txt = Path(fpath).reader(**self.ek).read()
			#txt = File(fpath).read(**self.ek)
		except ValueError:
			txt = "{}"
			File(fpath, affirm="touch").write(txt, **self.ek)
		except BaseException as ex:
			raise type(ex)(ex.args, xdata(fpath=fpath))
		
		try:
			try:
				conf = ast.literal_eval(txt)
			except:
				compile(txt, fpath, 'eval') #try to get a line number
				raise
		except BaseException as ast_ex:
			try:
				conf = json.loads(txt)
			except BaseException as json_ex:
				raise Exception ("config-read-error", xdata(
					path = fpath, pathk = k,
					json = {"type" : type(json_ex), "args" : json_ex.args},
					ast = {"type" : type(ast_ex), "args" : ast_ex.args}
				))
		
		# store config
		self.__config[path] = conf
		
	
	
	def save(self, path=None):
		"""
		Save (write) the value in `self.config` whose key matches `path`.
		If `path` is None, each value is written to its respective file.
		"""
		if path:
			txt = JDisplay().format(config[path])
			File(self.filepath(path), affirm="touch").write(txt, **self.ek)
		else:
			for path in self.config:
				txt = JDisplay().format(self.config[path])
				File(self.filepath(path), affirm="touch").write(txt,**self.ek)
	
	
	