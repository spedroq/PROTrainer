from prowatch.PROWatch import *
from dateutil import parser
import datetime
import sys


class PROWatchReplay:
    logging_levels = {
        "-1": "all",
        "0": "radon",
        "2": "bot input",
        "92": "mouse clicks",
        "93": "mouse movements",
        "94": "mouse scrolls",
        "91": "keyboard input up",
        "90": "keyboard input down"
    }

    def __init__(self):
        #
        #   Startup and create all the variables we'll need
        self.active_prowatch_logs_folder = ""
        self.active_logging_levels_for_replay = []
        self.active_replay_frequency_milliseconds = 50
        self.working_directory = "PROWatchReplays"
        

    def mainline(self):
        print("PROWatchReplay\nLog Replayer for PROWatch logs.")
        print("\n")
        #
        #   Get the input of a PROWatch log dir from the user
        print("Enter PROWatch log directory:")
        self.active_prowatch_logs_folder = input()
        print("\n")
        #
        #   Get the input for any filters
        print("Filter Selection")
        print(self.logging_levels)
        
        while True:
            print("Using Filters you can select which elements you would like to show.\n\
                You can stack multiple logging types together as this message will repeat.\nEnter 'quit' to exit this screen.\n\n\
                Enter a logging level ID:")
            filter_selection = input()
            if filter_selection.lower() == "quit":
                False
                #
                #   End on quit
                break
            for key,value in self.logging_levels.items():
                if str(filter_selection) == str(key) or str(filter_selection) == (value):
                    if filter_selection not in self.active_logging_levels_for_replay:
                        #
                        #   Save this selection from the user using the data dictionary for logging
                        #   types, be sure to add only unique logging levels
                        self.active_logging_levels_for_replay.append({key: value})
                        break
        
        #self.active_logging_levels_for_replay.append(self.logging_levels[0])
        #
        #   .
        #   Ok, now we have all the info, let's replay that log
        print(self.active_logging_levels_for_replay)
        logs = self.replay_logs_from_folder_using_logging_levels()
        log_text = ""
        for log in logs:
            log_text += log[2] + "\n"
        log_text = log_text[:-1]
        print("\nComplete")
        print("\nSave? (yes/no)")
        if input().lower() == "yes":
            print("\nFilename:")
            filename = input()
            if filename[-4:] != ".csv":
                print("Invalid filename. Writing 'output.csv' instead of '{}'".format(filename))
                filename = "output.csv"
            if not os.path.exists(self.active_prowatch_logs_folder + os.sep + self.working_directory):
                os.makedirs(self.active_prowatch_logs_folder + os.sep + self.working_directory)
            with open(self.active_prowatch_logs_folder + os.sep + self.working_directory + os.sep + filename, "w") as f:
                f.write(log_text)
        print("\nAll done")

    #
    #   A function to replay a log using an input of log files
    def replay_logs_from_folder_using_logging_levels(self, is_playback=False):
        #
        #   Get all the files from in there
        all_moves_at_times = []
        for file in self.get_all_prowatch_logs_from_folder():

            print("HANDLING FILE {}".format(file))
            #
            #   Ok, so now we need to analyse the log and replay it
            moves_at_times = self.get_moves_at_times_using_logging_levels_from_logging_file(file)
            #for move_at_time in moves_at_times:
            #    print(move_at_time[2])
            if len(moves_at_times) == 0:
                print("FILTERING REMOVES ALL RESULTS")
                sys.exit(0)
            #
            #   Print the analysis
            self.print_analysis_of_move_set(moves_at_times)
            #
            #   Ok, now replay this filter log
            if is_playback:
                self.replay_moves_at_times_from_just_now_onwards(moves_at_times)
            for m in moves_at_times:
                all_moves_at_times.append(m)
        return all_moves_at_times




    def get_moves_at_times_using_logging_levels_from_logging_file(self, log_file):
        moves_at_times = []
        time_offset = 0
        time_now = datetime.datetime.now()
        adjusted_now = 0

        is_valid = False

        log_file_text = ""
        with open(log_file, "r") as lf:
            log_file_text = lf.read()

  
        for line in log_file_text.split("\n")[1:]:
            #
            #   Is this a valid line?
            is_valid = False
            for active_logging_level in self.active_logging_levels_for_replay:
                try:
                    if active_logging_level["-1"]:
                        #print("ALL LOGGING ENABLED")
                        is_valid = True
                        break
                except:
                    pass
            
                
            for logging_level in self.active_logging_levels_for_replay:
                try:
                    for key,value in logging_level.items():
                        #print(",{}, | {}".format(key, line))
                        #print(line)
                        if ",{},".format(key) in line:
                            is_valid = True       
                            #print(line)
                except:
                    pass

           

            if is_valid:
                line_elements = line.split(",")
                                
                try:
                    log_time = parser.parse(line_elements[0])
                    bot_input = line_elements[4]
                except:
                    print("Analysis of a line failed - bot input column set to unknown")
                    bot_input = "unknown"
                moves_at_times.append(
                    (log_time, bot_input, line)
                )
                if time_offset == 0:
                    time_offset = time_now - log_time
                    adjusted_now = time_now - time_offset
        return moves_at_times

    #
    #   A function to return all the prowatch files from a folder
    def get_all_prowatch_logs_from_folder(self):
        log_file_paths = []
        files = os.listdir(self.active_prowatch_logs_folder)
        for file in files:
            if os.path.isfile(self.active_prowatch_logs_folder + os.sep + file):
                log_file = os.path.join(
                    self.active_prowatch_logs_folder, file
                )
                log_file_paths.append(log_file)
        return log_file_paths

    #
    #   A function to replay moves at times
    #   This locks the thread
    def replay_moves_at_times_from_just_now_onwards(self, moves_at_times):
        #just_now = time.time()
        try:
            adjusted_now = moves_at_times[0][0]
        except:
            adjusted_now = datetime.datetime.now()
        print("\n\nKEY PRESSES REPLAY IN REALTIME: ")
        print(adjusted_now)
        #   Replay
        i = 0
        while True:
            time.sleep(self.active_replay_frequency_milliseconds / 1000)
            adjusted_now += datetime.timedelta(milliseconds=self.active_replay_frequency_milliseconds)
            #
            #   Compare and see if we should print
            for move_at_time in moves_at_times: 
                if adjusted_now > move_at_time[0]:
                    """
                    print(
                        move_at_time[0].strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
                        move_at_time[1]
                    )
                    """
                    print(move_at_time[2])
                    last_printed = move_at_time
                    moves_at_times.remove(move_at_time)

            if len(moves_at_times) < 1:
                print("NO MORE ENTRIES MATCH THE CURRENT LOGGING FILTERS")
                break

    #
    #   A function to work out the adjusted time for a log, this is the time in the future that it will
    #   be played, but here for this element it is the time we are going to play it
    def get_adjusted_time_for_move_at_time(self, move_at_time):
        time_now = datetime.datetime.now()
        time_offset = time_now - move_at_time[0]
        return time_now - time_offset


    #
    #   A function to run an analysis on a move set
    def print_analysis_of_move_set(self, moves_at_times):
        total_presses = len(moves_at_times)
        total_time_length = moves_at_times[len(moves_at_times) - 1][0] - moves_at_times[0][0]
        seconds = total_time_length.seconds
        average_apm = round((total_presses / seconds) * 60, 1)
        average_aps = round((total_presses / seconds), 1)
        print("APM: {}".format(average_apm))
        print("APS: {}".format(average_aps))
        print("TOTAL INPUTS: {}".format(total_presses))
        print("TOTAL TIME: {}".format(total_time_length))

        if average_apm > 60:
            print("CAUTION, THESE INPUTS ARE TOO FAST")


            


