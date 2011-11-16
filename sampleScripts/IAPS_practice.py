import datetime
import experiment
from constants import *
from constantsIAPS import *
from experimentHandlers import *

######################################
#  Create the Experiment             #
######################################

# create the Experiment object which will do all the work of running the experiment
# tell the experiment to preload the images, since there are a small enough number per run
experiment = experiment.Experiment(preloadImages=True, fixationCross=True)

######################################
#  get subject and run info          #
######################################

# ask the operator to enter the subject ID and run # to create the log file
runNo = int(raw_input('Please enter run #:'))
subjectID = int(raw_input('Please enter subject ID #:'))
inScanner = raw_input('Is this in the scanner? (y or n):') == 'y'

######################################
#  Initialize the experiment         #
######################################

#create the log filename
now = datetime.datetime.now()
logFilename = "IAPS_practice_subject%03i_run%03i_%i-%i-%i.csv" % (subjectID, runNo, now.month, now.day, now.year)

# determine if this is a validation or estimation run based on the number
validationRun = False
if runNo == 2: 
	validationRun = True

# get the filenames for the stim and color orders
practiceRun = 1
if inScanner:
	practiceRun = 2
if validationRun:
	stimFilename = PRACTICE_VAL_STIM_FILENAME % (practiceRun)
	imagesFilename = PRACTICE_VAL_FILELIST_FILENAME % (practiceRun)
else:
	stimFilename = PRACTICE_EST_STIM_FILENAME % (practiceRun)
	imagesFilename = PRACTICE_EST_FILELIST_FILENAME % (practiceRun)

# determine the filename for the visual angle measurements
visualAngleFilename = PRACTICE_VISUAL_ANGLE_FILENAME % (subjectID)

# show instructions
instructionsText = ''
if validationRun:
	instructionsText = 'In this experiment you will see a series of images that repeat multiple times. There will be a white fixation cross (+) located in the center of the screen. We ask that you maintain focus on the cross at all times. \n\n Your task is to judge whether they are negative, neutral or positive. For negative press the leftmost button with your index finger, for neutral the second button with your middle finger, and for positive the third button with your ring finger. Categorize each image as quickly as you can. Since you will see multiple presentations of eaceh image, it is ok if you change your rating for successive viewings.\n\nPlease let your experimenter know when you are ready to continue...'
else:
 	instructionsText = 'In this experiment you will see a series of images. There will be a white fixation cross (+) located in the center of the screen. We ask that you maintain focus on the cross at all times. \n\n Your task is to judge whether they are negative, neutral or positive. For negative press the leftmost button with your index finger, for neutral the second button with your middle finger, and for positive the third button with your ring finger. Categorize each image as quickly as you can.\n\nPlease let your experimenter know when you are ready to continue...'

# use this function to initialize vision egg, open the log file,
# read in the input files and display the instructions
experiment.quickInit(logFilename, stimFilename, imagesFilename, visualAngleFilename, instructionsText)

########################################
# Add all Experiment handlers          #
########################################

# add a time handler which will turn the stimulus off after 1 second
experiment.addTimeHandler(StimOffTimeHandler(experiment,offTime=1))

# add a handler that will record the inputs from the scanner's 4 Button response box
experiment.addKeyHandler(Scanner4ButtonKeyHandler(experiment))

# tell the experiment that a trial ends after 4 seconds
experiment.setTrialFinishedHandler(TimeTrialFinishedHandler(experiment,seconds=4.0))

########################################
# Start the Experiment Loop            #
########################################

# finally, start the experiment loop which will display
# all the stimuli using the handlers crated above
experiment.runExperiment()
