class Blueprint:
	"""Object class for the whole array of elemnts in blueprint"""
	def __init__(self, objects_array):
		self.objects = objects_array

	def calculate_objects(self):
		"""Calculate objects by name"""
		self.objects_list = {}
		for value in self.objects.values():
			if value["Имя"] not in self.objects_list:
				self.objects_list[value["Имя"]] = 1
			else:
				self.objects_list[value["Имя"]] += 1