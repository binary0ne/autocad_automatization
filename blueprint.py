from __future__ import division 
import matplotlib.pyplot as plt
import math
import shapely
from shapely.geometry import LineString, Point

class Blueprint:
	"""Object class for the whole array of elemnts in blueprint"""
	def __init__(self, objects_array):
		self.objects = objects_array
		self.rooms = {}

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
			if value["Имя"] == "Линия":					
				if value["Начало X"]:
					y_start = float(value["Начало X"])
				if value["Начало Y"]:
					z_start = float(value["Начало Y"])
				if value["Конец Y"]:
					y_end = float(value["Конец X"])
				if value["Конец Z"]:
					z_end = float(value["Конец Y"])
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
			x2 = x1 + lenght * math.sin(math.radians(angle))
			y2 = y1 + lenght * math.cos(math.radians(angle))
			angle += increment
			ping_lines.append([x2, y2])
		#	plt.plot([x1, x2], [y1, y2])

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
		x = float(array['Положение X'])
		y = float(array['Положение Y'])
		intersections = self.ping_radius([x,y], int(5000), 16)
		
		# Find objects by intersections with lines builded from point of
		# position of a room label
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

		# Add lines found through intersections of already found ones
		int_points = []
		new_objects = True
		while new_objects:
			new_objects = False
			for wall_a in room_objects_list:
				local_intersections = 0
				outer_intersections = 0
				wall_a_params = self.lines[wall_a]
				l1 = LineString([(wall_a_params["start"]), (wall_a_params["end"])])
				for wall_b in room_objects_list:
					if wall_a != wall_b:
						wall_b_params = self.lines[wall_b]
						l2 = LineString([(wall_b_params["start"]), (wall_b_params["end"])])
						int_pt = l1.intersection(l2)
						if len(int_pt.coords) > 0:
							for x,y in list(int_pt.coords):
								local_intersections += 1
								int_point = [x, y]
								if int_point not in int_points:
									int_points.append(int_point)

				if local_intersections == 1:
					for parameter in [wall_a_params["start"], wall_a_params["end"]]:

						if parameter not in int_points:
							for outer_wall in self.lines.values():
								l2 = LineString([(outer_wall["start"]), (outer_wall["end"])])
								int_pt = l1.intersection(l2)
								if len(int_pt.coords) > 0:
									outer_intersections += 1
							if outer_intersections <= 2:
								int_points.append(parameter)

					for x1, y1 in int_points:
						compare_point = [x1, y1]
					for key, value in self.lines.items():
						points = [value["end"], value["start"]]
						if compare_point in points:
							if key not in room_objects_list:
								room_objects_list.append(key)
								new_objects = True

		array = {"corners": int_points, "walls": room_objects_list}
		return array

		#for x1, y1 in int_points:
		#	for x2, y2 in int_points:
		#		if [x1, y1] != [x2, y2]:
		#			plt.plot([x1, x2], [y1, y2])

		#for key, line in self.lines.items():
		#	if key in room_objects_list:
		#		line_x = (line["start"][0], line["end"][0])
		#		line_y = (line["start"][1], line["end"][1])
		#		# xmean = sum(i for i in line_x) / float(len(line_x))
		#		# ymean = sum(i for i in line_y) / float(len(line_y))
		#		plt.plot(line_x, line_y)
				# plt.annotate(key, xy=(xmean,ymean), xycoords="data")
		#print(array)
		#plt.show()

	def find_rooms(self):
		"""Method to find and list all rooms"""
		self.find_refferences()
		room_labels = self.objects_refferences["Номер помещения"]
		print("Found " + str(len(room_labels)) + " rooms, starting to identify them.")
		n = 0
		self.rooms = []
		for room_label in room_labels:
			print(room_label)
			room_elements = self.find_room(room_label)
			room_prefix = self.objects[room_label]["1"]
			room_number = self.objects[room_label]["01"]
			room_name = str(room_prefix) + str(room_number)
			room_elements["number"] = room_name
			self.rooms.append(room_elements)
			n += 1
			percent = int(n / len(room_labels) * 100)
			print(str(percent) + "%")
			
	def vizualize_room(self, room_number):
		"""Simple room plotting"""
		for room in self.rooms:
			if room["number"] == room_number:
				for key, line in self.lines.items():
					if key in room["walls"]:
						line_x = (line["start"][0], line["end"][0])
						line_y = (line["start"][1], line["end"][1])
				#		# xmean = sum(i for i in line_x) / float(len(line_x))
				#		# ymean = sum(i for i in line_y) / float(len(line_y))
						plt.plot(line_x, line_y)
						# plt.annotate(key, xy=(xmean,ymean), xycoords="data")
				print(room["corners"])
				#print(array)

		plt.show()

































