#Import SK learn libary for machine learning
from sklearn import datasets
from sklearn import linear_model
from sklearn.model_selection import train_test_split

import pickle #Used to serialise the model to be loaded later saves retraining everytime the program is rerun

import modeltrainer


#Used to turn the models prediction into a score of sorts viewed as a percentage to the user
def combine_scores(classes, probability):
    NO_OF_CLASSES = len(classes)
    #Treat this precition as some random variable and compute expectation
    #to come up with a score
    sum = 0
    for i in range(NO_OF_CLASSES):
        #Converts the class into a percentage (changing -1 to 1 into 0% to 100%)
        #This is used because -1 represents failiure and 1 represents sucess.
        #1 means 100% sucessful and -1 means 0% sucessful
        percentage_score_of_class = convert_to_percentage(classes[i])

        #Use formula for expectaion over discrete outcomes to decide final "sucess score"
        #Probabilities are normalised so sum of probability will be
        #approximately 1 (give or take for floating point innaccuracy)
        sum += percentage_score_of_class * probability[i]

        #print(str(percentage_score_of_class) + " * " + str(probability[i]))

    return sum

#Takes in a value between -1 and 1 and converts to a percentage between 0-100
def convert_to_percentage(value):
    return (value + 1) * 50

#Used to store a loaded linear model and update/save it
class ProjectEvaluator:


    def __init__(self):

        #Get filenames for model files
        self.START_MODEL_FILE_PATH = modeltrainer.START_MODEL_FILE_PATH
        self.IN_PROGRESS_MODEL_FILE_PATH = modeltrainer.IN_PROGRESS_MODEL_FILE_PATH
        #Load logistic regression models
        self.start_model = pickle.load(open(self.START_MODEL_FILE_PATH, 'rb'))
        self.in_progress_model = pickle.load(open(self.IN_PROGRESS_MODEL_FILE_PATH, 'rb'))

    #This will take in a projects riskiness and return a number between 0 and 1 which can be used as a percentage
    def get_initial_chance_of_success(self, startevaluationdata):
        input_data = startevaluationdata.get_data_as_matrix()

        prediction = self.start_model.predict_proba(input_data)

        return combine_scores(self.start_model.classes_, prediction[0]) #Return the prediction

    #This will take in a projects riskiness and return a number between 0 and 1 which can be used as a percentage
    def get_current_chance_of_success(self, currentevaluationdata):
        input_data = currentevaluationdata.get_data_as_matrix()

        prediction = self.in_progress_model.predict_proba(input_data)

        return combine_scores(self.in_progress_model.classes_, prediction[0]) #Return the prediction

    def update_model(self, new_startevaluationdata, new_currentevaluationdata, result_out):

        #=====================================================================
        #SIMPLE APPROACH USING fit()
        #[On the whole dataset again]
        #This uses the simple trainer in modeltrainer.py
        #=====================================================================
        #Add new data to dataset
        modeltrainer.add_to_dataset(new_startevaluationdata, new_currentevaluationdata, result_out)
        #Retrain models
        modeltrainer.retrain_all_models() #Calling retrain to use all data and not be verbose
        #Reload models
        self.start_model = pickle.load(open(self.START_MODEL_FILE_PATH, 'rb'))
        self.in_progress_model = pickle.load(open(self.IN_PROGRESS_MODEL_FILE_PATH, 'rb'))

        #=====================================================================
        #ALTERNATIVE APPROACH USING partial_fit() [For models that support it]
        #Not used as couldn't make results reliable/accuracte
        #=====================================================================

        #Needs to "retrain" the model using parital_fit()
        #Make sure warm start is enabled as to not delete all old training data (called from original train)
        #Then need to serialize the data and save it again (similar to modeltrainer.py)

        #CURRENTEVALATION_DATA_SIZE = len(new_currentevaluationdata)

        #Change start data into a matrix
        #new_start_data_in = new_startevaluationdata.get_data_as_matrix()
        #Loop through all current evaluation data to get the data as a matrix
        #new_in_progress_data_in = [new_currentevaluationdata[i].get_data_as_matrix() for i in range (CURRENTEVALATION_DATA_SIZE)]

        #Get data result/class (the data storing if the project succeeded)
        #new_start_data_out = [result_out]
        #new_in_progress_data_out = [result_out for i in range(CURRENTEVALATION_DATA_SIZE)]

        #Refit the model
        #self.start_model.partial_fit(new_start_data_in, new_start_data_out) #Start predictor
        #if CURRENTEVALATION_DATA_SIZE > 0: #If there was any in progress data
        #    self.in_progress_model.partial_fit(new_in_progress_data_in, new_in_progress_data_out) #In progress project predictor

        #Save start model
        #print("Saving start model to: " + self.START_MODEL_FILENAME)
        #Save model in serialised form
        #pickle.dump(self.start_model, open(self.START_MODEL_FILENAME, 'wb'))
        #print("Saved!")

        #Save in progress model
        #print("Saving in progress model to: " + self.IN_PROGRESS_MODEL_FILENAME)
        #Save model in serialised form
        #pickle.dump(self.in_progress_model, open(self.IN_PROGRESS_MODEL_FILENAME, 'wb'))
        #print("Saved!")
