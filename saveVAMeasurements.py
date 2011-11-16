import sys
sys.path.append('../shared')
import csv
import os
from constants import *


measurements = [0,0,0]
subjectID = int(raw_input('Please enter subject ID #:'))
sessionNoStr = raw_input('Please enter session #:')
measurements[EYE_TO_MIRROR_INDEX] = float(raw_input('Please enter distance from EYE TO MIRROR:'))
measurements[MIRROR_TO_SCREEN_INDEX] = float(raw_input('Please enter distance from MIRROR TO SCREEN:'))
measurements[SCREEN_HEIGHT_INDEX] = float(raw_input('Please enter the HEIGHT of the SCREEN in inches:'))

if sessionNoStr.lower() == PILOT_SESSION_ID:
	filename = PILOT_VISUAL_ANGLE_FILENAME % (subjectID)
elif sessionNoStr.lower() == PRACTICE_SESSION_ID:
	filename = PRACTICE_VISUAL_ANGLE_FILENAME % (subjectID)
elif sessionNoStr.lower() == LOCALIZER_SESSION_ID:
	filename = LOCALIZER_VISUAL_ANGLE_FILENAME % (subjectID)
elif sessionNoStr.lower() == LUMTEST_SESSION_ID:
	filename = LUMTEST_VISUAL_ANGLE_FILENAME % (subjectID)
elif sessionNoStr.lower() == RATING_SESSION_ID:
	filename = RATING_VISUAL_ANGLE_FILENAME % (subjectID)
else:
	sessionNo = int(sessionNoStr)
	filename = VISUAL_ANGLE_FILENAME % (subjectID, sessionNo)

filePath = os.path.join(LOGS_PATH, filename)
f = open(filePath, 'w')
writer = csv.writer(f)
writer.writerow(measurements)
f.close()
