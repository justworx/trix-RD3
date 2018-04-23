"""
Copyright 2018 justworx
This file is part of the trix project, distributed under the terms 
of the GNU Affero General Public License.
"""

import os

from ... import *


TESTDIR = os.path.normpath("%s/../testfiles"%str(__file__))


def report(debug=False):
	"""
	Loads all modules and prints a report listing modules and a brief
	error message, if any.
	"""
	
	#
	# TEST - IMPORT ALL
	#
	print ("\n\n*\n* DEV TEST: Import all modules:\n*\n")
	tt = Test(debug)
	tt.load()
	tt.report()
	
	#
	# TEST - FS WRAPPER IO
	#
	"""
	print ("\n\n*\n* DEV TEST: fs.wrapper() write/read:\n*\n")
	tt = TestFS(debug)
	
	#print (" * filenames: %s" % '; '.join(tt.filenames()))
	grid = trix.ncreate('fmt.grid.Grid')
	
	print ("\n** Make Files...")
	grid.output(tt.makefiles())
	
	print ("\n** Read Files...")
	grid.output(tt.readfiles())
	
	print ("\nReader Files...")
	grid.output(tt.readerfiles())
	"""



# -------------------------------------------------------------------
#
# TEST-FS - Test File Wrappers, Readers and write methods.
#
# -------------------------------------------------------------------
class TestFS(object):
	
	def __init__(self, debug=False):
		self.debug = debug
	
	DATA = u"1, 2, 3\n4, 5, 6\n7, 8, 9\n"	
	
	def filenames(self):
		
		f = ['test.txt','test.csv']
		c = ['gz','bz2']
		b = ['tar', 'zip']
		
		rr = []
		rr.extend(f)
		rr.extend([
			'.'.join([x,y]) for x in f for y in b
		])
		
		r = []
		r.extend(rr)
		r.extend([
			'.'.join([x,y]) for x in rr for y in c
		])
				
		return r
	
	
	
	def readfiles(self, debug=False):
		
		# work with a Dir object
		d = trix.ncreate('fs.dir.Dir', TESTDIR, affirm='makedirs')
		rr = [['FILE:','MEMBER:','WRAPPER:','READER:','READLINE:']]
		for fname in self.filenames():
			
			p = trix.ncreate('fs.Path', d.merge(fname))
			
			xl = fname.split('.')
			mem = '.'.join(xl[:2])
			
			r = None
			try:
				# look for wrappers that require a `member`
				if xl[-1] in ['tar','zip','tgz']:
					w = p.wrapper(encoding=DEF_ENCODE)
					r = w.reader(member=mem)
					rr.append([
						fname, mem, type(w).__name__, type(r).__name__, 
						str(r.readline()).strip()
					])
				
				# wrappers that don't want `member`
				else:
					mem = None
					w = p.wrapper(encoding=DEF_ENCODE)
					r = w.reader()
					rr.append([
						fname, mem, type(w).__name__, type(r).__name__, 
						str(r.readline()).strip()
					])
					
			except Exception as ex:
				rr.append([
					fname, mem, type(w).__name__, type(r).__name__, 
					str("ERROR! %s" % str(ex))
				])
				if self.debug:
					raise type(ex)('test-fail', xdata(detail='readfiles',
						file=fname, member=mem, wrapper=w, reader=r
					))
		
		return rr
	
	
	
	
	
	"""
	"""
	def readerfiles(self, debug=False):
		
		# work with a Dir object
		d = trix.ncreate('fs.dir.Dir', TESTDIR, affirm='makedirs')
		rr = [['FILE:','MEMBER:','WRAPPER:','READER:','READLINE:']]
		for fname in self.filenames():
			
			time.sleep(0.1)
			
			p = trix.ncreate('fs.Path', d.merge(fname))
			
			xl = fname.split('.')
			mem = '.'.join(xl[:2])
			
			r = None
			try:
				# look for wrappers that require a `member`
				if xl[-1] in ['tar','zip','tgz']:
					w = p.wrapper(encoding=DEF_ENCODE) #INFO-ONLY
					r = p.reader(encoding=DEF_ENCODE, member=mem)
					rr.append([
						fname, mem, type(w).__name__, type(r).__name__, 
						str(r.readline()).strip()
					])
				
				# wrappers that don't want `member`
				else:
					mem = None
					w = p.wrapper(encoding=DEF_ENCODE) #INFO-ONLY
					r = p.reader(encoding=DEF_ENCODE)
					rr.append([
						fname, mem, type(w).__name__, type(r).__name__, 
						str(r.readline()).strip()
					])
					
			except Exception as ex:
				rr.append([
					fname, mem, type(w).__name__, type(r).__name__, 
					str("ERROR! %s" % str(ex))
				])
				if self.debug:
					raise type(ex)('test-fail', xdata(detail='readerfiles',
						file=fname, member=mem, wrapper=w, reader=r
					))
		
		return rr
	
	
	
	
	
	def makefiles(self, debug=False):
		
		# work with a Dir object
		d = trix.ncreate('fs.dir.Dir', TESTDIR, affirm='makedirs')
		
		# remove any existing files before testing
		d.search(".", "*.*", fn=d.rm)
		
		# loop through each filename writing data
		rr = [["FILENAME:", 'MEMBER:', 'RESULT:', 'ERROR:']]
		for fname in self.filenames():
			p = trix.ncreate('fs.Path', d.merge(fname), affirm='touch')
			
			try:
				xl = fname.split('.')
				
				# look for wrappers that require a `member`
				if xl[-1] in ['tar','zip','tgz']:
					mem = '.'.join(xl[:2])
					wrap = p.wrapper(encoding=DEF_ENCODE)
					wrap.write(mem, self.DATA)
					rr.append([fname, mem, 'OK.', ''])
				
				# wrappers that don't want `member`
				else:
					mem = None
					#print ("wrapper utf8 %s" % fname)
					wrap = p.wrapper(encoding=DEF_ENCODE)
					#print (repr(wrap))
					wrap.write(self.DATA)
					rr.append([fname, mem, 'OK.', ''])
			
			except Exception as ex:
				rr.append([fname, mem, "ERROR!", str(ex)])
				if self.debug:
					raise type(ex)('test-fail', xdata(
						detail='test.TestFS.readfiles',
						file=fname, path=str(p), member=mem, wrapper=wrap
					))
		
		return rr






