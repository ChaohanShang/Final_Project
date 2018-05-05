import math
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

def read_iSchool_schedule(filepath ='weekly_schedule.csv'):
    """
    Read the weekly schedule with the number of courses and students into a DataFrame.
    :param filepath: string, the path of a csv file containing columns: "index", "courses", and "students"
    :return: a pandas DataFrame
    """
    return pd.read_csv(filepath, encoding='utf8').set_index('index')

def get_student_weekly_distribution(schedule):
    """
    Given the number of students on each time slot,
    generate the probability that a student comes to iSchool on a particular time slot.
    Assume the more students registered in the onsite courses during a time span,
    the more likely a student comes to the iSchool building to attend the course.
    :param schedule: the DataFrame imported by read_iSchool_schedule()
    :return: a 1D numpy array whose length is 15
    """
    student_num_array = schedule['students'].values.reshape((1, len(schedule['students'])))
    prob_array = (student_num_array / np.sum(student_num_array))[0]
    plt.plot(range(15), prob_array, color = 'darkorange')
    plt.fill_between(range(15), prob_array, [0] * 15, color = 'darkorange')
    plt.xticks(range(0, 15, 1))
    plt.ylim((0, 0.2))
    plt.xlabel('Time Blocks: 0 = Mon. morning, 1 = Mon. noon, 2 = Mon. afternoon, ...')
    plt.ylabel('The Likelihood a Student Comes to the iSchool Building')
    plt.savefig('prob.png')
    return prob_array

def get_student_parking_blocks(prob_array, mu: int = 3, sigma: int = 1):
    """
    Divide the working hours (8am-5pm) of a day into 3 blocks: morning (8am-11am), noon (11am-2pm), afternoon (2pm-5pm).
    The function selects several time blocks that a student comes to the iSchool building and need parking in a week
    associated with the distribution of student numbers over time blocks.
    Assume the number of time blocks obeys a normal distribution N(3,1).
    :return: A tuple of integers ranging from 0 to 14, indicating the time blocks a student needs parking
    """
    num_blocks = int(np.random.normal(loc = mu, scale = sigma))
    if num_blocks <= 1: num_blocks = 1    # adjustment for extreme cases since negative values are invalid
    # randomly pick up a case from all combinations, assume that the possibility is proportional to the distribution of student numbers
    return np.random.choice(15, num_blocks, replace = False, p = prob_array)

def get_parking_dept_enforcement_schedule(num_zones: int, checked_per_hour: int):
    """
    Simulate the plan of the university parking enforcement department by week.
    We assume that there are 30 zones in the campus, and they randomly check 3 zones every working hour.
    Consider 8am - 5pm on Mon - Fri, 9 * 5 = 45 hours in total.
    :param num_zones: int, total number of zones in the campus.
    :param checked_per_hour: int, average number of zones that the parking department enforce parking rules each hour.
    :return: a list of the zone numbers for every working hour, just like [(0, 15, 2), (3, 9, 18), ...]
    """
    # assume that the zones selected obey the uniform distribution
    return [np.random.choice(num_zones, checked_per_hour, replace = False) for working_hour in range(45)]

def violate_parking_rules(schedule, idx: int, meters_capacity: int = 60, prob_violate = 0.33):
    """
    Given the weekly schedule of courses, meters capacity and the probability of violating parking rules,
    decide whether a student will violate parking rules or not.
    :param schedule: the DataFrame imported by read_iSchool_schedule()
    :param idx: int, ranging from 0 to 14, indicates the time slot
    :param meters_capacity: the number of meters available around the iSchool
    :param prob_violate: float, the probability a student will violate the parking rules if no meters are available
    :return: 0 - False, 1 - True
    """
    if schedule.loc[idx, 'students'] >= meters_capacity:    # when surrounding meters are all occupied
        return np.random.binomial(1, prob_violate)
    else:
        return 0

