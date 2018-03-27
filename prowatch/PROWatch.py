#
#	P R O  W A T C H 
#	Pro Watch - Logger for PROTrainer
#
import threading
import os
import string
import random
import datetime
import time

#
#	PROWatch
#	Everything is in CSV pretty much
#	
class PROWatch(threading.Thread):
	def __init__(self):
		if "prowatch" not in os.getcwd():
			self.logging_dir_prefix = "prowatch" + os.sep + "logs"
		else:
			self.logging_dir_prefix = "logs"
		if not os.path.exists(self.logging_dir_prefix):
			os.mkdir(self.logging_dir_prefix)
		self.logging_dir = ""
		self.logging_file = ""
		self.logging_file_extension = ".csv"
		self.log_header_row = "date_time,log_id,code,status_message,key_press,key_press_type"
		self.run_id = self.random_string(8)

	def get_tidy_name_for_new_folder(self):
		folder_name = ""
		now = datetime.datetime.now()
		folder_name = "{}{}{}".format(
			now.strftime("%Y%m%d-%H%M%S"),
			"-", self.run_id
		)
		return folder_name

	def random_string(self, length):
		chars = ''.join(random.choice(string.ascii_lowercase) for _ in range(length))
		return chars

	def get_log_file_path(self):
		return "{}{}{}{}{}{}".format(
			self.logging_dir_prefix,
			os.sep,
			self.logging_dir,
			os.sep,
			self.logging_file,
			self.logging_file_extension
		)

	def get_tidy_date_for_logging(self):
		tidy_datetime = ""
		now = time.time()
		localtime = time.asctime(time.localtime(time.time()))
		now = datetime.datetime.now()
		tidy_datetime = "{}{}{}".format(
			now.strftime("%Y-%m-%d %H:%M:%S.%f"),
			",", self.random_string(4), 
			","
		)
		return tidy_datetime
	def get_logging_dir(self):
		return self.logging_dir_prefix + os.sep + self.logging_dir

	def start_logging(self):
		#
		#	Reset
		self.logging_dir = self.get_tidy_name_for_new_folder()
		os.mkdir(self.get_logging_dir())
		self.logging_file = self.random_string(8)
		self.log_write_header_row()

	def random_int(self, maximium_int):
		return random.randrange(0, int(maximium_int) + 1)

	def clear_log(self):
		with open(self.get_log_file_path(), "w") as log_file:
			log_file.write("")

	def log_write_header_row(self):
		self.clear_log()
		self.append_write_to_log(-1, self.log_header_row)

	def append_write_to_log(self, code, status="", key_press="", key_press_type=""):
		#
		#	List input, prepare the line
		if code == -1:
			log_data_string = ""
		else:
			log_data_string = self.get_tidy_date_for_logging() + ","
			log_data_string += str(code) + ","
		
		log_data_string += str(status)
		if log_data_string[-1:] != ",":
			log_data_string += ","

		if code != -1:
			log_data_string += str(key_press) + ","
			log_data_string += str(key_press_type) + ","
		log_data_string = log_data_string[:-1] + "\n"
		with open(self.get_log_file_path(), "a") as log_file:
			log_file.write(log_data_string)



def test():
	pw = PROWatch()
	#
	#	Start logging
	pw.start_logging()
	for i in range(0, 42):
		random_i = pw.random_int(42)
		pw.append_write_to_log(pw.random_int(random_i), "A random test function", "left mouse", "click")
		time.sleep(random_i / 100)

#test()

