# Student parking permit, to buy or not? --- Parking Decision Making at iSchool using Monte Carlo Simulation

## Team Members:
Chaohan Shang, Xinyu Tian, Yute Li, Shukai Yao

## Scenario & Purpose
The purpose of this project is to help iSchool students to decide whether purchase parking permit or not by using Monte Carlo Simulation.

As a student drives his/her car to the iSchool building for courses/events, s/he has the following options for parking.
With a parking permit ($660 per year), the student can park the car at the reserved spots.
Without a parking permit, s/he prefers parking on the street if there are meters available ($1 per hour).
Otherwise, student may possibly take risks of violating the parking rules and park at the private parking, especially in a rush.
In this way, the student is likely to receive a ticket ($50 per time) for the violation if the UI parking department checks the cars around iSchool.
Meanwhile, the holder of the parking spot may ask the tow company to tow the student’s car.
This could results in a huge amount ($200 on average) for the student to pay compares to the parking ticket.
The student might be lucky (without any loss) if the parking department does not patrol in this area and nobody tows his/her car.
Finally, we compare the average parking cost without parking permits over students to the price of annual parking permits to provide the advice for making decisions.

Here are some basic facts in the scenario.
* We only consider the working hours of weekdays, 8am - 5pm from Monday to Friday, when the parking rules are enforced.
**The working hours are divided into 3 time blocks**: morning (8am - 11am), noon (11am - 2pm), afternoon (2pm - 5pm). So there are 15 time blocks in a week;
* There are up to 60 meters around the iSchool (along Daniel Street, Fifth Street, and Sixth Street), and about 20 private parking spots.
Among those private ones, there are usually 5 spots unoccupied;
* The annual parking permit for students is $660;
* The violation ticket for private parking is $50 per time, and a tow costs $200 on average.

## Assumptions and Hypotheses
To simplify the scenario, we make the following assumptions:
* As long as a student comes to the iSchool building in any time during a time slot, s/he will park the car for the entire 3 hours;
* The weekly schedule of a student is fixed through the year (32 weeks);
* The UI parking department changes their schedule to enforce parking regulations every week;
* The time of ticketing and towing is not considered in the simulation;
* If the car is being towed, there will be no parking tickets issued;
* Ticket would not be waived if getting caught more than once in one time slot.
In other words, it is possible to receive at most 3 parking tickets in one time slot.

## Simulation's variables of uncertainty
There are 6 variables of uncertainty.

* The times a student needs parking at iSchool per week, which obeys a normal distribution.
We divide students into two groups, heavy workload students whose normal distribution centering at 5 and light workload students whose normal distribution centering at 2;

* The probability that a student comes to iSchool is proportional to the total number of students registered in the onsite courses in the given time slot;

![time_slot_distribution](https://github.com/ChaohanShang/Final_Project/blob/master/prob.png "Probability that a student comes to iSchool")

* The probability of private parking violation, which obeys binomial distribution with p = 0.33.
If the student's vehicle has been towed once, the his/her probability of violating private parking reduced to 0.1.
If all meters near iSchool are occupied and you don’t want to miss the class, you may violate the rules and park in the reserved parking space. You may also find farther but safer meters;

* The probability of meter parking violation, which obeys binomial distribution with p = 0.1.
Meters violation may occurs either purposely or accidentally (unexpected meters expiration).

* The probability of being towed, which obeys binomial distribution with p = 0.1.
If the owner of reserved parking spot calls the towing company, the violated car will be towed. And you need to pay a fee to get your car back;

* The zones checked by the UI parking department every hour. They pick up 3 zones out of 30 randomly, in other words, it follows a uniform distribution.

## Analytical Summary of your findings:

Here, we compare the annual price of student parking permit with the total costs of meters parking and possible parking violation.
The overall average cost is $921.3 for heavy workload students, and $371.3 for light workload students.

![result](https://github.com/ChaohanShang/Final_Project/blob/master/simulation.png "Visualization of the simulation")

As shown in the plot above, the expected total parking cost fluctuates at different depth and simulations, but the expectation becomes more stable when depth goes up.
Judging from the plot, we would argue that it is wise for heavy workload students, just like those who come to the iSchool building almost everyday to purchase a parking permit.
However, as for light workload ones, using meters seems to be more reasonable.

The result could be more realistic by using better distributions and choosing more accurate parameters.

## Instructions on how to use the program:

Please specify the number of simulations you want to do and the maximum iteration times by keyboard input.
The program will return the expected parking cost (final average cost) without purchasing a parking permit for heavy workload students and light workload students.
Moreover, there is a plot illustrating the results obtained at different depths.

You may also change the facts and assumptions by altering the values of parameters.

## All Sources Used:
* [Parking Rates at UI Parking Department](http://www.parking.illinois.edu/parking_items/rates)
* [Parking Meter Violation Fine Structure](http://parking.illinois.edu/parking-news/New-parking-meter-fine-structure)
* [numpy.random](https://docs.scipy.org/doc/numpy-1.14.0/reference/routines.random.html)
* [matplotlib.pyplot](https://matplotlib.org/api/_as_gen/matplotlib.pyplot.html)
