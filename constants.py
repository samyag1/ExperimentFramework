#import pygame.locals
#import pyaudio

# path constants
IMAGES_PATH = 'images'
STIMULI_PATH = 'stimOrder'
LOGS_PATH = 'logs'
SESSIONS_PATH = 'SessionsImages'
MASKS_PATH = 'masks'

# Experiment constants
BACKGROUND_COLOR = (0.25,0.25,0.25,0.25)
FIXATION_COLOR = (1,1,1,1)
TASK_COLOR = (0,.5,.5,1.0)
NULL_STIM_ID = 0
VISUAL_ANGLE = 12.0
PRESCAN_DUMMIES = 5
NO_ITI = -1
NULL_ID = 0
NULL_FILENAME = 'null'
NULL_LOG_ID = -1

# Stimulus Parameters constants
PARAM_LIST_START_SYMBOL = '$$'
MASK_COUNT_PARAM = 'MaskCount'
MASK_ON_PARAM = 'Mask%iOn'
MASK_OFF_PARAM = 'Mask%iOff'
MASK_ID_PARAM = 'Mask%iID'
STIM_OFF_FRAME_PARAM = 'StimOffFrame'
STIM_OFF_TIME_PARAM = 'StimOffTime'

# Viewport Constnats
FIXATION_VIEWPORT = 'FixationViewport'
VALENCE_SCALE_VIEWPORT = 'ValenceScaleViewport'
TEXT_ENTRY_VIEWPORT = 'TextEntryViewport'
STIMULUS_VIEWPORT = 'StimulusViewport'
EMPTY_VIEWPORT = 'EmptyViewport'
MASKS_VIEWPORT = 'MasksViewport'

#RESPONSE_KEYS = [pygame.locals.K_1, pygame.locals.K_2, pygame.locals.K_3, pygame.locals.K_4]

# TODO - uncomment if I get the audio recording working
## # audio recording constants
## AUDIO_FORMAT = pyaudio.paInt16
## AUDIO_CHANNELS = 1
## AUDIO_RATE = 44100
## AUDIO_TAG_FILENAME = 'image%04i.wav'
## AUDIO_PATH = 'audio'



