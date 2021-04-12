import os
import pdb
import time
import datetime
import threading
import json
import Pyro4

from subprocess import Popen, PIPE
from queue import Queue, Empty
from Event import Event, Auditd, Clicks, Keypresses, Traffic, TrafficThroughput, Timed, Suricata

class ValidatorController:
	def __init__(self, script_path, eceld_path, timeout=None):
		self.script_path = script_path
		self.eceld_path = eceld_path
		self.output_path = os.getcwd() + "/validation_temp/"
		
		# Process to run script and daemon to validate
		self.p = None
		self.kill_event = threading.Event()
		self.wait_event = threading.Event()

		# This will be the event that the validator will be looking for
		self.current_event = ""
		self.events = []

		# This will be the timeout functionality for validating
		self.start_time = None
		self.timeout = timeout

		if not os.path.exists(self.output_path):
			os.mkdir(self.output_path)

	def run_validation(self):
		self.kill_event.clear()
		self.kill_event.clear()

		t1 = threading.Thread(target=self.check_files, args=(), daemon=True)
		t1.start()	
#		self.p = Popen(["python3", "-m", "pdb", self.script_path], stdin=PIPE, close_fds=True)



	# INSTR must have \n at the end, otherwise command will hang
	def send_input(self, instr):
		self.p.stdin.write(instr.encode())

	def check_files(self):
		# loop
		try:
			eceld = Pyro4.Proxy("PYRONAME:ecel.service")
			eceld.start_collectors()
			print("O_O")
			
			while True:
				if self.wait_event.is_set():
					continue

				# if a start time has been set, determine a timeout event
				if self.start_time == None:
					self.start_time = datetime.datetime.now()
				else:
					if datetime.datetime.now() - self.start_time >= self.timeout:
						raise RuntimeError

				print("O_O")
				eceld.parse_data_all()
				print("O_O1")
				eceld.export_data(self.output_path)
				print("O_O2")
				self.import_files()
				print("O_O3")

		except Exception as e:
			raise Exception("thread error")			
	
	# could make this more efficient to continue where we left of, meaning we need to track
	# where we leave off
	def import_files(self):
		print("importing files")
		directories = ["/parsed/auditd/auditdData.JSON", "/parsed/pykeylogger/click.JSON", "/parsed/pykeylogger/keypressData.JSON", "/parsed/pykeylogger/timed.JSON", "/parsed/tshark/networkDataAll.JSON", "/parsed/tshark/networkDataXY.JSON", "/parsed/suricata/suricata.JSON"]
		type = ["auditid", "clicks", "keypresses", "timed", "traffic", "trafficThroughput", "suricata"]
		self.events = []
		
		try:
			for i in range(len(directories)):
				with open(self.eceld_path + directories[i]) as f:
					data = json.load(f)
					
					for d in data:
				            e = d
				            if type[i] == "auditd":
				                obj = Auditd(e['auditd_id'], e['content'], "auditd", e['start'])
				            elif type[i] == "clicks":
				                basename = os.path.basename(e['content'])
				                e['content'] = os.path.join(self.eceld_path, "raw/pykeylogger/click_images/" + basename)
				                obj = Clicks(e['clicks_id'], e['content'], e['type'], e['classname'], e['start'])
				            elif type[i] == "keypresses":
				                obj = Keypresses(e['keypresses_id'], e['content'], e['className'], e['start'])
				            elif type[i] == "timed":
				                obj = Timed(e["timed_id"], e['type'], e['classname'], e['content'], e['start'])
				            elif type[i] == "traffic":
				                obj = Traffic(e['traffic_all_id'], e['content'], e['className'], e['title'], e['start'])
				            elif type[i] == "trafficThroughput":
				                obj = TrafficThroughput(e['traffic_xy_id'], e['className'], e['start'], e['y'])
				            elif type[i] == "suricata":
				                obj = Suricata(e['suricata_id'], e['suricata_rule_id'], e['content'], e['className'], e['start'])
				            if type[i] not in self._event:
				                self._events[type[i]] = [obj]
				            else:
				                self._events[type[i]].append(obj)
		except Exception:
			print("Failed to import " + type)

if __name__ == '__main__':
	v = Validator('./t.py', '/home/kali/eceld-netsys/ProjectData/antoinetest', timeout=5)
	
	try:
		v.run_validation()
#		v.send_input('s\n')
#		v.send_input('s\n')
#		v.send_input('s\n')
#		v.send_input('s\n')
#		v.send_input('s\n')
#		v.send_input('s\n')
	except Exception as e:
		print(e)
		print("error in main")		

	