def being_towed(schedule, idx, private_capacity = 5, prob_tow = 0.1):
    """
    Given the weekly schedule of courses, private parking capacity and the probability of being towed,
    decide whether a car will be towed or not.
    :param schedule: the DataFrame imported by read_iSchool_schedule()
    :param idx: int, ranging from 0 to 14, indicates the time slot
    :param private_capacity: the number of private parkings at iSchool
    :param prob_tow: float, the probability the professors, staffs will call the towing service if no private parking is available
    :return: 0 - False, 1 - True
    """
    if schedule.loc[idx, 'courses'] >= private_capacity:    # when private parking plots at iSchool are all occupied
        return np.random.binomial(1, prob_tow)
    else:
        return 0

def violate_meters(prob = 0.1):
    """
    Assume the probability of violating the parking meters, either intentionally or accidentally, is 0.1 on average
    :param prob: float, the probability a student violate the meters
    :return: 0 - False, 1 - True
    """
    return np.random.binomial(1, prob)

def idx_2_day_and_time_block(idx):
    """

    :param idx:
    :return:
    """
    day, time_block = (math.floor(idx / 3), idx % 3)  # convert the index to days and blocks (3 -> (1,0) - Tuesday morning)
    return day, time_block

def simulate_violate(schedule, idx, check_schedule_by_slot, std_id, weekly_result, prob_violate_array):
    """

    :param schedule:
    :param idx:
    :param check_schedule_by_slot:
    :param std_id:
    :param weekly_result:
    :param prob_violate_array:
    :return:
    """
    (weekly_ticket, weekly_tow, weekly_cost) = weekly_result
    day, time_block = idx_2_day_and_time_block(idx)
    if being_towed(schedule, idx, 5, prob_tow=0.1) == 1:  # the car is towed
        weekly_tow += 1
        weekly_cost += 200
        prob_violate_array[std_id] = 0.1
    else:
        if 1 in set(check_schedule_by_slot[day][time_block]):  # the iSchool area is checked by the parking dept
            # assume that the zone code for iSchool is 1
            weekly_ticket += 1
            weekly_cost += 50
    weekly_result = (weekly_ticket, weekly_tow, weekly_cost)
    return weekly_result, prob_violate_array

def simulate_meter(idx, check_schedule_by_slot, std_id, students_street_tickets, weekly_result):
    (weekly_ticket, weekly_tow, weekly_cost) = weekly_result
    day, time_block = idx_2_day_and_time_block(idx)
    if violate_meters(prob=0.1) == 1:
        if 1 in set(check_schedule_by_slot[day][time_block]):
            students_street_tickets[std_id] += 1
            if students_street_tickets[std_id] >= 3:
                weekly_ticket += 1
                weekly_cost += 40
            elif students_street_tickets[std_id] >= 2:
                weekly_ticket += 1
                weekly_cost += 25
            else:
                weekly_ticket += 1
    else:
        weekly_cost += 3
    weekly_result = (weekly_ticket, weekly_tow, weekly_cost)
    return weekly_result

