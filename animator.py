'''

'''
import time
class Animator(object):
	"""docstring for Animator"""
	def __init__(self, data):
		super(Animator, self).__init__()
		self.initial_data = self.final_data = self.data = data
		self.end_time = self.start_time = time.time()

	def animate(self, final_data, animation_time):
		self.start_time = time.time()
		self.end_time = time.time() + animation_time
		self.initial_data = dict(self.data)
		self.final_data = final_data

	def update(self):
		ct = time.time()
		x = self.end_time -  ct
		if x <= 0.0: 
			for key in self.final_data:
				self.data[key] = self.final_data[key]
		else:
			for key in self.final_data:
				gradient = 1.0 * (self.final_data[key] - self.data[key]) / x
				self.data[key] = gradient * (ct - self.start_time) + self.data[key]
		self.start_time = ct
