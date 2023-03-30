
#Import SK learn libary for machine learning
from sklearn import datasets
from sklearn import linear_model
from sklearn.model_selection import train_test_split
from startevaluationdata import StartEvaluationData
from currentevaluationdata import CurrentEvaluationData

import pickle #Used to serialise the model to be loaded later saves retraining everytime the program is rerun

from os import path

COMBINED_MODEL_NAME = "model"
FILE_EXTENSION = ".sav"

START_POSTFIX = "start" #The filename for the model to load
IN_PROGRESS_POSTFIX = "inprogress" #The filename for the model to load

#Get the path from this file to easily and robustly load files even if the program starts in a diferent file directory
BASEPATH = path.dirname(__file__)

#Filename of datasets
START_DATASET_FILENAME = "startevaluationdataset.txt" #Filename of start prediction dataset
IN_PROGRESS_DATASET_FILENAME = "inprogressevaluationdataset.txt" #Filename of in progress project prediction dataset

#Generate the filepath of the datasets assuming they are in the same file location as THIS current file
START_DATASET_FILE_PATH = path.abspath(path.join(BASEPATH, START_DATASET_FILENAME))
IN_PROGRESS_DATASET_FILE_PATH = path.abspath(path.join(BASEPATH, IN_PROGRESS_DATASET_FILENAME))

#Create the filename for the the saved (pickled) model
START_MODEL_FILENAME = COMBINED_MODEL_NAME + START_POSTFIX + FILE_EXTENSION
IN_PROGRESS_MODEL_FILENAME = COMBINED_MODEL_NAME + IN_PROGRESS_POSTFIX + FILE_EXTENSION

#Generate the filepath for this assuming it starts in the same place as THIS current file
START_MODEL_FILE_PATH = path.abspath(path.join(BASEPATH, START_MODEL_FILENAME))
IN_PROGRESS_MODEL_FILE_PATH = path.abspath(path.join(BASEPATH, IN_PROGRESS_MODEL_FILENAME))



#Used to determine how much of the data should normally be used to test the model
DEFAULT_TEST_TRAIN_SPLIT = 0.2

def train_model_and_save(data_set_filepath, model_file_path, verbose, test_train_split):
    if verbose == True:
        print("=== Start Training ===")
    if verbose == True:
        print("Loading Dataset from path: " + data_set_filepath)
    #Loads data from a file called dataset.txt
    #(this is actually a svmlight file)
    #this is a file used to represent a sparse matrix (sparse matrix being a matrix with many 0s)
    #this matrix represents the dataset we'll use to train
    #in_data is the inputs we'll take and output_data are like the results of the data.
    #Think in data as happiness etc. out data is probability of success
    in_data, out_data = datasets.load_svmlight_file(data_set_filepath)
    if verbose == True:
        print("Dataset Loaded!")
    #=====================================================================
    #SIMPLE APPROACH USING LogisticRegression()
    #Requires total retraining of model instead of incremental Training
    #Has proved more reliable and accurate however (worth the extra training time!)
    #=====================================================================
    #Logistic Regression Algorithm/Object to load
    logisitc_regression = linear_model.LogisticRegression(
    #warm_start = True,
    #class_weight = 'balanced',
    max_iter = 2000,
    solver = 'newton-cholesky', #Sometimes can produce more accurate/certain results
    C = 0.001 #Tune for size of data
    )

    #=====================================================================
    #ALTERNATIVE APPROACH USING Stocastic Gradient Descent + partial_fit()
    #Not used as proved innaccurate/unreliable for our data
    #=====================================================================
    #logisitc_regression = linear_model.SGDClassifier(
    #warm_start = False, #Warm start makes the model reuse old training data
    #max_iter = 2000, #Maximum number of interations
    #loss = 'modified_huber', #Still uses logistic regression under the hood, maybe use modified_huber instead of log_loss
    #penalty = 'l1',
    #alpha = 0.001, #makes probabilities more uncertain
    #)

    #NOTES FOR ML
    #Could also modified_huber
    #used to use LinearRegression this was not a good idea


    #Seperate training data into a train test Split
    #All this does is take our input data and our output data and split it into a set of training data
    #and a set of data the model hasn't seen
    if test_train_split == 0:
        #If no test data
        #Put all data into training
        in_train = in_data
        in_test = [[]]
        out_train = out_data
        out_test = [[]]
    else:
        #If data put aside to test is wanted
        in_train, in_test, out_train, out_test = train_test_split(in_data, out_data, test_size=test_train_split)

    if verbose == True:
        print("=== Start Training Linear Regression Model ===")
    #Train model
    #This function trains on the training data
    #trained_model = logisitc_regression.partial_fit(in_train, out_train, [-1.0, 1.0]);
    trained_model = logisitc_regression.fit(in_train, out_train)
    if not test_train_split == 0:
        #make predictions based on the test data
        predictions = trained_model.predict(in_test)

        #get the size of the test data for a loop (I bodged this code)
        size = len(in_test.toarray())
        #size = in_test.getnnz() #this didn't work
        if verbose == True:
            #Display test data
            for i in range(size):
                #print out predicted values
                input_values = in_test[i].toarray()
                expected_output = out_test[i]
                predicted_output = predictions[i]
                #print("Values: ")
                #print(input_values)
                print("Expected: " + str(expected_output))
                print("Predicted: " + str(predicted_output))
                print("")

    #Find a score for the machine learning model
    score = trained_model.score(in_data, out_data) #find score for all data (not just training or test data)

    if verbose == True:
        #Print out model score
        print("Model Score: " + str(score))

    if verbose == True:
        print("Saving model to: " + model_file_path)
    #Save model in serialised form
    pickle.dump(trained_model, open(model_file_path, 'wb'))


