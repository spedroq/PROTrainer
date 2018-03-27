from PROWatch import *
from dateutil import parser
import datetime

prowatch = PROWatch()

log_file = r"C:\____Development\PROTrainer\prowatch\logs\20180327-010801-ddtmxvns\ktuyrgss.csv"

#
#	Break it into lines
log_file_text = ""
with open(log_file, "r") as fi:
	log_file_text = fi.read()

moves_at_times = []
time_offset = 0
time_now = datetime.datetime.now()
adjusted_now = 0

for line in log_file_text.split("\n"):
	if ",2," in line:
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



#
#	In a loop until we reach the end of inputs
last_printed = ""
total_presses = len(moves_at_times)
total_time_length = moves_at_times[len(moves_at_times) - 1][0] - moves_at_times[0][0]
days, seconds = total_time_length.days, total_time_length.seconds
hours = days * 24 + seconds // 3600
minutes = (seconds % 3600) // 60
seconds = seconds % 60
average_apm = round((total_presses / seconds) * 60, 1)
average_aps = round((total_presses / seconds), 1)
while True:
	milliseconds_to_sleep = 100
	time.sleep(milliseconds_to_sleep / 1000)
	adjusted_now += datetime.timedelta(milliseconds=100)
	#
	#	Compare and see if we should print
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

print(total_presses, total_time_length, average_apm)

print("APM: {}".format(average_apm))
print("APS: {}".format(average_aps))
print("TOTAL INPUTS: {}".format(total_presses))
print("TOTAL TIME: {}".format(total_time_length))


if average_apm > 60:
	print("CAUTION, THESE INPUTS ARE TOO FAST")