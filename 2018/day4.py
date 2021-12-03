import re
from datetime import datetime

f = open('input_day4.txt','r')
lines = f.readlines()
f.close()

# date_time_obj = datetime. strptime(date_time_str, '%d/%m/%y %H:%M:%S')
#[1518-06-13 00:02] falls asleep
#[1518-03-18 23:57] Guard #857 begins shift
#[1518-05-05 00:22] wakes up

timestamps = []

def func():
    for line in lines:
        result = re.search('\[(\d*)-(\d*)-(\d*) (\d*):(\d*)\] (.*)',line.rstrip())
        year=int(result.groups()[0])
        month=int(result.groups()[1])
        day=int(result.groups()[2])
        hour=int(result.groups()[3])
        minutes=int(result.groups()[4])
        index = minutes + hour * 60 + day * 24*60 + month * 24*60*12
        action = result.groups()[5]
        value = 0
        if (action == "falls asleep"):
            value = -1
        elif (action == "wakes up"):
            value = -2            
        else:
            value = int(re.search("Guard #(\d*) begins shift",action).groups()[0])
        timestamps.append((index,value))
    timestamps.sort(key=lambda x:x[0])
    print(timestamps)

func()
        