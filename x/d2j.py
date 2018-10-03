#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.
#

# UNDER CONSTRUCTION

from .. import *

def jdoc(npath):
	"""	Export object __doc__ to json."""
	
	v = nvalue("app.jconf.jconf")
	d = dict(v.__dict__)
	r = {}
	for k in d:
		if ("__" not in k):
			r[k] = d[k].__doc__.strip()
	
	trix.display(r)

