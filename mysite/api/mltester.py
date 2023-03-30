import sys #Import system file to add extra imports from outside file

import pathlib

path = pathlib.Path(__file__).parent.parent.joinpath('static/Risk_Assessment')

print(sys.path)

sys.path.append(path)

from startevaluationdata import StartEvaluationData
from currentevaluationdata import CurrentEvaluationData
from projectevaluator import ProjectEvaluator
import datetime


print("Start")

#Make sure there is only one instance of this in the code
evaluator = ProjectEvaluator()

#initial_budget, num_developers, num_other_team_members, original_deadline, daily_running_cost, num_tasks
DEADLINE_DATE = datetime.datetime.now() + datetime.timedelta(days = 100) #What date format should I use?

#Load in dummy data to predict chance of success (parameters listed below)
#initial_budget, num_developers, num_other_team_members, original_deadline, daily_running_cost, num_tasks
start_evaluation_data = StartEvaluationData(100000, 20, 2, DEADLINE_DATE, 100, 100)

#Get chance of success
chance_of_success = evaluator.get_initial_chance_of_success(start_evaluation_data)
print("Chance_Of_Success: " + str(chance_of_success))


print("RETRAIN MODEL")
#Get all past data to train on
#initial_budget, num_developers, num_other_team_members, original_deadline, daily_running_cost, num_tasks
start_evaluation_data = StartEvaluationData(100000, 20, 2, DEADLINE_DATE, 100, 100)
#initial_budget, current_budget, money_spent, num_developers, num_other_team_members, num_team_left, original_deadline, current_deadline, daily_running_cost, num_tasks, completed_tasks, average_happiness, average_confidence
all_past_current_evaluation_data = [CurrentEvaluationData(100000, 100000, 0, 20, 2, 0, DEADLINE_DATE, DEADLINE_DATE, 100, 100, 0, 1, 1)]

#Retrain the model with new data
evaluator.update_model(start_evaluation_data, all_past_current_evaluation_data, 1) #-1 for project failier 1 for project success


#Get new chance of success (Just to see change)
chance_of_success = evaluator.get_initial_chance_of_success(start_evaluation_data)
print("Chance_Of_Success: " + str(chance_of_success))
