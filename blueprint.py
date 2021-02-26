from __future__ import division 
import matplotlib.pyplot as plt
import math
import shapely
from shapely.geometry import LineString, Point

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
			if value["Имя"] == "МЛиния":					
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
			elif value["Стиль печати"] == "АР - Стены" and value["Имя"] == "Линия":
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
		"""Builds visual of the blueprint"""
		for key, line in self.lines.items():
			line_x = (line["start"][0], line["end"][0])
			line_y = (line["start"][1], line["end"][1])
			# xmean = sum(i for i in line_x) / float(len(line_x))
			# ymean = sum(i for i in line_y) / float(len(line_y))
			plt.plot(line_x, line_y)
			# plt.annotate(key, xy=(xmean,ymean), xycoords="data")

		plt.show()

	def ping_radius(self, xy_coords, lenght, lines):
		"""Pings all nearby objects"""
		ping_lines = []
		x1 = xy_coords[0]
		y1 = xy_coords[1]
		angle = 0
		increment = 360 / lines
		while angle < 360:
			x2 = x1 + lenght * math.cos(angle)
			y2 = y1 + lenght * math.sin(angle)
			angle += increment
			ping_lines.append([x2, y2])
#			plt.plot([x1, x2], [y1, y2])

		# Intersection snippet from 
		# https://stackoverflow.com/
		# questions/20677795/
		# how-do-i-compute-the-intersection-point-of-two-lines
		array = {}
		line_n = 0
		for x2, y2 in ping_lines:
			array[line_n] = []
			l1 = LineString([(x1, y1), (x2, y2)])
			for key, line_b in self.lines.items():
				l2 = LineString([(line_b["start"]), (line_b["end"])])
				int_pt = l1.intersection(l2)
				if len(int_pt.coords) > 0:
					x = int_pt.x
					y = int_pt.y
					r = [x, y]
					array[line_n].append([key, r])
			line_n += 1

		return array

	def find_room(self, object_name):
		"""Find coordinates of a surrounding room and get its objects"""
		array = self.objects[object_name]
		x = float(array['Положение Y'])
		y = float(array['Положение Z'])
		intersections = self.ping_radius([x,y], float(50000), 360)
		
		found_objects = {}
		for key, value in intersections.items():
			objects = {}
			for obj_name, ispoint in value:
				end_x = ispoint[0]
				end_y = ispoint[1]
				dist = math.hypot(end_x - x, end_y - y)
				objects[dist] = obj_name
			found_objects[key] = objects
		
		room_objects_list = []

		for key, distances in found_objects.items():
			distances_list = []
			for distance in distances:
				distances_list.append(distance)
			if len(distances_list) > 0 and distances[(min(distances_list))] not in room_objects_list:
				room_objects_list.append(distances[(min(distances_list))])

		for key, line in self.lines.items():
			if key in room_objects_list:
				line_x = (line["start"][0], line["end"][0])
				line_y = (line["start"][1], line["end"][1])
				# xmean = sum(i for i in line_x) / float(len(line_x))
				# ymean = sum(i for i in line_y) / float(len(line_y))
				plt.plot(line_x, line_y)
				# plt.annotate(key, xy=(xmean,ymean), xycoords="data")

		plt.show()

	
































