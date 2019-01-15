#!/bin/python2.7

import argparse
import csv
from naoqi import ALProxy


class Converter:

	def __init__(self):
		self.names = list()
		self.times = list()
		self.keys = list()

	def parse_motion_file(self, motion_file_location, webots_time_type):

		with open(motion_file_location) as motion_file:
			reader = csv.DictReader(motion_file, delimiter=',')
			# First populate the names list with all the name of the fields except WEBOTS_MOTION and V1
			# which are the two first
			self.names = reader.fieldnames[2:]
			# The naoqi requires the time slots for every field
			times_row = list()
			# Temporary store the values of each row because reader can only read once.
			rows = list()
			# Do one scan to all the rows to get the times slots
			for row in reader:
				# Activate this if the time is in type 00:00:000
				if webots_time_type:
					times_row.append(self.get_seconds(row['#WEBOTS_MOTION']))
				else:
					times_row.append(float(row['#WEBOTS_MOTION']))
				rows.append(row)

			# Re scan to fill the keys list
			for field in self.names:
				self.times.append(times_row)
				all_values_for_this_field = list()
				for row in rows:
					all_values_for_this_field.append(float(row[field]))

				self.keys.append(all_values_for_this_field)

	def get_seconds(self, time_str):
		m, s, ms = time_str.split(':')
		return float(m) * 60 + float(s) + float(ms) / 1000

	def get_lists(self):
		return self.names, self.times, self.keys


class Executor:

	def __init__(self, robot_ip, robot_port):
		self.motion = ALProxy("ALMotion", robot_ip, robot_port)
		# Uncomment if you want to initiate from a specific posture
		# self.posture = ALProxy("ALRobotPosture", robot_ip, robot_port)
		# self.posture.goToPosture("StandInit", 0.5)

	def run(self, names, times, keys):
		try:
			self.motion.angleInterpolation(names, keys, times, True)
		except BaseException, err:
			print err


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--ip", type=str, default="127.0.0.1", help="Robot ip address")
	parser.add_argument("--port", type=int, default=9559, help="Robot port number")
	parser.add_argument("--motionfile", type=str, help="Motion file")
	parser.add_argument("--webotstimetype", type=bool, default=False, help="Webots time type mm:ss:ms, default false")

	args = parser.parse_args()

	# Convert motion file and populate the 3 lists
	converter = Converter()
	converter.parse_motion_file(args.motionfile, args.webotstimetype)
	names, times, keys = converter.get_lists()

	# Execute to nao robot
	executor = Executor(args.ip, args.port)
	executor.run(names, times, keys)
