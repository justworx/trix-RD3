	
class JustAnIdea(object):
	"""just an idea..."""
	
	# EVAL
	@classmethod
	def eval(cls, x, **k):
		"""Evaluate with ast literal eval; fallback on jparse."""
		try:
			return cls.module('ast').literal_eval(x)
		except:
			return cls.jparse(x)
