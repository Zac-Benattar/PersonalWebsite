
from startevaluationdata import StartEvaluationData
#Class used to store all the relevant project data during development
#This object can return a matrix containing data for the model to predict a riskiness


from datetime import datetime #Import to get the current date and time
from datetime import timezone

class CurrentEvaluationData(StartEvaluationData): #CurrentEvaluationData inherits from StartEvaluationData
    #Overrides StartEvaluationData init
    def __init__(self, initial_budget, current_budget, money_spent, num_developers, num_other_team_members, num_team_left, original_deadline, current_deadline, daily_running_cost, num_tasks, completed_tasks, average_happiness, average_confidence):
        self.initial_budget = initial_budget
        self.current_budget = current_budget

        self.money_spent = money_spent

        self.num_developers = num_developers
        self.num_other_team_members = num_other_team_members

        self.num_team_left = num_team_left

        CURRENT_DAY = datetime.now(timezone.utc)

        TIME_DELTA_ORIGINAL = original_deadline - CURRENT_DAY
        TIME_DELTA_CURRENT = current_deadline - CURRENT_DAY

        self.days_until_original_deadline = TIME_DELTA_ORIGINAL.days
        self.days_until_current_deadline = TIME_DELTA_CURRENT.days

        #Find an approximate guess at how long the money in the company will last based on
        #Cost estimates
        self.days_budget_covers_running_costs = (self.current_budget - self.money_spent) / daily_running_cost

        self.num_tasks = num_tasks
        self.num_completed_tasks = completed_tasks

        self.current_average_happiness = average_happiness
        self.current_average_confidence = average_confidence

    #Overrides method from StartEvaluationData
    def get_data_as_matrix(self):
        matrix = [[
        self.initial_budget,
        self.current_budget,
        self.money_spent,
        self.num_developers,
        self.num_other_team_members,
        self.num_team_left,
        self.days_until_original_deadline,
        self.days_until_current_deadline,
        self.days_budget_covers_running_costs,
        self.num_tasks,
        self.num_completed_tasks,
        self.current_average_happiness,
        self.current_average_confidence
        ]]

        return matrix #Return 1xn matrix

    #Overrides method from StartEvaluationData
    #Used for implementing this in higher order functions
    @staticmethod
    def get_external_data_as_matrix(project):
        #matrix = [[
        #project.initial_budget,
        #project.current_budget,
        #project.money_spent,
        #project.num_developers,
        #project.num_other_team_members,
        #project.num_team_left,
        #project.days_until_original_deadline,
        #project.days_until_current_deadline,
        #project.days_budget_covers_running_costs,
        #project.num_tasks,
        #project.num_completed_tasks,
        #project.current_average_happiness,
        #project.current_average_confidence
        #]]

        #return matrix #Return 1xn matrix
        return project.get_data_as_matrix() #

    #Used to determine what object is stored as current evaluation data and start evaluation can be stored in the same place
    #Useful for figuring out if a risk assesment snapshot was an initial estimate or an "project in progress" estimate
    def is_start_evaluation_data(self):
        return False

    #Used to determine what object is stored as current evaluation data and start evaluation can be stored in the same place
    #Useful for figuring out if a risk assesment snapshot was an initial estimate or an "project in progress" estimate
    def is_current_evaluation_data(self):
        return True

    #Inherits methods from StartEvaluationData

    def get_current_budget(self):
        return self.current_budget

    def get_days_until_current_deadline(self):
        return self.days_until_current_deadline

    def get_average_happiness(self):
        return self.current_average_happiness

    def get_average_confidence(self):
        return self.current_average_confidence

    #To String Function
    def __str__(self):
        return "[initial_budget: " + str(self.initial_budget) +\
        ", current_budget: " + str(self.current_budget) +\
        ", money_spent: " + str(self.money_spent) +\
        ", num_developers: " + str(self.num_developers) +\
        ", num_other_team_members: " + str(self.num_other_team_members) +\
        ", num_team_left: " + str(self.num_team_left) +\
        ", days_until_original_deadline: " + str(self.days_until_original_deadline) +\
        ", days_until_current_deadline: " + str(self.days_until_current_deadline) +\
        ", days_budget_covers_running_costs: " + str(self.days_budget_covers_running_costs) +\
        ", num_tasks: " + str(self.num_tasks) +\
        ", num_completed_tasks: " + str(self.num_completed_tasks) +\
        ", current_average_happiness: " + str(self.current_average_happiness) +\
        ", current_average_confidence: " + str(self.current_average_confidence)  + "]"
