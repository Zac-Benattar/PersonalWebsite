#Class used to store all the relevant project data at the start of development
#It includes less data than current evaluation data which inherits from this
#This is because the project isn't in progress yet and some values would be useless
#This object can return a matrix containing data for the model to predict a riskiness

from datetime import datetime #Import to get the current date and time
from datetime import timezone

class StartEvaluationData:
    def __init__(self, initial_budget, num_developers, num_other_team_members, original_deadline, daily_running_cost, num_tasks):
        self.initial_budget = initial_budget
        self.money_spent = 0
        self.num_developers = num_developers
        self.num_other_team_members = num_other_team_members

        CURRENT_DAY = datetime.now(timezone.utc)

        TIME_DELTA = original_deadline - CURRENT_DAY

        self.days_until_original_deadline = TIME_DELTA.days

        #Find an approximate guess at how long the money in the company will last based on
        #Cost estimates
        if daily_running_cost > 0:
            self.days_budget_covers_running_costs = (self.initial_budget - self.money_spent) / daily_running_cost
        else:
            self.days_budget_covers_running_costs = 0
        self.num_tasks = num_tasks
        self.num_completed_tasks = 0

    def get_data_as_matrix(self):
        matrix = [[
        self.initial_budget,
        self.money_spent,
        self.num_developers,
        self.num_other_team_members,
        self.days_until_original_deadline,
        self.days_budget_covers_running_costs,
        self.num_tasks,
        self.num_completed_tasks
        ]]

        return matrix #Return 1xn matrix

    #Used for implementing this in higher order functions
    @staticmethod
    def get_external_data_as_matrix(project):
        #matrix = [[
        #project.initial_budget,
        #project.money_spent,
        #project.num_developers,
        #project.num_other_team_members,
        #project.days_until_original_deadline,
        #project.days_budget_covers_running_costs,
        #project.num_tasks,
        #project.num_completed_tasks
        #]]

        #return matrix #Return 1xn matrix
        return project.get_data_as_matrix()

    #
    def get_initial_budget(self):
        return self.initial_budget

    def get_num_developers(self):
        return self.num_developers

    def get_num_other_team_members(self):
        return self.num_other_team_members

    def get_total_team_members(self):
        return self.get_num_developers() + self.get_num_other_team_members()

    def get_days_until_original_deadline(self):
        return self.days_until_original_deadline

    def get_days_budget_covers_running_costs(self):
        return self.days_budget_covers_running_costs

    def get_num_tasks(self):
        return self.num_tasks

    def get_num_completed_tasks(self):
        return self.num_completed_tasks

    def get_num_uncompleted_tasks(self):
        return self.get_num_tasks() - self.get_num_completed_tasks()

    #Used to determine what object is stored as current evaluation data and start evaluation can be stored in the same place
    #Useful for figuring out if a risk assesment snapshot was an initial estimate or an "project in progress" estimate
    def is_start_evaluation_data(self):
        return True

    #Used to determine what object is stored as current evaluation data and start evaluation can be stored in the same place
    #Useful for figuring out if a risk assesment snapshot was an initial estimate or an "project in progress" estimate
    def is_current_evaluation_data(self):
        return False

    #To String Function
    def __str__(self):
        return "[initial_budget: " + str(self.initial_budget) +\
        ", money_spent: " + str(self.money_spent) +\
        ", num_developers: " + str(self.num_developers) +\
        ", num_other_team_members: " + str(self.num_other_team_members) +\
        ", days_until_original_deadline: " + str(self.days_until_original_deadline) +\
        ", days_budget_covers_running_costs: " + str(self.days_budget_covers_running_costs) +\
        ", num_tasks: " + str(self.num_tasks) +\
        ", num_completed_tasks: " + str(self.num_completed_tasks) + "]"