"""
log_file = r"C:\____Development\PROTrainer\prowatch\logs\20180327-010801-ddtmxvns\ktuyrgss.csv"

print("\nEnter PROWatch log directory")
log_file = input()
#
#   Get that file
files = os.listdir(log_file)
for file in files:
    if len(file) > 2:
        log_file += os.sep + file
print(log_file)

#
#   Break it into lines
log_file_text = ""
with open(log_file, "r") as fi:
    log_file_text = fi.read()

moves_at_times = []
time_offset = 0
time_now = datetime.datetime.now()
adjusted_now = 0

is_valid = False

for line in log_file_text.split("\n"):
    if ",2," in line:
        is_valid = True
        line_elements = line.split(",")
        log_time = parser.parse(line_elements[0])
        bot_input = line_elements[4]
        moves_at_times.append(
            (log_time, bot_input)
        )

        if time_offset == 0:
            time_offset = time_now - log_time
            adjusted_now = time_now - time_offset
            #print(time_offset)
        #print((log_time, bot_input))
#print(moves_at_times)

if is_valid:

    #
    #   In a loop until we reach the end of inputs
    last_printed = ""
    total_presses = len(moves_at_times)
    total_time_length = moves_at_times[len(moves_at_times) - 1][0] - moves_at_times[0][0]
    days, seconds = total_time_length.days, total_time_length.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    average_apm = round((total_presses / seconds) * 60, 1)
    average_aps = round((total_presses / seconds), 1)
    #
    #   Metrics
    print("APM: {}".format(average_apm))
    print("APS: {}".format(average_aps))
    print("TOTAL INPUTS: {}".format(total_presses))
    print("TOTAL TIME: {}".format(total_time_length))


    if average_apm > 60:
        print("CAUTION, THESE INPUTS ARE TOO FAST")

    print("\n\nKEY PRESSES REPLAY IN REALTIME: ")
    #   Replay
    while True:
        milliseconds_to_sleep = 100
        time.sleep(milliseconds_to_sleep / 1000)
        adjusted_now += datetime.timedelta(milliseconds=100)
        #
        #   Compare and see if we should print
        for move_at_time in moves_at_times: 
            if adjusted_now > move_at_time[0]:
                print(
                    move_at_time[0].strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
                    move_at_time[1]
                )
                last_printed = move_at_time
                moves_at_times.remove(move_at_time)

        if len(moves_at_times) < 1:
            break

    #print(total_presses, total_time_length, average_apm)

    
else:
    print("THIS LOG FILE HAS NO ENTRIES TO ANALYSE")

input()

"""

#pwr = PROWatchReplay()
#pwr.mainline()