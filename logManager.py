import os
import pdb
import pygame.locals
from constants import *

class LogData:

    def __init__(self):
        # setup buffers used for logging
        self.trialStartTimes = [] # trial start time (absolute)
        self.trialStopTimes = [] # trial end time (absolute)
	self.stimOnTimes = [] 
	self.stimOffTimes = [] 
	self.stimFilenames = []
	self.responseTimes = []
	self.responseValues = []
        self.trialCount = 0


class LogManager:

#####################################
#  Constructor	                    #
#####################################

    def __init__(self):

        self.logFile = None
        self.append = False
        self.lastStimPresented = 0
        
#####################################
#  Public Interface	            #
#####################################

    def openLogFile(self, logFilename):

        # create the pathname for the log file
        logPath = os.path.join(LOGS_PATH, logFilename)

        # if the file exists, then ask the user what to do
        if os.path.exists(logPath):
            answered = False
            while(not(answered)):

                # tell the user their options
                answer = raw_input("the log file that will be created for this run already exists. Type [o]verwrite, [a]ppend, (c)ontinue from last response, or [e]xit:")

                # overwrite the existing log file
                if answer == 'o':
                    self.logFile = open(logPath, "w")
                    answered = True
                # append to the existing log file, but indicate that the stim presentation
                # shoudl start from the beginning
                elif answer == 'a':
                    self.logFile = open(logPath, "a")
                    answered = True
                    self.append = True
                # append to the existing log file, but indicate that stim presentation
                # should start from the last stim presented in the current log file
                elif answer == 'c':
                    self.lastStimPresented = self.findLastStimPresented(logPath)
                    self.logFile = open(logPath, "a")
                    answered = True
                    self.append = True
                # just exit the script
                elif answer == 'e':
                    exit()
        # otherwise open it for reading
        else:
            self.logFile = open(logPath, "w")
                    
        return self.lastStimPresented

        # TODO - figure out when the firstStimPresented is passed in
        # logs all the info collected during the run

        # TODO - also log the stimParams for each trial??
    def logRun(self, logData, firstStimPresented=1):

            # do nothing if there is nothing to log
            if logData.trialCount == 0:
                    return

            # determine the max length of response arrays for any trial
            maxResponses = 0
            maxResponses = max([max(len(res),maxResponses) for res in logData.responseValues])

            # create the header for the log file as long as this isn't an append run
            if not(self.append):
                    header = "trial #,trialStart,trialEnd,imageFilename,imageOn,imageOff"

                    # add the response column headers, which can vary from run to run
                    # based on the max number of presses for a given trial
                    for n in xrange(maxResponses):
                            header = header + ", ResponseTime%i,ResponseValue%i" % (n+1, n+1)

                    # add the newline at the end
                    header = header + "\n"

                    # write the header
                    self.logFile.write(header)

# TODO - write out the stimParams
            curOut = ''
            for d in xrange(len(logData.stimOnTimes)):

                    # store all the variables into the list except the response Onsets
                    curOut = curOut + "%i,%.5f,%.5f,%s,%.5f,%.5f" % (d+self.lastStimPresented+1, \
                                                                     logData.trialStartTimes[d],\
                                                                     logData.trialStopTimes[d],\
                                                                     logData.stimFilenames[d], \
                                                                     logData.stimOnTimes[d], \
                                                                     logData.stimOffTimes[d])

                    # get the list of current response
                    curResponseTimes = logData.responseTimes[d]
                    curResponseValues = logData.responseValues[d]

                    # put an 'na' into the position of all response lists
                    # that aren't the max length response list
                    for n in xrange(len(curResponseTimes),maxResponses):
                            curResponseTimes.append(-1)
                            curResponseValues.append(-1)
                            
                    # write out all the responses
                    for n in xrange(maxResponses):
                            curOut = curOut + ",%.5f,%s" % (curResponseTimes[n], \
                                                            str(curResponseValues[n]))

                    # add the newline
                    curOut = curOut + "\n"

            # write the entire run's output
            self.logFile.write(curOut)

    def closeLog(self):
        if self.logFile != None:
            self.logFile.close()
            self.logFile = None
            
        
    def cancelLog(self):      
        if self.logFile != None:
            self.logFile.write("Task quit with escape key at %.5f" % (getTime()))
            self.logFile.close()
            self.logFile = None

    def writeDummy(self, dummy, curTime):
	if self.logFile != None:
		self.logFile.write("Dummy %d, %.5f\n" % (dummy, curTime))

#####################################
#  Helper Functions	            #
#####################################

    def findLastStimPresented(self, logPath):

            # open the file for reading
            logFile = open(logPath, "r")
            reader = csv.reader(logFile)

            # Assuming that the first column is only a number when it represented the stim # of the last presented stim
            lastStimPresented = 0
            for line in reader:
                    try:
                            lastStimPresented = int(line[0])
                    except ValueError:
                            pass

            # close the file
            logFile.close()

            return lastStimPresented

