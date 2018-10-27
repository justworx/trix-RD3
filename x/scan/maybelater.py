#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under
# the terms of the GNU Affero General Public License.
#


from trix.x.scan import *


class Scanner_Plus_Ultra(Scanner):
	"""The Scanner for A Great Big Beautiful Tomorrow."""

	# PASS DELIMITERS
	def passdelim(self, delimiters, passwhite=True):
		
		#
		# I *think* there's no need to catch StopIteration because
		# self.ignore() - via passwhite - will handle that. However,
		# this is something to watch for.
		#
		while True:
			if passwhite:
				self.passwhite()
			if self.c.char not in delimiters:
				return
			else:
				self.passwhite()

