import math
import numpy as np
import pandas as pd
from itertools import combinations
from matplotlib import pyplot as plt
import warnings
warnings.filterwarnings("ignore")

debug = False

def parking_timeslot():
    # Assume the times of students come to the iSchool building to attend courses obey a normal distribution N (3,1)
    x = int(np.random.normal(loc = 3, scale = 1))
    possibleresult = list(combinations(range(15),x))
    select = np.random.random_integers(0,len(possibleresult)-1)
    return possibleresult[select]

def select_checkzone():
    # Divide the map into 30 parts, each time search 3 out of 30.
    # Uniformly pick 3 zones for checking.
    possibleresult = list(combinations(range(30),3))
    select = np.random.random_integers(0,len(possibleresult)-1)
    return possibleresult[select]

def parking_check_schedule():
    # the parking enforcement check every hour from Monday through Saturday
    # Consider 8:00am to 5:00 pm. 11 * 5 = 55 hours in total.
    check_schedule = []
    for day in range(0,5):
        for hour in range(0,9):
            check_schedule.append(select_checkzone())
    return check_schedule

def read_volume_data():
    vol = pd.read_csv('volume.csv', encoding='utf8').set_index('index')
    return vol

def violate_parking_rules(idx):
    if vol.loc[idx, 'students'] >= 60:
        return np.random.binomial(1, 0.33)
    else:
        return 0

def tow(idx):
    if vol.loc[idx, 'courses'] >= 5:
        return np.random.binomial(1, 0.1)
    else:
        return 0

if __name__ == "__main__":
    num_student = 200

    total_cost_by_iter = {}

    for num_iter in range(2, 50, 1):
        students_course_info = {}
        for std_id in range(num_student):
            course_info = []
            timeslot = parking_timeslot()
            for ts in range(len(timeslot)):
                course_info.append((math.floor(timeslot[ts] / 3), timeslot[ts] % 3))
            if debug:
                print(course_info)
            students_course_info[std_id] = course_info

        vol = read_volume_data()

        total_ticket = 0
        total_tow = 0
        total_cost = 0
        for iter in range(num_iter):
            annual_ticket = 0
            annual_tow = 0
            annual_cost = 0
            for week in range(32):
                weekly_ticket = 0
                weekly_tow = 0
                weekly_cost = 0
                check_schedule = parking_check_schedule()
                check_schedule = np.array(check_schedule).reshape(5, 3, 9)
                if debug:
                    print(check_schedule)
                    print("-----------------")
                for std_id in range(num_student):
                    for course in range(len(students_course_info[std_id])):
                        day = students_course_info[std_id][course][0]
                        time_slot = students_course_info[std_id][course][1]
                        idx = 3*day + time_slot
                        if violate_parking_rules(idx) == 1:
                            if tow(idx) == 1:
                                weekly_tow += 1
                                weekly_cost += 200
                            else:
                                if 1 in set(check_schedule[day][time_slot]):
                                    weekly_ticket += 1
                                    weekly_cost += 50
                        else:
                            weekly_cost += 3
                annual_ticket += weekly_ticket
                annual_tow += weekly_tow
                annual_cost += weekly_cost
            total_ticket += annual_ticket
            total_tow += annual_tow
            total_cost += annual_cost
        average_cost = total_cost / (num_iter*num_student)
        print("Ticket", total_ticket / (num_iter*num_student))
        print("Tow", total_tow / (num_iter*num_student))
        print(average_cost)
        total_cost_by_iter[num_iter*num_student] = average_cost
    plt.ylim((500, 1000))
    plt.axhline(y=675, linestyle='dashdot', color='red')
    plt.plot(total_cost_by_iter.keys(), total_cost_by_iter.values(), color='navy')
    plt.show()
