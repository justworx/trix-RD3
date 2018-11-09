#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.
#

import time

def loop(iterable, **k):
	"""
	What I want is some way to loop within a lambda. I think Param 
	may need a "loop()" method that:
	
	1) allows an executable argument to process items in, eg., p.v
	2) allows callback `done` to determine if the goal is reached
	
	Argument `iterable` may be any iterable object.
	
	Keyword arguments may be:
	 * proc - a callable object that processes every iter item
	 * done - a
	"""
	
	# if there's to be a return value, `result` is it
	result = None
	
	#
	# Pass sleep=<float: seconds> if a pause is needed between
	# iterations. This probably isn't ever needed except in odd cases
	# where the method is being used to perform some task rather than
	# to calculate a return value in a callback (eg, for Cursor)
	#
	sleep = k.get('sleep')
	
	#
	# The callable `proc` is not required, but it's probably going to
	# be the most commonly used in Cursor queries. It's purpose is to
	# incrementally calculate some value based on a series of passes
	# through a loop
	#
	proc = k.get('proc', None)
	
	#
	# done
	#
	done = k.get('done', None)
	
	try:
		for item in iter(iterable):
			
			if proc:
				result.append(proc(item))
			
			if callable(done:
				if done(item):
					return result[0] if len(result)==1 else result
					
			if sleep:
				time.sleep(sleep)
	
	except StopIteration:
		pass
	
	if result != None:
		return result
