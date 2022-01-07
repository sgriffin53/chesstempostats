import csv
import time
import calendar
from datetime import datetime

def myFunc(stat):
    return stat.passed * 100 / stat.tried

class Stat:
    def __init__(self, name=''):
        self.tried = 0
        self.passed = 0
        self.name = name

def statExists(stat_name, stats):
    for stat in stats:
        if stat.name == stat_name: return True
    return False

def getStat(stat_name, stats):
    for i, stat in enumerate(stats):
        if stat.name == stat_name: return i
    return None

file = 'attempts.csv'
stats = []
time_threshold = 60 * 60 * 24
tried_threshold = 0.05
str_in = input("Enter time span in hours (blank for default of 24hr): ")
if str_in:
    time_threshold = 60 * 60 * float(str_in)
str_in = input("Enter threshold for attempts as a percentage: (leave blank default of 5% of total): ")
if str_in:
    str_in = str_in.replace('%', '')
    tried_threshold = int(str_in) / 100
total_done = 0
with open(file, newline='') as csvfile:
    readlines = csv.reader(csvfile, delimiter=',', quotechar='|')
    for i, row in enumerate(readlines):
        if i == 0: continue
        if i < 100000000:
            if len(row) == 0: continue
            date = row[0] + ":00"
            #utc_time = time.strptime(date)
            epoch = datetime.fromisoformat(date).timestamp()
            age = time.time() - epoch
            if age > time_threshold: continue
            total_done += 1
            #correct = row[10]
            correct = True
            if row[10] == '1': correct = True
            else: correct = False
            #print(correct)
            tactics = row[16:]
            for tactic in tactics:
                tactic = tactic.replace('\"','')
                tactic_name = tactic.split(":")[0]
                if tactic_name == "": continue
                if not statExists(tactic_name, stats):
                    new_stat = Stat(tactic_name)
                    stats.append(new_stat)
                    new_stat.tried += 1
                    if correct:
                        new_stat.passed += 1
                else:
                    new_stat = stats[getStat(tactic_name, stats)]
                    new_stat.tried += 1
                    if correct:
                        new_stat.passed += 1

sortedstats = list(stats)
sortedstats.sort(key=myFunc, reverse=True)

time_threshold_mins = int(time_threshold / 60)
time_threshold_hrs = int(time_threshold_mins / 60)
timestring = str(time_threshold_mins) + " minutes."
if time_threshold >= 60 * 60:
    timestring = str(time_threshold_hrs) + " hours."

print("")
print("Stats for last " + timestring)
print("Limiting to stats that make up at least " + str(tried_threshold * 100) + "% of total.")
print("")
for stat in sortedstats:
    if stat.tried < total_done * tried_threshold: continue
    percentage = stat.passed * 100 / stat.tried
    percentage = round(percentage, 2)
    buffer1 = " " * (40 - len(stat.name))
    triedstring = str(stat.passed) + "/" + str(stat.tried)
    buffer2 = " " * (5 - len(triedstring))
    print(stat.name + buffer1 + triedstring + buffer2 + " - " + str(percentage) + "%")
print("Total of " + str(total_done) + " tactics in last " + timestring)