#Automatic train and test from dataset
def train_all_models():
    #Train start estimation
    train_model_and_save(START_DATASET_FILE_PATH, START_MODEL_FILE_PATH, True, DEFAULT_TEST_TRAIN_SPLIT)
    #Train in progress estimation
    train_model_and_save(IN_PROGRESS_DATASET_FILE_PATH, IN_PROGRESS_MODEL_FILE_PATH, True, DEFAULT_TEST_TRAIN_SPLIT)

#Automatic TRAIN ONLY from dataset
def retrain_all_models():
    #Train start estimation
    train_model_and_save(START_DATASET_FILE_PATH, START_MODEL_FILE_PATH, False, 0)
    #Train in progress estimation
    train_model_and_save(IN_PROGRESS_DATASET_FILE_PATH, IN_PROGRESS_MODEL_FILE_PATH, False, 0)

#Used to write new entries into the dataset
def add_to_dataset(new_startevaluationdata, new_currentevaluationdata, result_out):
    start_dataset_file = open(START_DATASET_FILE_PATH, 'a') # Open file in append mode
    in_progress_dataset_file = open(IN_PROGRESS_DATASET_FILE_PATH, 'a') # Open file in append mode

    CURRENTEVALATION_DATA_SIZE = len(new_currentevaluationdata)


    new_startevaluationdata_matrix = StartEvaluationData.get_data_as_matrix(new_startevaluationdata)

    new_currentevaluationdata_matrix = [CurrentEvaluationData.get_data_as_matrix(new_currentevaluationdata[i]) for i in range(CURRENTEVALATION_DATA_SIZE)]


    #Write to start_dataset_file
    line = ""
    line += str(result_out)
    fields = new_startevaluationdata_matrix[0]
    NUM_FIELDS = len(fields)
    for i in range(NUM_FIELDS):
        #Join field to string
        index = i + 1
        line += " " + str(index) + ":" + str(fields[i])
    start_dataset_file.write("\n" + line) #Write line

    #Write to in_progress_dataset_file
    for line_index in range(CURRENTEVALATION_DATA_SIZE):
        #Loop through all new data points for lines
        line = ""
        line += str(result_out)
        fields = new_currentevaluationdata_matrix[line_index][0]
        NUM_FIELDS = len(fields)
        for i in range(NUM_FIELDS):
            #Join field to string
            index = i + 1
            line += " " + str(index) + ":" + str(fields[i])
        in_progress_dataset_file.write("\n" + line) #Write line

    start_dataset_file.close()
    in_progress_dataset_file.close()
