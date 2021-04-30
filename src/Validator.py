import os
import time
import datetime
import threading
import json
import Pyro4
import sys
import shutil

from .Event import Event, Auditd, Clicks, Keypresses, Traffic, TrafficThroughput, Timed, Suricata

class Validator:
	def __init__(self, timeout):
		self.eceld = Pyro4.Proxy("PYRONAME:ecel.service")
		self.start_time = None
		self.output_path = os.getcwd() + "/validation_temp/"
		self.timeout = timeout
		self.events = []

		if not os.access(os.getcwd(), os.W_OK):
			os.chmod(os.getcwd(), stat.S_IWUSR)

		self.eceld.start_collectors()
		self.validation_loop()

	def validation_loop(self):
		while True:
			if not os.path.exists(self.output_path):
				os.mkdir(self.output_path)
			else:
				shutil.rmtree(self.output_path)
				os.mkdir(self.output_path)				

			if self.start_time == None:
				self.start_time = datetime.datetime.now()
			else:
				if datetime.datetime.now() - self.start_time >= datetime.timedelta(seconds=self.timeout):
					raise RuntimeError("Script validation timed out ({0} seconds)".format(self.timeout))

			self.eceld.stop_collectors()
			self.eceld.parse_data_all()
			self.eceld.export_data(self.output_path)
			self.import_files()

			for item in self.events:
				print(item)
			
	# could make this more efficient to continue where we left of, meaning we need to track
	# where we leave off
	def import_files(self):
		print("importing files")
		directories = ["/parsed/auditd/auditdData.JSON", "/parsed/pykeylogger/click.JSON", "/parsed/pykeylogger/keypressData.JSON", "/parsed/pykeylogger/timed.JSON", "/parsed/tshark/networkDataAll.JSON", "/parsed/tshark/networkDataXY.JSON", "/parsed/suricata/suricata.JSON"]
		type = ["auditid", "clicks", "keypresses", "timed", "traffic", "trafficThroughput", "suricata"]
		self.events = []
		
		try:
			for i in range(len(directories)):
				with open(self.output_path + directories[i]) as f:
					data = json.load(f)
					
					for d in data:
				            e = d
				            if type[i] == "auditd":
				                obj = Auditd(e['auditd_id'], e['content'], "auditd", e['start'])
				            elif type[i] == "clicks":
				                basename = os.path.basename(e['content'])
				                e['content'] = os.path.join(self.output_path, "raw/pykeylogger/click_images/" + basename)
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
			print("Failed to import " + type[i])

if __name__ == '__main__':
	try:
		v = Validator(int(sys.argv[1]))
	except RuntimeError as e:
		print(e)

	