def simulate_process(max_iter, num_student, schedule, prob_array, mu, sigma):
    average_cost_by_iter = {}  # for each line in visualization
    print('=== Simulation {:<} (Parking at iSchool {} times per week) ==='.format(sim + 1, mu))
    for num_iter in range(1, max_iter + 1):  # try different depths
        depth = num_iter * num_student
        total_result = np.zeros(3)
        for iter in range(num_iter):  # each iteration in a given depth
            # assume student's schedule is fixed through the year
            std_course_info = [list(get_student_parking_blocks(prob_array, mu, sigma)) for std_id in range(num_student)]
            prob_violate_array = np.full(num_student, 0.33)
            students_street_tickets = np.zeros(num_student)
            for week in range(32):  # 32 working weeks per year
                weekly_result = np.zeros(3)
                check_schedule_by_hour = get_parking_dept_enforcement_schedule(30, 3)  # randomly pick 3 out of 30
                check_schedule_by_slot = np.array(check_schedule_by_hour).reshape(5, 3, 9)  # build the enforcement schedule of the parking department
                std_id = 0
                for each_std_courses in std_course_info:
                    for idx in each_std_courses:
                        if violate_parking_rules(schedule, idx, 60, prob_violate_array[std_id]) == 1:  # the student violates parking rules
                            weekly_result, prob_violate_array = simulate_violate(schedule, idx, check_schedule_by_slot, std_id, weekly_result, prob_violate_array)
                        else:
                            weekly_result = simulate_meter(idx, check_schedule_by_slot, std_id, students_street_tickets, weekly_result)
                    std_id += 1
                total_result += weekly_result
        average_cost = total_result[2] / depth
        if details_flag == True:
            print('--- Depth {:<} ---'.format(depth))
            print('Ticket {:>12.1f}'.format(total_result[0] / (depth)))
            print('Tow {:>15.1f}'.format(total_result[1] / (depth)))
            print("Average Cost {:>6.1f}".format(average_cost))
        average_cost_by_iter[depth] = average_cost
    print("(Parking at iSchool {} times per week) Average Cost {:>6.1f} at Simulation {}".format(mu, np.mean(list(average_cost_by_iter.values())), sim + 1))
    return average_cost_by_iter

if __name__ == "__main__":
    schedule = read_iSchool_schedule('weekly_schedule.csv')
    prob_array = get_student_weekly_distribution(schedule)
    num_student = 200
    annual_parking_permit = 660     # FY18 Student Rates - 12 Month Permit
    # allow users to skip the detailed results for every iteration
    details_flag = True
    while True:
        details_flag_str = input('Would you like to view the results for every iteration? (Y/N)\n')
        if len(details_flag_str) == 0:
            continue
        if details_flag_str[0] in ['N', 'n', 'F', 'f']:
            details_flag = False
            break
        elif details_flag_str[0] in ['Y', 'y', 'T', 't']:
            break
        else:
            print(('Please enter Yes (Y) or No (N).'))
            continue
    # allow users to determine the depth
    while True:
        try:
            num_sim = int(input('Please enter the simulation times:\n'))
            max_iter = int(input('Please enter the maximum number of iterations for each simulation:\n'))
        except ValueError:
            print(('Please enter a valid number.'))
            continue
        else:
            break
    max_depth = max_iter * num_student
    print('Maximum depth for each simulation: ' + str(max_depth) + ', or the mean is calculated against ' + str(max_depth)+ ' cases.')
    heavy_final_total_cost = light_final_total_cost = 0
    for sim in range(num_sim):
        heavy_average_cost_by_iter = simulate_process(max_iter, num_student, schedule, prob_array, mu = 5, sigma = 1)
        light_average_cost_by_iter = simulate_process(max_iter, num_student, schedule, prob_array, mu = 2, sigma = 1)
        plt.plot(list(heavy_average_cost_by_iter.keys()), list(heavy_average_cost_by_iter.values()))
        plt.plot(list(light_average_cost_by_iter.keys()), list(light_average_cost_by_iter.values()))
        heavy_final_total_cost += np.sum(list(heavy_average_cost_by_iter.values()))
        light_final_total_cost += np.sum(list(light_average_cost_by_iter.values()))
        print("Final Average Cost for Heavy Workload Students: " + str(round(heavy_final_total_cost / (num_sim * max_iter), 1)))
        print("Final Average Cost for Light Workload Students: " + str(round(light_final_total_cost / (num_sim * max_iter), 1)))
    # visualize the results by a bunch of lines
    plt.ylim((200, 1100))
    plt.xticks(range(0, max_depth + 1, 5 * num_student))
    plt.axhline(y=annual_parking_permit, linestyle='dashdot', color='red')
    plt.xlabel('Depth (Number of Students * Iteration Times)')
    plt.ylabel('Annual Parking Cost (USD)')
    fig_name = 'simulation.png'
    plt.savefig(fig_name)
