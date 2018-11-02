#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under
# the terms of the GNU Affero General Public License.
#


import operator


class oper(object):
	"""Built-in operations set to strings (for evaluation)."""
	
	def __init__(self, **k):
		"""
		Pass optional kwarg `ops` as a dict with keys naming methods from
		the operator module. 
		
		Default is `OPERATORS` - all available operators.
		"""
		self.__ops = k.get('ops', OPERATORS)
		self.__call__ = self.call
	
	def call(self, op, *a):
		return self.__ops[op](*a)
	
	def operators(self, opers):
		self.__ops = {}
		for o in opers:
			pass





#
# ALL OPERATORS
#

OPERATORS = {
	
	operator.__abs__      : [1,"math","abs"], # abs(a).
	operator.__inv__      : [1,"bits","~"  ], # ~a.
	operator.__invert__   : [1,"bits","~"  ], # ~a.
	operator.__neg__      : [1,"math","-"  ], # -a.
	operator.__not__      : [1,"bool","not"], # not a.
	operator.__pos__      : [1,"math","+"  ], # +a.
	
	operator.__add__      : [2,"math","+"  ], # a + b
	operator.__and__      : [2,"bits","&"  ], # a & b
	operator.__concat__   : [2,"math","+"  ], # a + b  (sequences)
	operator.__contains__ : [2,"bool","in" ], # b in a 
	operator.__eq__       : [2,"comp","==" ], # a == b
	operator.__ge__       : [2,"comp",">=" ], # a >= b
	operator.__gt__       : [2,"comp",">"  ], # a > b
	operator.__iadd__     : [2,"math","+=" ], # a += b
	operator.__iand__     : [2,"bits","&=" ], # a &= b
	operator.__iconcat__  : [2,"math","+=" ], # a += b (sequences)
	operator.__ilshift__  : [2,"bits","<<="], # a <<= b
	operator.__imod__     : [2,"math","%=" ], # a %= b
	operator.__imul__     : [2,"math","*=" ], # a *= b
	operator.__ior__      : [2,"bits","|=" ], # a |= b
	operator.__ipow__     : [2,"math","**="], # a **= b
	operator.__irshift__  : [2,"bits",">>="], # a >>= b
	operator.__isub__     : [2,"math","-=" ], # a -= b
	operator.__ixor__     : [2,"bits","^=" ], # a ^= b
	operator.__le__       : [2,"comp","<=" ], # a <= b
	operator.__lshift__   : [2,"bits","<<" ], # a << b
	operator.__lt__       : [2,"comp","<"  ], # a < b
	operator.__mod__      : [2,"math","%"  ], # a % b
	operator.__mul__      : [2,"math","*"  ], # a * b
	operator.__ne__       : [2,"comp","!=" ], # a != b
	operator.__or__       : [2,"bits","|"  ], # a | b
	operator.__pow__      : [2,"math","**" ], # a ** b
	operator.__rshift__   : [2,"bits",">>" ], # a >> b
	operator.__sub__      : [2,"math","-"  ], # a - b
	operator.__truediv__  : [2,"math","/"  ], # a / b
	operator.__xor__      : [2,"bits","^"  ]  # a ^ b
}

# cross-version division
try:
	OPERATORS[operator.__div__]       = [2,"/=" ,"math"] # a /= b
except:
	OPERATORS[operator.__itruediv__]  = [2,"/=" ,"math"] # a /= b
	OPERATORS[operator.__ifloordiv__] = [2,"//=","math"] # a //= b



#
# KEYS
#  - separate operators by number of arguments expected
#
OPKEY_1 = []
OPKEY_2 = []

for k in OPERATORS:
	if OPERATORS[k][0] == 1:
		OPKEY_1.append(OPERATORS[k])
	elif OPERATORS[k][0] == 2:
		OPKEY_2.append(OPERATORS[k])


#
# OPERATOR SETS
#
OP_BITS = []
OP_BOOL = []
OP_COMP = []
OP_MATH = []


try:
	for k in OPERATORS:
		if OPERATORS[k][1] == "bits":
			OP_BITS.append(OPERATORS[k])
		elif OPERATORS[k][1] == "bool":
			OP_BOOL.append(OPERATORS[k])
		elif OPERATORS[k][1] == "comp":
			OP_COMP.append(OPERATORS[k])
		elif OPERATORS[k][1] == "math":
			OP_MATH.append(OPERATORS[k])
except Exception as ex:
	raise
	"""
	from ... import * # trix, for xdata ; remove after debugging
	raise type(ex)(ex.args, xdata(
			k=k, op_k=OPERATORS[k]
		))
	"""