# -------------------------------------------------------------------
#
# TEST - LOAD ALL MODULES
#
# -------------------------------------------------------------------
class Test(object):
	def __init__(self, debug=False):
		
		self.debug = debug
		
		# the directory holding the root package (eg, ~/dev, ~, etc...)
		self.parent = trix.path().path
		self.parlen = len(self.parent.split('/'))
		
		# the start of the import path (eg, dev.trix, dev.trix)
		self.inpath = trix.innerpath()
		
		# path elements within root package (eg, ['dev','trix'], etc...)
		inpathlist = self.inpath.split('.')
		
		# the name of this package
		self.package = inpathlist[-1]
		
		# path within the root package (eg, dev/trix, dev/trix)
		self.pkgpath = "/".join(inpathlist)
		
		# path to the package being tested (eg, trix, trix)
		self.path = "%s/%s" % (self.parent, self.pkgpath)
		
		# a Dir object to path containing *.py files to test
		self.dir = trix.ncreate('fs.dir.Dir', self.path)
		
		# CURRENTLY LOADED MODULES
		self.__loaded = {}
	
	
	
	#
	# RESULT STORAGE
	#
	
	@property
	def current(self):
		return self.__loaded
	
	
	#
	# MODULE PATHS - eg., "./trix/fs/dir.py"
	#
	
	@property
	def paths(self):
		"""Return list of *.py paths within package."""
		try:
			return self.__paths
		except:
			self.__paths = sorted(self.dir.find("*.py"))
			return self.__paths
	
	def pathgen(self):
		"""Generator for module (/full/dir/*.py) paths."""
		for path in self.paths:
			yield path
	
	
	#
	# MODULE SPEC - eg., "trix.fs.dir"
	#
	
	@property
	def modules(self):
		"""Return list of module (python.import.path) sepcifications"""
		try:
			return self.__modules
		except:
			self.__modules = sorted(self.modgen())
			return self.__modules
			
	
	def modgen(self):
		"""Generator for module (python-import) paths."""
		plen = self.parlen
		for path in self.paths:
			# path from within parent directory
			r = path.split('/')
			r = r[plen:] 
			
			# ignore files that start with x_
			if r[-1][:2]=='x_':
				continue
			
			# ignore init files, import their package path
			if r[-1] == '__init__.py': 
				r = r[:-1]
			
			# don't test __main__.py
			elif r[-1] != '__main__.py':
				
				# drop the .py where found at the end of module paths
				r[-1] = r[-1].split('.')[0]
				
				# yield the module name!
				p = '.'.join(r)
				
				# don't test a tester!
				if self.__module__ != r:
					yield p
	
	
	#
	# MODULE LOADING
	#
	
	def loadmodule(self, modspec):
		"""Import the module specified by `modspec`."""
		
		L = locals()
		G = globals()

		try:
			# for root module
			if modspec:
				m = __import__(modspec,G,L,[],0)
				
			# import (or reload) the modspec module
			elif modspec in self.__loaded:
				m = reload(self.__loaded[modspec])
			else:
				m = __import__(modspec,G,L,[],0)
			
			# store result
			self.__loaded[modspec] = dict(modspec=modspec, module=m)
			
		except BaseException as ex:
			self.__loaded[modspec] = dict(modspec=modspec, module=None, 
				error=xdata()
			)
			if self.debug:
				print ("modspec = %s" % modspec)
				raise
	
	
	
	def load(self):
		for modspec in self.modules:
			self.loadmodule(modspec)
	
	
	
	def report(self):
		if not len(self.current):
			self.load()
		
		gg = [["MODULE:", 'RESULT:']]
		for modspec in self.current:
			item = self.current[modspec]
			gg.append([
				modspec, "Loaded" if item.get('module') else "ERR! %s" % (
					str(item.get('error',{}).get('prior',{}).get('xargs', '?'))
				)
			])
		
		grid = trix.ncreate('fmt.grid.Grid')
		grid.output(gg)
