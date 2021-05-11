import os

import datetime
import threading
import json
import Pyro4
import sys
import shutil
import time
import pyautogui
import time


from .ProjectController import ProjectController
from pathlib import Path
from .Event import Event, Auditd, Clicks, Keypresses, Traffic, TrafficThroughput, Timed, Suricata
from PyQt5.QtWidgets import *


class Validator():
	def __init__(self, timeout, script_path, terminal):
		self.eceld = Pyro4.Proxy("PYRONAME:ecel.service")
		self.timeout = timeout
		self.script_path = script_path
		self.code_index = 0
		self.terminal = terminal
		
		# Sets up the validation_temp folder path to store eceld data for validation
		op = ProjectController.get_project_directory()
		folder_name = Path("validation_temp/")
		self.output_path = os.path.join(op,folder_name)

		# get write and read access to dir
		if not os.access(os.getcwd(), os.W_OK):
			os.chmod(os.getcwd(), stat.S_IWUSR)

		if not os.path.exists(self.output_path):
				os.mkdir(self.output_path)	

		# read script files
		try:
			self.json_script = json.load(open(script_path + "Validator.json", 'r'))
			self.executable_script = open(script_path + ".py", 'r').read().split("\n")
		except FileNotFoundError as e:
			print(e)

		# executing imports does not actually add imports to runtime
		for item in self.executable_script:
			self.code_index += 1
			if len(item) <= 0:
				break
			else:
				print(item)
				exec(self.executable_script[self.code_index - 1])

	def validate(self):
		self.eceld.remove_data()
		self.eceld.start_collectors()	

		try:
			for item in self.json_script:
				# The system sleeps for the delta time of the event before running it through the validator loop
				dt = datetime.datetime.strptime(item["Time"], '%H:%M:%S')
				delta_time = datetime.timedelta(hours=dt.hour, minutes=dt.minute, seconds=dt.second)
				time.sleep(delta_time.total_seconds())
				self.validator_loop(item)
				
		except TimeoutError as e:
			print(e)

		self.eceld.stop_collectors()
		self.parse_eceld(None)

	def validator_loop(self, item):
		print(self.executable_script[self.code_index])
		
		# If the event is an action, execute it
		if item['v'] == "action":
			exec(self.executable_script[self.code_index])
			self.print_progress("Executed: action at line {}\n".format(self.code_index))
			self.code_index += 1
		else:
			# Otherwise, start the timer for the timeout
			timer = datetime.datetime.now()
			cpTimer = datetime.timedelta(hours=timer.hour, minutes=timer.minute, seconds=timer.second)

			while True:
				self.print_progress("Checking: " + item["Type"] + ": " + item["Attributes"] + "\n")
				# Check observation. self.parse_eceld(item) will return True if the validator validates the ovservation
				if self.parse_eceld(item):
					break
				now = datetime.datetime.now()
				cpNow = datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second)
				print("cp Now ", cpNow)
				print("cpTimer ", cpTimer)
				# Otherwise, if self.parse_eceld(item) keeps returning False, it will timeout
				if cpTimer - cpNow < datetime.timedelta(seconds=self.timeout):
					self.print_progress("Script execution timed out after {} seconds\n".format(self.timeout))
					raise TimeoutError("Script execcution timed out after {0} seconds.".format(self.timeout))
		

		if len(item['Children']) > 0:
			for child in item['Children']:
				if "action" in child['v']:
					self.code_index += 1
				self.validator_loop(child)
				dt = datetime.datetime.strptime(item["Time"], '%H:%M:%S')
				delta_time = datetime.timedelta(hours=dt.hour, minutes=dt.minute, seconds=dt.second)
				time.sleep(delta_time.total_seconds())


	def parse_eceld(self, item):
		# remove previously parsed information
		shutil.rmtree(self.output_path)
		os.mkdir(self.output_path)

		# parse eceld data at this point
		self.eceld.parse_data_all()
		self.eceld.export_data(self.output_path)

		# checks observation
		if item is not None:		
			return self.check_obs(item)
		return False
			
	def check_obs(self, item):
		obs = item["Attributes"]
		print("obs ", obs)

		# get eceld_export unique name
		for root, subdirs, files in os.walk(self.output_path):
			for d in subdirs:
				if 'ecel-export' in d:
					export = d
		export = self.output_path + "/" + export

		# Checks system calls
		if item["Type"] == "auditd_id":
			return self.check_auditd(export, obs)

		# Checks network traffic
		elif item["Type"] == "traffic_all_id":
			return self.check_traffic(export, obs)
		return False
	
	# Checks system calls
	def check_auditd(self, export, obs):
		with open(export + "/parsed/auditd/auditdData.JSON") as f:
			data = json.load(f)
			print("data ", data)
			for event in data:
				print("event ", event)
				for key in event:
					print("key ", key)
					if type(obs) == type(event[key]):
						print("compare obs: ", obs)
						print("compare data: ", event[key])
						try:
							if obs in event[key]:
								print("MATCH", obs, event[key])
								self.print_progress("MATCH " + obs + " " + event[key] + "\n")
								return True
						except TypeError:
							if obs == event[key]:
								print("MATCH", obs, event[key])
								self.print_progress("MATCH " + obs + " " + event[key] + "\n")
								return True
							else:
								print("NO MATCH")
								return False
		return False

	# Checks network traffic
	def check_traffic(self, export, obs):
		with open(export + "/parsed/tshark/networkDataAll.JSON") as f:
			data = json.load(f)
			print("data ", data)
			for event in data:
				print("event ", event)
				for key in event:
					print("key ", key)
					if type(obs) == type(event[key]):
						print("compare obs: ", obs)
						print("compare data: ", event[key])
						try:
							if obs in event[key]:
								print("MATCH", obs, event[key])
								self.print_progress("MATCH " + obs + " " + event[key] + "\n")
								return True
						except TypeError:
							if obs == event[key]:
								print("MATCH", obs, event[key])
								self.print_progress("MATCH " + obs + " " + event[key] + "\n")
								return True
							else:
								print("NO MATCH")
								return False
		return False

	def print_progress(self, text):
	    cursor = self.terminal.textCursor()
	    cursor.movePosition(cursor.End)
	    cursor.insertText(text)
	
	def stop(self):
		self.eceld.stop_collectors()
		self.json_script = None
		self.executable_script = None