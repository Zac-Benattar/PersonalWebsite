from startevaluationdata import StartEvaluationData
from currentevaluationdata import CurrentEvaluationData
from projectevaluator import ProjectEvaluator

import modeltrainer

import datetime

#Test an initial train of model
#Initial train is verbose and will reveal model score
def test_train_model():
    print("==== Start Test: Train Model ====")
    modeltrainer.train_all_models() #Prints out result of training
    print("==== Test Finished ====")

#Test loading a model
def test_load_model():
    #Make sure there is only one instance of this in the code
    #Stores a project to be evalauted
    print("==== Start Test: Load ProjectEvaluator ====")
    print("Try Load Model")
    EVALUATOR = ProjectEvaluator()  #Load project evaluator
    print("==== Test Finished ====")

#Test getting a prediction for initial project success prediction data
def test_get_initial_prediction():
    print("==== Start Test: Get Initial Prediction ====")

    EVALUATOR = ProjectEvaluator() #Load project evaluator

    #Load in dummy data to predict chance of success (parameters listed below)
    DEADLINE_DATE = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days = 100) #Load a date
    #initial_budget, num_developers, num_other_team_members, original_deadline, daily_running_cost, num_tasks
    start_evaluation_data = StartEvaluationData(0, 0, 0, DEADLINE_DATE, 0, 1000)

    result = EVALUATOR.get_initial_chance_of_success(start_evaluation_data)

    print("Result For: " + str(start_evaluation_data))
    print("Result: " + str(result))

    print("==== Test Finished ====")

#Test getting a prediction for current project success prediction data
def test_get_current_prediction():
    print("==== Start Test: Get Current Prediction ====")

    EVALUATOR = ProjectEvaluator()  #Load project evaluator

    #Load in dummy data to predict chance of success (parameters listed below)
    DEADLINE_DATE = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days = 100) #Load a date
    current_evaluation_data = CurrentEvaluationData(100000, 100000, 0, 20, 2, 0, DEADLINE_DATE, DEADLINE_DATE, 100, 100, 0, 0, 0)

    result = EVALUATOR.get_current_chance_of_success(current_evaluation_data)

    print("Result For: " + str(current_evaluation_data))
    print("Result: " + str(result))
    print("==== Test Finished ====")

#Test retraining the project evaluator
def test_retrain_all():
    print("==== Start Test: Retrain Model ====")

    EVALUATOR = ProjectEvaluator()  #Load project evaluator


    print("Get Initial Training!")

    #Load in dummy data to predict chance of success (parameters listed below)
    DEADLINE_DATE = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days = 100) #Load a date
    #initial_budget, num_developers, num_other_team_members, original_deadline, daily_running_cost, num_tasks
    start_evaluation_data = StartEvaluationData(0, 0, 0, DEADLINE_DATE, 0, 1000)

    result = EVALUATOR.get_initial_chance_of_success(start_evaluation_data)

    print("Result For: " + str(start_evaluation_data))
    print("Result: " + str(result))

    #Load in dummy data to predict chance of success (parameters listed below)
    DEADLINE_DATE = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days = 100) #Load a date
    current_evaluation_data = CurrentEvaluationData(100000, 100000, 0, 20, 2, 0, DEADLINE_DATE, DEADLINE_DATE, 100, 100, 0, 0, 0)

    result = EVALUATOR.get_current_chance_of_success(current_evaluation_data)

    print("Result For: " + str(current_evaluation_data))
    print("Result: " + str(result))

    all_past_current_evaluation_data = [current_evaluation_data] #Store a list of all past data

    print("Retrain Model!")
    EVALUATOR.update_model(start_evaluation_data, all_past_current_evaluation_data, -1) #-1 for project failier 1 for project success

    print("Get New Predictions!")

    result = EVALUATOR.get_initial_chance_of_success(start_evaluation_data)

    print("Result For: " + str(start_evaluation_data))
    print("Result: " + str(result))

    result = EVALUATOR.get_current_chance_of_success(current_evaluation_data)

    print("Result For: " + str(current_evaluation_data))
    print("Result: " + str(result))

    print("==== Test Finished ====")


def test_all():
    #============================
    # All used tests are executed here
    #============================
    test_train_model()
    print("")
    test_load_model()
    print("")
    test_get_initial_prediction()
    print("")
    test_get_current_prediction()
    print("")
    test_retrain_all()

#Run all tests
test_all()
