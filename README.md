Create a FORK of this repository to store your code, data, and documentation for the final project. Detailed instructions for this assignment are in the course Moodle site.  The reason I'm asking you to fork this empty repository instead of creating a stand-alone repository is that it will be much easier for me and all students in the course to find all of our projects for code review and for grading. You can even get code review from students in the other section of IS590PR this way.

Even though your fork of this repository shall be public, you'll still need to explicitly add any students on your team as Collaborators in the Settings. That way you can grant them write privileges.

DELETE these lines from TEMPLATE up.

TEMPLATE for your report:

# Title: Student parking permit, to buy or not?
--- Parking decision making at iSchool using Monte Carlo Simulation

## Team Member(s):
Chaohan Shang, Xinyu Tian, Yute Li, Shukai Yao

# Monte Carlo Simulation Scenario & Purpose:
(be sure to read the instructions given in course Moodle)

## Simulation's variables of uncertainty
We have 4 variables of uncertainty. 

The first one is the number of onsite courses weekly for each student, the range of values is 1 to 6 and it obeys normal distribution. More courses means longer parking time.

The second one is the probability of parking violation, it obeys binomial distribution. If all meters near iSchool are parked and you don’t want to miss the class, the only choice you have is to park in the reserved parking space.

The third one is the probability of being checked by parking dept per hour. We divide the university into 30 zones and the parking dept checks 3 zones per hour. So that for each zone, the probability of being checked per hour is one tenth. If the zone of iSchool is checked, the violated car will receive a ticket.

The last one is the probability of being towed, it obeys binomial distribution. If the owner of reserved parking space call the towing company, the violated car will be towed. And you need to pay a fee to get your car back.

## Hypothesis or hypotheses before running the simulation:

## Analytical Summary of your findings: (e.g. Did you adjust the scenario based on previous simulation outcomes?  What are the management decisions one could make from your simulation's output, etc.)

## Instructions on how to use the program:

## All Sources Used:

