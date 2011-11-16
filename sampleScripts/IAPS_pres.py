import datetime
import experiment
from constants import *
from constantsIAPS import *
from experimentHandlers import *


#####################################
#  Create the Experiment             #
######################################

# create the Experiment object which will do all the work of running the experiment
# tell the experiment to preload the images, since there are a small enough number per run
experiment = experiment.Experiment(preloadImages=True, fixationCross=True)

######################################
#  get subject and run info          #
######################################

# ask the operator to enter the subject ID and run # to create the log file
sessionNoStr = raw_input('Please enter session #:')
runNo = int(raw_input('Please enter run #:'))
subjectID = int(raw_input('Please enter subject ID #:'))

# determine if this is a validation or estimation run based on the number
validationRun = False
if VALIDATION_RUN_NOS.count(runNo) > 0: 
	validationRun = True

######################################
#  Create the log file               #
######################################

# NOTE** I don't use quickInit because I don't want to show the instructions
# for every run, just the first two, and quickInit always shows the instructions

#create the log file
piloting = False
logFilename = ''
now = datetime.datetime.now()
if sessionNoStr.lower() == PILOT_SESSION_ID:
	piloting = True
	logFilename = "IAPS_subject%03i_PilotSession_run%0i_%i-%i-%i.csv" % (subjectID, runNo, now.month, now.day, now.year)
else:
	sessionNo = int(sessionNoStr)
	logFilename = "IAPS_subject%03i_session%02i_run%0i_%i-%i-%i.csv" % (subjectID, sessionNo, runNo, now.month, now.day, now.year)

# check if file exists, and ask user to overwrite or append if it does
experiment.openLogFile(logFilename)

#####################################
#  Initialize Vision Egg  #
#####################################

experiment.initVisionEgg()

#####################################
#  Figure input filenames and load  #
#####################################
		
# get the filenames for the stim and color orders
if validationRun:
	if piloting:
		stimFilename = PILOT_VAL_STIM_FILENAME % (runNo)
		imagesFilename = PILOT_VAL_FILELIST_FILENAME % (runNo)
	else:
		stimFilename = VAL_STIM_FILENAME % (sessionNo, runNo)
		imagesFilename = VAL_FILELIST_FILENAME % (sessionNo, runNo)
else:
	if piloting:
		stimFilename = PILOT_EST_STIM_FILENAME % (runNo)
		imagesFilename = PILOT_EST_FILELIST_FILENAME % (runNo)
	else:
		stimFilename = EST_STIM_FILENAME % (sessionNo, runNo)
		imagesFilename = EST_FILELIST_FILENAME % (sessionNo, runNo)

# determine the filename for the visual angle measurements
if piloting:
	visualAngleFilename = PILOT_VISUAL_ANGLE_FILENAME % (subjectID)
else:
	visualAngleFilename = VISUAL_ANGLE_FILENAME % (subjectID, sessionNo)

# load the simutlis input files which tell the experiment which stim files to show
# and for how long to show them
experiment.loadInputFiles(stimFilename, imagesFilename, visualAngleFilename)

########################################
# Run the instructions		       #
########################################

# only show the instructions the first time
if runNo == ESTIMATION_RUN_NOS[0] or runNo == VALIDATION_RUN_NOS[0]:
	if validationRun:
		text = 'In this experiment you will see a series of images that repeat multiple times. There will be a white fixation cross (+) located in the center of the screen. We ask that you maintain focus on the cross at all times. \n\n Your task is to judge whether they are negative, neutral or positive. For negative press the leftmost button with your index finger, for neutral the second button with your middle finger, and for positive the third button with your ring finger. Categorize each image as quickly as you can. Since you will see multiple presentations of eaceh image, it is ok if you change your rating for successive viewings.\n\nPlease let your experimenter know when you are ready to continue...'
	else:
		text = 'In this experiment you will see a series of images. There will be a white fixation cross (+) located in the center of the screen. We ask that you maintain focus on the cross at all times. \n\n Your task is to judge whether they are negative, neutral or positive. For negative press the leftmost button with your index finger, for neutral the second button with your middle finger, and for positive the third button with your ring finger. Categorize each image as quickly as you can.\n\nPlease let your experimenter know when you are ready to continue...'
	experiment.showInstructions(text)

########################################
# Initialize the Physio data collection#
########################################

#experiment.startPhysio()

########################################
# Wait for the scanner to start	       #
########################################

experiment.waitForScanner()

########################################
# Add Experiment Handlers              #
########################################

# add a time handler which will turn the stimulus off after 1 second
experiment.addTimeHandler(StimOffTimeHandler(experiment, offTime=1))

# add a handler that will record the inputs from the scanner's 4 Button response box
experiment.addKeyHandler(Scanner4ButtonKeyHandler(experiment))

# tell the experiment that a trial ends after two TTL pulses
experiment.setTrialFinishedHandler(TTLTrialFinishedHandler(experiment,ttlTotal=2))

########################################
# Start the Experiment Loop            #
########################################

# finally, start the experiment loop which will display
# all the stimuli using the handlers crated above
experiment.runExperiment()

########################################
# Wait end Dummies       	       #
########################################

# wait for another 5 dummies (10  seconds) to let HRF settle down
experiment.waitDummies(5)
