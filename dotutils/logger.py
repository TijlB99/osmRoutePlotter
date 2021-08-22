
class SimpleLogger():
	def __init__(self, verbose=False):
		self.verbose = verbose

	def log(self, str):
		if self.verbose:
			print(str)
