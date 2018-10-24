"""
Fast Forward!

>>> from ff import *
>>> x = ff([2,1,3])
>>> x
<ff 'list'>

>>> x(list.append, 4)
<ff 'list'>
>>> x.o
[2, 1, 3, 4]

>>> x(sorted).o
[1, 2, 3, 4]
>>> x(reversed).o
<list_reverseiterator object at 0x7f5a4da71ac8>
>>> list(x(reversed).o)
[4, 3, 1, 2]
>>> list(x(reversed).o)
[4, 3, 1, 2]
>>> list(x(sorted)(reversed).o)
[4, 3, 2, 1]

"""

from trix import *
from trix.util.wrap import *


class ff(Wrap):
	
	def __init__(self, o):
		Wrap.__init__(self, o)
	
	def __call__(self, fn, *a, **k):
		return ff(fn(self.o, *a, **k))
	
	def each(self, fn, *a, **k):
		r = []
		for x in self.o:
			r.append(fn(x, *a, **k))
		return ff(r)
	
	
	# --- utility ---
	
	@property
	def param(self):
		"""
		Return the Param type from data.param. This is available here
		because Param objects are very useful for parameter evaluation, 
		but may be needed only rarely.
		"""
		try:
			return self.__Param
		except:
			self.__Param = trix.nvalue('data.param.Param')
			return self.__Param


"""
THIS IS COPIED FROM JQUERY DOC...
  Should be some good ideas here for methods to go along with `each`.
  There are probably several here... parents, children, at least...
  that could be useful for recursively searching dict keys or lists
  within lists... Might need some kind of selection class in order to 
  implement such a thing...


add() 	Adds elements to the set of matched elements
addBack() 	Adds the previous set of elements to the current set
andSelf() 	Deprecated in version 1.8. An alias for addBack()
children() 	Returns all direct children of the selected element
closest() 	Returns the first ancestor of the selected element
contents() 	Returns all direct children of the selected element (including text and comment nodes)
each() 	Executes a function for each matched element
end() 	Ends the most recent filtering operation in the current chain, and return the set of matched elements to its previous state
eq() 	Returns an element with a specific index number of the selected elements
filter() 	Reduce the set of matched elements to those that match the selector or pass the function's test
find() 	Returns descendant elements of the selected element
first() 	Returns the first element of the selected elements
has() 	Returns all elements that have one or more elements inside of them
is() 	Checks the set of matched elements against a selector/element/jQuery object, and return true if at least one of these elements matches the given arguments
last() 	Returns the last element of the selected elements
map() 	Passes each element in the matched set through a function, producing a new jQuery object containing the return values
next() 	Returns the next sibling element of the selected element
nextAll() 	Returns all next sibling elements of the selected element
nextUntil() 	Returns all next sibling elements between two given arguments
not() 	Returns elements that do not match a certain criteria
offsetParent() 	Returns the first positioned parent element
parent() 	Returns the direct parent element of the selected element
parents() 	Returns all ancestor elements of the selected element
parentsUntil() 	Returns all ancestor elements between two given arguments
prev() 	Returns the previous sibling element of the selected element
prevAll() 	Returns all previous sibling elements of the selected element
prevUntil() 	Returns all previous sibling elements between two given arguments
siblings() 	Returns all sibling elements of the selected element
slice() 	Reduces the set of matched elements to a subset specified by a range of indices
"""
