

## x.pq

The `pq` class wraps a dict or list object, and provides a set of 
methods that allow for manipulation of the data in interesting ways.


A fairly typical-looking use of pq might go something like this:

    >>> from trix.x.pq import *
    >>> q = pq([1,2,3,4,5])
    
    # use wrapped list functions to affect the object
    >>> q.append(9)
    
    # use the `o` property to access the object directly
    >>> q.o # [1, 2, 3, 4, 5, 9]
    
    # access list items
    >>> q[3] # 4


The basics are pretty much the same as using an actual List object, 
but pq contains several additional methods that might turn out to be
very useful.

The `each`, `select`, and `update` methods each accept an executable
object (eg, lambda, function, or method...) to which a Param object -
see trix.data.param - is given as the first argument. This provides
an easy way to query and/or maniputlate list and dict objects with
very little effort.

```
from trix.x.pq import *

```

# grrr... gotta go. more to come later.

