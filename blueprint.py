import matplotlib.pyplot as plt

class Blueprint:
	"""Object class for the whole array of elemnts in blueprint"""
	def __init__(self, objects_array):
		self.objects = objects_array

	def count_objects(self):
		"""Calculate objects by name"""
		self.objects_list = {}
		for value in self.objects.values():
			if value["Имя"] not in self.objects_list:
				self.objects_list[value["Имя"]] = 1
			else:
				self.objects_list[value["Имя"]] += 1

	def find_refferences(self):
		"""Get objects refferences by name"""
		self.objects_refferences = {}
		for key, value in self.objects.items():
			if value["Имя"] not in self.objects_refferences:
				self.objects_refferences[value["Имя"]] = [key]
			else:
				self.objects_refferences[value["Имя"]].append(key)

	def generate_lines(self):
		"""Generating range of coordinates for a line"""
		self.lines = {}
		for key, value in self.objects.items():
			if value["Начало Y"]:
				y_start = float(value["Начало Y"])
			if value["Начало Z"]:
				z_start = float(value["Начало Z"])
			if value["Конец Y"]:
				y_end = float(value["Конец Y"])
			if value["Конец Z"]:
				z_end = float(value["Конец Z"])
			if y_start and z_start and y_end and z_end:
				self.lines[key] = {}
				self.lines[key]["start"] = [y_start, z_start]
				self.lines[key]["end"] = [y_end, z_end]

	def vizualize_lines(self):
		for line in self.lines.values():
			line_x = (line["start"][0], line["end"][0])
			line_y = (line["start"][1], line["end"][1])
			plt.plot(line_x, line_y)
		plt.show()

	def find_room(self, object_name):
		"""Find coordinates of a surrounding room and get its objects"""

