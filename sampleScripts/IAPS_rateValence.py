import datetime
import experiment
from constants import *
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
logFilename = "IAPS_ValenceRating_subject%03i_%i-%i-%i.csv" % (subjectID, now.month, now.day, now.year)

# determine the filename for the visual angle measurements
visualAngleFilename = RATING_VISUAL_ANGLE_FILENAME % (subjectID)

instructions = 'In this experiment you will see a series of images. There will be a white fixation cross (+) located in the center of the screen. We ask that you maintain focus on the cross at all times. \n\n Your task is to judge how negative or positive each image is on a 1-9 scale with 1 being extremely negative, 5 being neutral, and 9 being extremely positive. For example, a 6 would be close to neutral, but slightly positive. Categorize each image as quickly as you can. We want your first impression, but don\'t overthink it. Don\'t rush too quickly as to mis-categorize either though. \n\nPlease let your experimenter know when you are ready to continue...'
# use the experiment to load the input files

# use this function to initialize vision egg, open the log file,
# read in the input files and display the instructions
experiment.quickInit(logFilename, RATINGS_STIM_FILENAME, RATINGS_FILELIST_FILENAME, visualAngleFilename, instructions)

########################################
# Add Experiment Handlers              #
########################################

######## Viewports ######################

# add a viewport that will display the 1 to 9 valence rating scale at the top 
experiment.addViewport(name=VALENCE_SCALE_VIEWPORT)

############### Key Handlers ####################

# add a handler that will log key presses between 1 and 9, the valence rating here
experiment.addKeyHandler(Rate1To9KeyHandler(experiment))

################## Null Stim Handlers ################

# tell the experiment to give the user a break every time it encounters a null stim
experiment.addNullStimHandler(BreakNullStimHandler(experiment))

################# Trial Finished Handler

# set the TrialFinished handler to move one once the user has given a response
# in this case we're using the Rate1To9 key handler for the response
experiment.setTrialFinishedHandler(ResponseTrialFinishedHandler(experiment, count=1))

########################################
# Start the Experiment Loop            #
########################################

# finally, start the experiment loop which will display
# all the stimuli using the handlers crated above
experiment.runExperiment()
