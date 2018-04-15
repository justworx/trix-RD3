#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.
#


from . import * # trix, sys


class MainArgs(object):
	"""Parse command line arguments."""
	
	def __init__(self, args):
		self.args = []
		self.krgs = {}
	
		for a in args:
			if a[:2]=="--":
				kv = a[2:].split("=")
				self.krgs[kv[0]] = kv[1] if len(kv)>1 else True
			else:
				self.args.append(a)



if __name__ == '__main__':

	# program args
	app = sys.argv[0]
	cmd = sys.argv[1] if len(sys.argv) > 1 else ''
	args = sys.argv[2:]

	derr = {}
	try:
		# parse main args
		mak = MainArgs(args)
		derr['main-args'] = mak
		
		if False:
			pass
		
		
		#
		# VERSION
		#
		elif cmd in ['-v', 'version']:
			version = dict(
				version   = VERSION,
				copyright = "Copyright (C) 2018 justworx",
				license   = 'agpl-3.0'
			)
			trix.display(version)
			#print ("trix version: %s" % VERSION) 
		
		
		#
		# PORTSCAN
		#
		elif cmd in ['portscan']:
			print ("Scanning local ports...")
			n = trix.ncreate('util.network.Host')
			r = n.portscan() 
			trix.display(r)
		
		
		#
		# TEST - Load all package modules; Test key features.
		#
		#if cmd == 'test':
		#	from trix.dev import test
		#	test.report(**mak.krgs)
		#
		
		
		#
		#
		# LAUNCH
		#
		#
		elif cmd == 'launch':
			
			#
			# TEST ERROR HANDLING
			#
			#
			#raise Exception('test-error')
			#
			
			try:
				# --- unpack object args and load module ---
				
				d_meth = d_dict = d_type = d_obj = None
				obj = ca = ca64 = clsname = clsargs = clskrgs = None
				methname = methargs = methkrgs = None
				
				#
				# COMPACT ARGS
				# expand the first argument, a compact b64 json (array) string
				#
				ca64 = trix.ncreate('fmt.JCompact').expand(mak.args[0])
				derr['compact-args'] = ca64
				
				#
				# ALL ARGS
				# convert compressed args/krgs to an array
				#
				ca = trix.jparse(ca64.decode('UTF8'))
				derr['all-args'] = ca
				
				#
				# CLASS ARGS
				# 3 args required (for object creation)
				#  - c = class - a string fit for `trix.create`
				#  - a = args  - class constructor args...
				#  - k = kwargs  ...and kwargs
				#
				clsname,clsargs,clskrgs = ca[0:3]
				derr['class-args'] = (clsname,clsargs,clskrgs)
				
				#
				# THIS IS THE OBJECT (eg, 'net.server.Server')
				#
				obj = trix.create(clsname, *clsargs, **clskrgs)
				
				#
				# METHOD ARGS
				# Unpack method args and load module:
				#   - m  = method (of object `o`) to call
				#   - ma = method args
				#   - mk = method kwargs
				#
				methname,methargs,methkrgs = ca[3:6]
				derr['method-args'] = (methname,methargs,methkrgs)
				
				
				#
				# build and call the object's specified method
				#  - DEBUGGING: track the building of `meth`
				#
				if methname:
					
					d_obj = obj
					d_type = type(obj)
					d_dict = d_type.__dict__
					d_meth = methname
					
					# get the actuall method object as `methname`
					try:
						meth = dict(type(obj).__dict__)[methname]
					except Exception as ex:
						raise
				
					#
					# CALL THE METHOD!
					#
					meth(obj, *methargs, **methkrgs)
					
					#
					# When `meth()` exits, execution ends. Until then,
					# we're stuck in the line above (meth(obj,...)
					#
			
			except BaseException as ex:
				
				trix.log ('MAIN: BaseException', str(ex), ex.args)
				
				# group arguments for easier reading of exception
				xmeth = dict(
						methargs=methargs, methkrgs=methkrgs,
						d_meth=d_meth, d_type=d_type, d_obj=d_obj
					)
				xparams = dict(
						app=app, cmd=cmd, args=mak.args, kwargs=mak.krgs, 
					)
				
				# package the exception into a dict
				errdict = dict(
					message = "err-launch-fail",
					x_args = ex.args,
					x_meth = xmeth,
					x_params = xparams,
					x_type = type(ex),
					derr = derr, 
					obj = obj,
					mapprxy = d_dict, 
					tracebk = trix.tracebk()
				)
				
				# JCompact the dict and write it to stderr as a json string
				#jc = trix.ncreate('fmt.JDisplay') # debugging
				jc = trix.ncreate('fmt.JCompact')
				sys.stderr.write(jc(errdict))
				
				trix.log ('\n\nMAIN: end BaseException')
			
		
		
		#
		#
		# UNHANDLED COMMANDS
		#
		#
		else:
			raise ValueError("invalid-command")
	
	
	#
	# debugging - add argument info to the exception
	#
	except BaseException as ex:
		trix.log ('\n\nMAIN: Enclosing Exception', str(ex))
		try:
			#
			# WHY IS THIS RAISED IN A TRY/EXCEPT BLOCK?
			#  - Raising in this try/except block causes an exception with a
			#    "prior" exception, which adds to the understanding of what
			#    took place.
			#  - It may cause some exceptions to contain duplicate data, but
			#    will prevent loss of information in other cases.
			#
			raise type(ex)(ex.args, xdata(
				app=app, cmd=cmd, args=mak.args, kwargs=mak.krgs
			))
		except:
			raise type(ex)(ex.args, xdata(app=app, cmd=cmd))
	

