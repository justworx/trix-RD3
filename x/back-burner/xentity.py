#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under 
# the terms of the GNU Affero General Public License.
#


#
# This looked like it was going to be necessary, but then later it
# looked like it's NOT going to be necessary. I guess I'll stow it
# here.
#


try:
	#py3
	from html.entities import *
except:
	#py2
	from htmlentitydefs import *

