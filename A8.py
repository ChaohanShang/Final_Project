import math
import numpy as np
from itertools import combinations,permutations

# Assume the location code for ischool is 1.
def parking_timeslot():
    # Time slot that need to park, x is the number of courses.
    x = np.random.random_integers(1,6)
    possibleresult = list(combinations(range(15),x))
    select = np.random.random_integers(0,len(possibleresult)-1)
    return possibleresult[select]

def select_checkzone():
    # Divide the map into 20 parts, each time search 3 out of 20.
    # Uniformly pick 3 zones for checking.
    possibleresult = list(combinations(range(20),3))
    select = np.random.random_integers(0,len(possibleresult)-1)
    return possibleresult[select]

def parking_check_schedule():
    # the parking enforcement check every hour from Monday through Saturday
    # Consider 8:00am to 19:00 pm. 11 * 5 = 55 hours in total.
    check_schedule = []
    for i in range(0,5):
        for j in range(0,11):
            check_schedule.append(select_checkzone())
    return check_schedule

def meter():
    return np.random.random_integers(0,1)

def tow():
    return np.random.random_integers(0,1)

timeslot = parking_timeslot()
courseinfo = []
for i in range(len(timeslot)):
    t = (math.floor(timeslot[i]/3), timeslot[i]%3)
    courseinfo.append(t)
print(courseinfo)

# meter = True
# tow = True
ttltkt = 0
ttltow = 0
for i in range(100):
    cost = 0
    towtime = 0
    tickettime = 0
    for ii in range(32):
        check_schedule = []
        for i in range(0,5):
            for j in range(0,9):
                check_schedule.append(select_checkzone())
        check_schedule = np.array(check_schedule).reshape(5,3,9)
        print(check_schedule)
        print("-----------------")
        for i in range(len(courseinfo)):
                x = courseinfo[i][0]
                y = courseinfo[i][1]
                print(check_schedule[x][y])
                if meter() == 0:
                    if tow() ==1:
                        towtime += 1
                    else:
                        if 1 in set(check_schedule[x][y]):
                            tickettime +=1
                else:
                    cost += 3
    ttltkt += tickettime
    ttltow += towtime
print("tkt",ttltkt/100)
print("tow",ttltow/100)

