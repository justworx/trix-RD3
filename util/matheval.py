#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under the 
# terms of the GNU Affero General Public License.
#
#  - Evaluates mathematical text expressions and returns the 
#    result. Does NOT use the python eval() method, so it is
#    (hopefully) safe enough for use with expressions received
#    from unknown sources.
#  - This functionality will probably be absorbed into a bigger
#    evaluation system someday.
#

import ast, math, operator

# binary operators
BOPS = {
	ast.Add: operator.add,
	ast.Sub: operator.sub,
	ast.Mult: operator.mul,
	ast.Div: operator.div,
	ast.Pow: operator.pow,
	ast.Mod: operator.mod 
}

# unary operators
UOPS = {
	ast.USub: operator.neg,
	ast.UAdd: operator.pos
}

# variables from math module
NAMES = {
	'e' : math.e,
	'pi' : math.pi
}

# unwanted functions from math module
FN_BAD = ['fsum']

# relevant builtin functions
FN_GOOD = {
	'abs' : abs
}


#
#  *********  EVAL NODE  *********
#
def __eval(node, vars, fn):
	
	# EXPRESSION
	if isinstance(node, ast.Expression):
		return __eval(node.body, vars, fn)
	
	# NUMBER
	elif isinstance(node, ast.Num):
		return float(node.n)
	
	# BINARY OP:
	elif isinstance(node, ast.BinOp):
		op_type = type(node.op)
		if op_type in BOPS:
			return BOPS[op_type](
				__eval(node.left, vars, fn),
				__eval(node.right, vars, fn)
			)
		else:
			raise ValueError("invalid-binary-op", {
				'op': (type(node.op).__name__)
			})
	
	# UNARY OP:
	elif isinstance(node, ast.UnaryOp):
		op_type = type(node.op)
		if op_type in UOPS:
			return UOPS[op_type](__eval(node.operand, vars, fn))
		else:
			raise ValueError("invalid-unary-op", {
				'op': (type(node.op).__name__)
			})
	
	#
	# VARIABLES:
	# - Names of vars argument variables, or the e
	#   and pi from math module.
	#
	elif isinstance(node, ast.Name):
		if node.id in vars:
			return vars[node.id]
		elif node.id in NAMES:
			return NAMES[node.id]
		else:
			raise ValueError("invalid-variable", {
				'var': node.id
			})
	
	#
	# STRING:
	# - This is intended to support arguments to 
	#   functions that will eventually return a
	#   number. It has the affect of allowing 
	#   string operations, but I don't know of 
	#   any reason to prevent that, so I'll leave
	#   it here.
	#
	elif isinstance(node, ast.Str):
		return node.s
	
	#
	# ATTRIBUTE
	# - I suppose this would reintroduce the 
	#   dangers I went to all this trouble to
	#   avoid. I'm leaving it here so I won't
	#   forget how it's done. I recommend against 
	#   uncommenting this, though, unless you
	#   "know what you're doing".
	# - If I'm not mistaken, it will open your
	#   entire system up to anyone who can call
	#   the eval() function below.
	#
	#elif isinstance(node, ast.Attribute):
	#	attr = node.attr
	#	return getattr(__eval(node.value, vars, fn),attr)
	#
	
	#
	# FUNCTIONS:
	# - Handle the functions described in the math
	#   module and relevant builtin functions.
	#
	elif isinstance(node, ast.Call):
		if not isinstance(node.func, ast.Name):
			raise ValueError("invalid-function")
		
		if node.func.id == FN_GOOD:
			func = FN_GOOD[node.func.id]
		elif node.func.id in fn:
			func = fn[node.func.id]
		elif not node.func.id in FN_BAD:
			func = getattr(math, node.func.id, None)
		if func is None:
			raise ValueError("invalid-function", {
				'fn': (node.func.id)
			})
		
		if node.args is not None:
			args = [__eval(v, vars, fn) for v in node.args]
		else:
			args = []
		return func(*args)
	
	else:
		raise ValueError("invalid-node-type", {
			'nodetype': type(node).__name__
		})


#
# ********* EVAL *********
#
def eval(expr, vvars={}, fn={}):
	"""
	Use the eval() method to safely 
	evaluate a math expression given by
	the function's first argument. The 
	second optional argument is a dict 
	containing variables. The third 
	optional argument is a dict listing
	functions.
	
	The builtin abs() function and all 
	functions from the math module are 
	allowed except for fpow.
	
	The math module's e and pi variables
	are built-in defaults. They may be 
	replaced using the second argument.
	
	EXAMPLES:
	$ python
	>>> import util.eval as ev
	>>> ev.eval("x+1", {'x':2})
	3
	>>> fun = {
	...   'x' : lambda v: 'big!' if not v else 'bigger!'
	... }
	>>> ev.eval("x(isinf(99))", {}, fun)
	'big!'
	>>>
	>>> def half(n):
	...   return n/2.0
	...
	>>> ev.eval("fx(pi)", {}, {'fx':half})
	1.5707963267948966
	"""
	r = __eval(ast.parse(expr, mode='eval'), vvars, fn)
	try:
		if r == int(r):
			return int(r)
	except Exception:
		pass
	return r






