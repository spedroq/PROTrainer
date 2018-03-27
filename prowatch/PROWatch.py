
# P R O  W A T C H
# Pro Watch - Logger for PROTrainer
import threading
import os
import string
import random
import datetime
import time


# PROWatch
# Everything is in CSV pretty much
class PROWatch(threading.Thread):

    logging_dir_prefix = logging_dir = logging_file = logging_file_extension = log_header_row = run_id = ""

    def run(self):
        # Fix path for running instance of prowatch (log files)
        if "prowatch" not in os.getcwd():
            # Running from root folder
            self.logging_dir_prefix = "prowatch" + os.sep + "logs"
        else:
            # Running from this folder
            self.logging_dir_prefix = "logs"
        # If the loggin root path does not exist, create it
        if not os.path.exists(self.logging_dir_prefix):
            os.mkdir(self.logging_dir_prefix)
        # Init all attributes
        self.logging_dir = ""
        self.logging_file = ""
        self.logging_file_extension = ".csv"
        self.log_header_row = "date_time,log_id,code,status_message,key_press,key_press_type"
        self.run_id = self.random_string(8)
        self.start_logging()

    def get_tidy_name_for_new_folder(self):
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
        """
        Method to generate a unique date string containing a unique random value.
        :return: date string of right now and a unique random value.
        """
        now = datetime.datetime.now()
        tidy_datetime = "{}{}{}".format(
            now.strftime("%Y-%m-%d %H:%M:%S.%f"),
            ",", self.random_string(4),
            ","
        )
        return tidy_datetime

    def get_logging_dir(self):
        """
        Method to get the logging directory.
        """
        return self.logging_dir_prefix + os.sep + self.logging_dir

    def start_logging(self):
        """
        Method to make a folder and create the file for this logging session.
        """
        self.logging_dir = self.get_tidy_name_for_new_folder()
        os.mkdir(self.get_logging_dir())
        self.logging_file = self.random_string(8)
        self.log_write_header_row()

    @staticmethod
    def random_int(maximium_int):
        return random.randrange(0, int(maximium_int) + 1)

    def clear_log(self):
        with open(self.get_log_file_path(), "w") as log_file:
            log_file.write("")

    def log_write_header_row(self):
        """
        Method to write the header in the log file.
        NOTE: It clears the file.
        """
        # Clear the log to write the header as the header
        self.clear_log()
        # Write the header
        self.append_write_to_log(-1, self.log_header_row)

    def append_write_to_log(self, code: int, status: str="", key_press: str="", key_press_type: str=""):
        """
        Method to take inputs and append it to the log.
        :param code: status code as an int.
        :param status: status message as a str (with no commas).
        :param key_press: key press as a str.
        :param key_press_type: type of key press as a str.
        """
        # List input, prepare the line

        # If this is the header row, do not insert the date
        if code == -1:
            log_data_string = ""
        else:
            log_data_string = self.get_tidy_date_for_logging() + ","
            log_data_string += str(code) + ","

        # Write the status code
        log_data_string += str(status)
        # Fix for .csv just in case there is no ',' at the end
        if log_data_string[-1:] != ",":
            log_data_string += ","

        # If this is not the header row
        if code != -1:
            # Insert the rest of the values
            log_data_string += str(key_press) + ","
            log_data_string += str(key_press_type) + ","
        # Remove the final ',' if it exists and append a '\n'.
        log_data_string = log_data_string[:-1] + "\n"

        # Write line to the log
        with open(self.get_log_file_path(), "a") as log_file:
            log_file.write(log_data_string)


def test():
    pw = PROWatch()
    # Start logging
    pw.start_logging()
    for i in range(0, 42):
        random_i = pw.random_int(42)
        pw.append_write_to_log(pw.random_int(random_i), "A random test function", "left mouse", "click")
        time.sleep(random_i / 100)

#test()

