#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.
#


from ... import *
from trix.util.urlinfo import *


def report(**k):
	
	print ("\n#\n# URL-INFO\n#")
	
	
	#
	# STRING URL
	#
	ui = urlinfo("http://localhost:8080/foo/bar.html?a=b#cde")
	rr = {
		"password": "",
		"netloc": "localhost:8080",
		"port": 8080,
		"username": "",
		"host": "localhost",
		"wrap": False,
		"query": "a=b",
		"path": "/foo/bar.html",
		"fragment": "cde",
		"scheme": "http"
	}
	if ui.dict != rr:
		raise Exception("FAIL!", xdata(
			url="http://localhost:8080/foo/bar.html?a=b#cde"
		))
	
	print ("str: OK")
	
	
	#
	# INT
	#
	rr = {
	  "wrap": False,
	  "host": "",
	  "port": 9999
	}
	if urlinfo(9999).dict != rr:
		raise Exception("FAIL!", xdata(url=9999))
	
	print ("int: OK")

	
	#
	# TUPLE
	#
	rr = {'port': 9999, 'host': 'localhost', 'wrap': False}
	if urlinfo(('localhost',9999)).dict != rr:
		raise Exception("FAIL!", xdata(url=('localhost',9999)))
	
	print ("tuple: OK")

