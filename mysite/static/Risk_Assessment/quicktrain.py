
import modeltrainer #Import trainer to use

import sys #Used to fetch command line arguments

#Code if this file is executed through the command line
#TO RUN TRAINING CODE
#Type: python3 modeltrainer.py [DATASET_FILEPATH] [MODEL_FILENAME]
#TO TRAIN ALL MODELS AT ONCE RUN
#Type: python3 modeltrainer.py

args = sys.argv; #Get arguments

no_of_arguments = len(args) #Get number of arguments note first/0th argument is just run program call

if no_of_arguments == 3:
    #If the code ran with the correct amount of arguments
    modeltrainer.train_model_and_save(args[1], args[2], True, modeltrainer.DEFAULT_TEST_TRAIN_SPLIT) #First argument is just the call to running the program
elif no_of_arguments == 1:
    #call function if file is run through command line
    modeltrainer.train_all_models()
else:
    print("Incorrect number of arguments")
    print("Use: python3 modeltrainer.py")
    print("or use: python3 modeltrainer.py [DATASET_FILEPATH] [MODEL_FILENAME]")
