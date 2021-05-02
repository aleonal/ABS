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

# TEST ON KALI, SHOULD WORK
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
		
		# TEST ON KALI, SHOULD WORK TODO: change this to project folder
		#self.output_path = os.getcwd() + "/validation_temp/"
		# I think we should make this folder automatically from the beginning like the events folder 
		# it's storing but not creating the folder
		# for now just create the folder in the project
		op = ProjectController.get_project_directory()
		folder_name = Path("validation_temp/")
		self.output_path = os.path.join(op,folder_name)

		# get write and read access to dir
		if not os.access(os.getcwd(), os.W_OK):
			os.chmod(os.getcwd(), stat.S_IWUSR)

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
				self.validator_loop(item)
				dt = datetime.datetime.strptime(item["Time"], '%H:%M:%S')
				delta_time = datetime.timedelta(hours=dt.hour, minutes=dt.minute, seconds=dt.second)
				time.sleep(delta_time.total_seconds())
				
		except TimeoutError as e:
			print(e)

		self.eceld.stop_collectors()

		# IF YOU WANT TO TEST ECELD WORKING CORRECTLY, UNCOMMENT THIS LINE
#		self.parse_eceld()

	def validator_loop(self, item):
		print(self.executable_script[self.code_index])
		
		if item['v'] == "action":
			exec(self.executable_script[self.code_index])
			self.print_progress("Executed: action at line {}\n".format(self.code_index))
			self.code_index += 1
		else:
			timer = datetime.datetime.now()

			while True:
				self.print_progress("Checking: " + item["Type"] + "\n")
				#ADDED SELF.CHECK_OBS(ITEM)
				if self.parse_eceld():# and self.check_obs(item):
					break

				if datetime.datetime.now() - timer < datetime.timedelta(seconds=self.timeout):
					raise TimeoutError("Script execcution timed out after {0} seconds.".format(self.timeout))
		

		if len(item['Children']) > 0:
			for child in item['Children']:
				if "action" in child['v']:
					self.code_index += 1
				self.validator_loop(child)
				dt = datetime.datetime.strptime(item["Time"], '%H:%M:%S')
				delta_time = datetime.timedelta(hours=dt.hour, minutes=dt.minute, seconds=dt.second)
				time.sleep(delta_time.total_seconds())


	def parse_eceld(self):
		# remove previously parsed information
		shutil.rmtree(self.output_path)
		os.mkdir(self.output_path)

		# parse eceld data at this point
		self.eceld.parse_data_all()
		self.eceld.export_data(self.output_path)

		#TODO: check observations. Currently defaults to True, but it must be a conditional
	        #Implemented in separate method below	
		return True
	'''
	#TODO: Need a way to open the eceld_export... folder		
	def check_obs(self, item):
		obs = item["Attribute"]
		#with open(self.output_path/"validation_temp"/eceld_export.../parsed/tshark/networkDataAll.JSON) as f:
		data = json.load(f)
		for d in data:
		    for key in d:
			if type(obs) == type(d[key]):
			    try:
				if obs in d[key]:
				    print("MATCH", obs, d[key])
			    except TypeError:
				if int(obs) == d[key]:
				    print("MATCH", obs, d[key]
			    else:
				pass
	'''
	def print_progress(self, text):
	    cursor = self.terminal.textCursor()
	    cursor.movePosition(cursor.End)
	    cursor.insertText(text)


#	def __init__(self):
#		self.eceld = Pyro4.Proxy("PYRONAME:ecel.service")
#		self.output_path = os.getcwd() + "/validation_temp/"
#		self.start_time = None
#		self.validating = False
#		self.events = []
#
#		if not os.access(os.getcwd(), os.W_OK):
#			os.chmod(os.getcwd(), stat.S_IWUSR)
#
#	def validation_loop(self, timeout):
#		self.eceld.remove_data()
#		self.eceld.start_collectors()
#		self.validating = True
#
#		while True:
#			if not os.path.exists(self.output_path):
#				os.mkdir(self.output_path)				
#
#			if self.start_time == None:
#				self.start_time = datetime.datetime.now()
#			else:
#				if datetime.datetime.now() - self.start_time >= datetime.timedelta(seconds=timeout):
#					print("Script validation timed out ({0} seconds)".format(timeout))
#					self.validating = False
#					return
#
#			shutil.rmtree(self.output_path)
#			os.mkdir(self.output_path)
#
#			self.eceld.stop_collectors()
#			self.eceld.parse_data_all()
#			self.eceld.export_data(self.output_path)
#			self.import_files(output_path)
#
#			for item in self.events:
#				print(item)
#
#	def import_files(self):
#		print("importing files")
#		directories = ["/parsed/auditd/auditdData.JSON", "/parsed/pykeylogger/click.JSON", "/parsed/pykeylogger/keypressData.JSON", "/parsed/pykeylogger/timed.JSON", "/parsed/tshark/networkDataAll.JSON", "/parsed/tshark/networkDataXY.JSON", "/parsed/suricata/suricata.JSON"]
#		type = ["auditd", "clicks", "keypresses", "timed", "traffic", "trafficThroughput", "suricata"]
#		self.events = []
#		
#		try:
#			for i in range(len(directories)):
#				with open(self.output_path + directories[i]) as f:
#					data = json.load(f)
#					
#					for d in data:
#						e = d
#						if type[i] == "auditd":
#							obj = Auditd(e['auditd_id'], e['content'], "auditd", e['start'])
#						elif type[i] == "clicks":
#							basename = os.path.basename(e['content'])
#							e['content'] = os.path.join(output_path, "raw/pykeylogger/click_images/" + basename)
#							obj = Clicks(e['clicks_id'], e['content'], e['type'], e['classname'], e['start'])
#						elif type[i] == "keypresses":
#							obj = Keypresses(e['keypresses_id'], e['content'], e['className'], e['start'])
#						elif type[i] == "timed":
#							obj = Timed(e["timed_id"], e['type'], e['classname'], e['content'], e['start'])
#						elif type[i] == "traffic":
#							obj = Traffic(e['traffic_all_id'], e['content'], e['className'], e['title'], e['start'])
#						elif type[i] == "trafficThroughput":
#							obj = TrafficThroughput(e['traffic_xy_id'], e['className'], e['start'], e['y'])
#						elif type[i] == "suricata":
#							obj = Suricata(e['suricata_id'], e['suricata_rule_id'], e['content'], e['className'], e['start'])
#
#						if type[i] not in type:
#							self.events[type[i]] = [obj]
#						else:
#							self.events[type[i]].append(obj)
#		except Exception:
#			print("Failed to import " + type[i])
