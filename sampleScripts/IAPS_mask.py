import sys
sys.path.append('../')
import datetime
import experiment
from constants import *
from constantsVAMeasurements import *
from constantsIAPS import *
from experimentHandlers import *

######################################
#  Create the Experiment             #
######################################

# create the Experiment object which will do all the work of running the experiment
# set the Inter-Trial Interval (ITI) to 500ms, and 
# tell the experiment NOT to preload the images, as there are two many
experiment = experiment.Experiment(iti=0.5, preloadImages=False, fixationCross=True)

######################################
#  get subject info                  #
######################################

# ask the operator to enter the subject ID and run # to create the log file
subjectID = int(raw_input('Please enter subject ID #:'))

######################################
#  Initialize the experiment         #
######################################

#create the log file
now = datetime.datetime.now()
logFilename = "IAPS_SemanticMask_subject%03i_%i-%i-%i.csv" % (subjectID, now.month, now.day, now.year)

# TODO - Make a unique filename
# determine the filename for the visual angle measurements
visualAngleFilename = RATING_VISUAL_ANGLE_FILENAME % (subjectID)

instructions = ''
# use the experiment to load the input files

# use this function to initialize vision egg, open the log file,
# read in the input files and display the instructions
experiment.quickInit(logFilename, MASKS_STIM_FILENAME, MASKS_FILELIST_FILENAME, visualAngleFilename, instructions)

########################################
# Add Experiment Handlers              #
########################################

# add a time handler which will turn the stimulus off after the number of
# frames specified in the stimParams file
experiment.addTimeHandler(StimOffTimeHandler(experiment,offFrame=1,useStimParams=True))

# this handler will display the masks given in the file referenced below
# in the order and number specified in the stimParams file
masksPath = os.path.join(MASKS_PATH, MASKS_FILES_FILENAME)
experiment.addTimeHandler(ShowMasksTimeHandler(experiment,masksPath))

############### Key Handlers ####################

# add a handler that will display the text that the user types
# in the bottom of the screen
experiment.addKeyHandler(TextEntryKeyHandler(experiment))

################# Trial Finished Handler #################

# set the TrialFinished handler to finish when a response is made
# in this case it's when the user has entered a sentence in TextEntryKeyHandler
experiment.setTrialFinishedHandler(ResponseTrialFinishedHandler(experiment, count=1))

########################################
# Start the Experiment Loop            #
########################################

# finally, start the experiment loop which will display
# all the stimuli using the handlers crated above
experiment.runExperiment()
