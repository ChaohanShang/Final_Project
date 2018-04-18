import math
import numpy as np
from itertools import combinations,permutations

# Assume the location code for ischool is 1.
def parking_timeslot():
    # Time slot that need to park, x is the number of courses.
    x = np.random.random_integers(1,6)
    return list(combinations(range(15),x))[np.random.random_integers(1,len(list(combinations(range(15),x))))]

def select_checkzone():
    # Divide the map into 20 parts, each time search 3 out of 20.
    # Uniformly pick 3 zones for checking.
    checklist = list(combinations(range(20),3))[np.random.random_integers(1,len(list(combinations(range(20),3))))]
    return checklist

def parking_check_schedule():
    # the parking enforcement check every hour from Monday through Saturday
    # Consider 8:00am to 19:00 pm. 11 * 5 = 55 hours in total.
    check_schedule = []
    for i in range(0,5):
        for j in range(0,11):
            check_schedule.append(select_checkzone())
    return check_schedule

timeslot = parking_timeslot()
courseinfo = []
for i in range(len(timeslot)):
    t = (math.floor(timeslot[i]/3), timeslot[i]%3)
    courseinfo.append(t)
print(courseinfo)

caughttime = 0
for i in range(16):
    print("-----------------")
    check_schedule = []
    for i in range(0,5):
        for j in range(0,9):
            check_schedule.append(select_checkzone())
    check_schedule = np.array(check_schedule).reshape(5,3,9)
    # print(check_schedule)
    # print("-----------------")
    for i in range(len(courseinfo)):
        x = courseinfo[i][0]
        y = courseinfo[i][1]
        print(check_schedule[x][y])
        if 1 in check_schedule[x][y]:
            print("dang")
            caughttime +=1
        else:
            print("safe")

print(caughttime)
