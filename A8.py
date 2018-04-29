import math
import numpy as np
import pandas as pd
from itertools import combinations
from matplotlib import pyplot as plt

import warnings

import time
warnings.filterwarnings("ignore")

debug = False

def get_student_parking_slots(prob_array):
    """
    Divide the working hours (8am-5pm) of a day into 3 slots: morning (8am-11am), noon (11am-2pm), afternoon (2pm-5pm).
    The function selects several time slots that a student comes to the iSchool building and need parking in a week
    associated with the distribution of student numbers over time slots.
    Assume the number of time slots obeys a normal distribution N(3,1).
    :return: A tuple of integers ranging from 0 to 14, indicating the time slots a student needs parking
    """
    num_slots = int(np.random.normal(loc = 3, scale = 1))
    if num_slots <= 1: num_slots = 1    # adjustment for extreme cases since negative values are invalid
    return np.random.choice(15, num_slots, replace = False, p = prob_array)
    # all_possible_slots = list(combinations(range(15), num_slots))    # generate a list of all possible combinations
    # randomly_selected = np.random.randint(0, len(all_possible_slots))
    # randomly pick up a case, assume that the possibility of reaching different combinations are equal
    # return all_possible_slots[randomly_selected]    # return a particular time slots

def select_checkzone():
    # Divide the map into 30 parts, each time search 3 out of 30.
    # Uniformly pick 3 zones for checking.
    return np.random.choice(30, 3, replace = False)
    # possibleresult = list(combinations(range(30),3))
    # select = np.random.random_integers(0,len(possibleresult)-1)
    # return possibleresult[select]

def parking_check_schedule():
    # the parking enforcement check every hour from Monday through Saturday
    # Consider 8:00am to 5:00 pm. 11 * 5 = 55 hours in total.
    check_schedule = []
    for day in range(0,5):
        for hour in range(0,9):
            check_schedule.append(select_checkzone())
    return check_schedule

def read_volume_data(filename = 'volume.csv'):
    vol = pd.read_csv(filename, encoding='utf8').set_index('index')
    return vol

def generate_time_slot_distribution(vol):
    student_num_array = vol['students'].reshape((1, len(vol['students'])))
    prob_array = (student_num_array / np.sum(student_num_array))[0]
    return prob_array

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
    vol = read_volume_data()
    prob_array = generate_time_slot_distribution(vol)
    num_student = 500
    max_iter = 10
    num_lines = 1
    # num_lines = int(input('Simulation times: '))
    # num_student = int(input('Number of students: '))
    # max_iter = int(input('Maximum iteration times: '))
    total_cost_by_iter = {}

    for line in range(num_lines):
        for num_iter in range(1, max_iter + 1):
            students_course_info = {}
            for std_id in range(num_student):
                course_info = []
                timeslot = get_student_parking_slots(prob_array)
                for ts in range(len(timeslot)):
                    course_info.append((math.floor(timeslot[ts] / 3), timeslot[ts] % 3))
                if debug:
                    print(course_info)
                students_course_info[std_id] = course_info
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
            num_simulations = num_iter*num_student
            average_cost = total_cost / num_simulations
            print('Ticket{:>12.1f}'.format(total_ticket / (num_simulations)))
            print('Tow{:>15.1f}'.format(total_tow / (num_simulations)))
            print("Average Cost {:>4.1f}".format(average_cost))
            total_cost_by_iter[num_simulations] = average_cost
        print(total_cost_by_iter)
        plt.plot(total_cost_by_iter.keys(), total_cost_by_iter.values())
    plt.ylim((400, 800))
    plt.axhline(y=675, linestyle='dashdot', color='red')
    plt.xlabel('Number of simulations')
    plt.ylabel('USD')
    plt.savefig('plot.png')
