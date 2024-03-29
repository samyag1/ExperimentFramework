# IAPS constants
SESSION_COUNT = 5 
VALIDATION_RUN_NOS = [2,4,7,9]
ESTIMATION_RUN_NOS = [1,3,5,6,8,10]
ESTIMATION_RUN_COUNT = len(ESTIMATION_RUN_NOS)
VALIDATION_RUN_COUNT = len(VALIDATION_RUN_NOS)
PRACTICE_RUN_COUNT = 1 # TODO CHANGE BACK TO 2 IF NECESSARY
PROFUSION_RUN_TIME = 332 # profusion runtime is 5:32, wich is 332 seconds
RESTINGSTATE_TTL_COUNT = 140 # resting state runtime is 6:07 with ~2.5TR, which works out to 140 TTLs
PILOT_ESTIMATION_EXEMPLAR_COUNT = 36
ESTIMATION_EXEMPLAR_COUNT = 48
VALIDATION_EXEMPLAR_COUNT = 9
ESTIMATION_REPEAT_COUNT = 2
NULL_COUNT = 8
NULL_INTERVAL = (ESTIMATION_EXEMPLAR_COUNT*ESTIMATION_REPEAT_COUNT) / NULL_COUNT
BREAK_INTERVAL = 150# we want a break approximately every 5 minutes, and assuming ~2 sec / rating, that's 5*60 = 300 / 2 = 150

# filename constants
EST_STIM_FILENAME = 'estStimOrder_Session%i_Run%i.csv'
EST_FILELIST_FILENAME = 'estFileList_Session%i_Run%i.csv'
VAL_STIM_FILENAME = 'valStimOrder_Session%i_Run%i.csv'
VAL_FILELIST_FILENAME = 'valFileList_Session%i_Run%i.csv'
PILOT_EST_STIM_FILENAME = 'estStimOrder_PilotSession_Run%i.csv'
PILOT_EST_FILELIST_FILENAME = 'estFileList_PilotSession_Run%i.csv'
PILOT_VAL_STIM_FILENAME = 'valStimOrder_PilotSession_Run%i.csv'
PILOT_VAL_FILELIST_FILENAME = 'valFileList_PilotSession_Run%i.csv'
PRACTICE_EST_STIM_FILENAME = 'estStimOrder_PracticeSession%i.csv'
PRACTICE_EST_FILELIST_FILENAME = 'estFileList_PracticeSession%i.csv'
PRACTICE_VAL_STIM_FILENAME = 'valStimOrder_PracticeSession%i.csv'
PRACTICE_VAL_FILELIST_FILENAME = 'valFileList_PracticeSession%i.csv'
EXAMPLES_SCANNER_FILELIST_FILENAME = 'fileList_ExamplesScanner.csv'
EXAMPLES_MOCK_FILELIST_FILENAME = 'fileList_ExamplesMock.csv'
RATINGS_STIM_FILENAME = 'stimOrder_Ratings.csv'
RATINGS_FILELIST_FILENAME = 'fileList_Ratings.csv'
LOCALIZER_OBJECT_STIM_FILENAME = 'objStimOrder%02d.csv'
LOCALIZER_RETINOTOPY_STIM_FILENAME = 'retStimOrder.csv'
MASKS_STIM_FILENAME = 'stimParams_Mask.csv'
MASKS_FILELIST_FILENAME = 'fileList_Mask.csv'
MASKS_FILES_FILENAME = 'maskFilenames.csv'

# examples scripts constnats
EXAMPLE_NEGATIVE_INDEX = 0
EXAMPLE_NEUTRAL_INDEX = 1
EXAMPLE_POSITIVE_INDEX = 2
NEGATIVE = 'negative'
NEUTRAL = 'neutral'
POSITIVE = 'positive'


# IAPS StimCreation constants
PILOT_ESTIMATION_EXEMPLAR_COUNT = 36
ESTIMATION_EXEMPLAR_COUNT = 48
VALIDATION_EXEMPLAR_COUNT = 9
ESTIMATION_REPEAT_COUNT = 2
NULL_COUNT = 8
NULL_INTERVAL = (ESTIMATION_EXEMPLAR_COUNT*ESTIMATION_REPEAT_COUNT) / NULL_COUNT
