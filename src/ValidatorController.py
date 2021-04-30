import os
import pdb
import time
import datetime
import threading
import Pyro4

from subprocess import Popen, PIPE

class ValidatorController:
	def __init__(self, script_path):
		self.script_path = script_path

	def run_validation(self, timeout):
		self.p1 = Popen(["python3", "-m", "pdb", self.script_path], stdin=PIPE, close_fds=True)
		self.p2 = Popen(["python3", "-m", "src.Validator", str(timeout)], stdin=PIPE, close_fds=True, cwd=os.getcwd())

	# INSTR must have \n at the end, otherwise command will hang
	def send_input(self, p, instr):
		p.stdin.write(instr.encode())

if __name__ == '__main__':
	v = ValidatorController('../test-antoine/sampleNoDependencies.py')
	
	try:
		v.run_validation()
	except Exception as e:
		print(e)	

	

