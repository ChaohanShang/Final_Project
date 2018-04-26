Create a FORK of this repository to store your code, data, and documentation for the final project. Detailed instructions for this assignment are in the course Moodle site.  The reason I'm asking you to fork this empty repository instead of creating a stand-alone repository is that it will be much easier for me and all students in the course to find all of our projects for code review and for grading. You can even get code review from students in the other section of IS590PR this way.

Even though your fork of this repository shall be public, you'll still need to explicitly add any students on your team as Collaborators in the Settings. That way you can grant them write privileges.

DELETE these lines from TEMPLATE up.

TEMPLATE for your report:

# Title: Student parking permit, to buy or not?
--- Parking decision making at iSchool using Monte Carlo Simulation

## Team Member(s):
Chaohan Shang, Xinyu Tian, Yute Li, Shukai Yao

# Monte Carlo Simulation Scenario & Purpose:
our project is trying to design a system by using Monte Carlo Simulation for students to decide whether they should purchase parking permit or not. 

Our system has three outcomes basically. When a student pays the meter, he or she may receive a ticket if the payment period is expired. In addition, if a student parks in the parking lot with permit restrictions, the police may ask the tow company to tow the student’s car. This could a large amount for students to pay compares to the parking ticket. However, the student could be lucky without the penalty if the police is not patrol in this area. The result of the probability whether the student may receive a ticket or be towed is calculated with the database which are the course schedule and the number of students at the particular time period. This simulation can help student to decide whether they should purchase a parking permit or keep paying the meters. So they can know which option is more affordable.


## Simulation's variables of uncertainty
We have 4 variables of uncertainty. 

The first one is the number of onsite courses weekly for each student, the range of values is 1 to 6 and it obeys normal distribution. More courses means longer parking time.

The second one is the probability of parking violation, it obeys binomial distribution. If all meters near iSchool are parked and you don’t want to miss the class, the only choice you have is to park in the reserved parking space.

The third one is the probability of being checked by parking dept per hour. We divide the university into 30 zones and the parking dept checks 3 zones per hour. So that for each zone, the probability of being checked per hour is one tenth. If the zone of iSchool is checked, the violated car will receive a ticket.

The last one is the probability of being towed, it obeys binomial distribution. If the owner of reserved parking space call the towing company, the violated car will be towed. And you need to pay a fee to get your car back.

## Hypothesis or hypotheses before running the simulation:
There are two parking methods:
  1. Parking with permit($675).
  2. Standard parking. Pay $1/hour on street if there are parking spot available and violate parking if there are no parking        spots. 

The time of ticketing and towing is not considered in the simulation.

Cars will be towed if the reserved parking spots are occupied by onwers. If the car is being towed, there will be no tickets issued.

Ticket would not be waived if getting caught more than once in one time slot. In other words, it is possible to receive at most 3 parking tickets in one time slot.
  

## Analytical Summary of your findings: (e.g. Did you adjust the scenario based on previous simulation outcomes?  What are the management decisions one could make from your simulation's output, etc.)

Here, we compare the annual price of student parking permit with the total costs of meters parking and possible parking violation. Given the assumptions that the meters will be full if many students attend the classes at the same time, and the students will take the risk to park at the private parking in some cases if there's no meters available, we realized that purchasing the parking permit ($675) may be more economical when comparing with the expected total costs without a permit ($1222 = meters $372 + tickets $250 + tows $600).

(TODO: Visualization)
As we did experiments over different iteration times, we obtained the result shown as above. 

We changed the parameters in the distributions to make the results more realistic.

## Instructions on how to use the program:
(TODO: user interaction?)

## All Sources Used:
* [itertools.combinations](https://docs.python.org/3/library/itertools.html?highlight=combinations#itertools.combinations)
* [numpy.random](https://docs.scipy.org/doc/numpy-1.14.0/reference/routines.random.html)
