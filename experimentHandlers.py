import os
import csv
import pygame.locals
from constants import *

#######################################
# Base Classes                        #
#######################################

# base class for all handlers
class Handler:

    def __init__(self, experiment):
        self.experiment = experiment

    def newTrial(self):
        pass

# handles time events, like turning stimuli off, adding masks, flashing backgrounds, etc.
class TimeHandler(Handler):

    def conditionMet(self, elapsedTime, elapsedFrames, stimParams, responses):
        return False

    def handleTime(self, elapsedTime, elapsedFrames, stimParams):
        pass

# handlers user key presses. Eveyrthing from TTL pulses, to Escape ending the experiment, to responses
class KeyHandler(Handler):

    def conditionMet(self, keyCode, keyValue, modifiers, stimParams, responses):
        return False

    # TODO - Add the logData to the parameters passed in so that handlers can add
    # fields to be logged - do this for all handlers
    def handleKey(self, keyCode, keyValue, modifiers, stimParams):
        '''
        return params: [1] if a response is to be logged, this is the response, otherwise None
        '''
        return None

# Handles events that are based on user input. Since the KeyHandlers decide what keys count
# as an actual response, these are called after the Key Handlers to do additional processing
class ResponseHandler(Handler):

    def __init__(self, experiment, responses):
        Handler.__init__(experiment)
        self.responses = responses

    def handleResponse(self, responseCount):
        pass
    
# used to tell the experiment what to do when it encounters a NULL trial (0)
class NullStimHandler(Handler):

    def handleNullStim(self, stimParams):
        '''
        This method is called whenever there\'s a NULL stim code (0) in the stim
        train to be presented. Returning True indicates that all the handling
        for the NULL stim is done within this handler, and the next stim should
        be presented. False means to continue on with normal handling
        '''
        return False

# experiment asks this handler when the current trial should finish
class TrialFinishedHandler(Handler):

    def trialFinished(self, elapsedTime, elapsedFrames, events, responses, stimParams):
        '''
        Indicates whether the current trial should finish. Return True to finish False otherwise
        '''
        return False

#######################################
# Time Handlers                       #
#######################################

# Turns off the stimuli at a specific elapsed time, measured in seconds or frames
class StimOffTimeHandler(TimeHandler):

    def __init__(self, experiment, offTime=None, offFrame=None, useStimParams=False):
        Handler.__init__(self,experiment)
        self.offTime = offTime
        self.offFrame = offFrame
        self.useStimParams=useStimParams

    def conditionMet(self, elapsedTime, elapsedFrames, stimParams, responses):

        # if the stimulus has already been turned off, then return False
        if not(self.experiment.stimulusShown()):
            return False

        # the image is still being show, so if the number of frames or time has passed
        # since the beginning of the trial, then return true, otherwise false
        if self.offFrame != None:
            offFrame = self.offFrame
            if self.useStimParams:
                offFrame = int(stimParams[STIM_OFF_FRAME_PARAM])
            return elapsedFrames >= offFrame
        else:
            offTime = self.offTime
            if self.useStimParams:
                offTime = int(stimParams[STIM_OFF_TIME_PARAM])
            return elapsedTime >= offTime
        

    def handleTime(self, elapsedTime, elapsedFrames, stimParams):

        # tell the experiment to clear the stimulus from the screen
        self.experiment.clearStimulus()
            
class ShowMasksTimeHandler(TimeHandler):

    def __init__(self, experiment, maskFilenames):
        # call the base class constructor
        Handler.__init__(self,experiment)

        # create a member variable that will keep track of which mask is currently being shown
        self.curMaskToShow = 1
        self.maskOn = False

        # DEBUGGING
        self.onTime = 0
        
        # add the masks viewport into the experiment which will hold all the mask images
        experiment.addViewport(name=MASKS_VIEWPORT, viewport=EMPTY_VIEWPORT)

        # load the file which contains all the mask filenames
        f = open(maskFilenames, 'r')
        csvreader = csv.reader(f)

        # read in the image filenames
        self.maskFilenames = csvreader.next()
        f.close()
        
        # load all the mask images
        self.masks = []
        for maskFilename in self.maskFilenames:
            maskPath = os.path.join(MASKS_PATH, maskFilename)
            self.masks.append(self.experiment.loadImage(filename=maskPath))

    def conditionMet(self, elapsedTime, elapsedFrames, stimParams, responses):
        
        # if the stimulus is not yet been turned off, then indicate
        # no handling needed as the masks come after the stimulus
        if self.experiment.stimulusShown():
            return False

        # get the mask count parameter. If the number of masks to be shown for this
        # trial have already been shown, then indicate no handling is needed
        maskCount = int(stimParams[MASK_COUNT_PARAM])
        if self.curMaskToShow > maskCount:
            return False
        
        # if there is a mask already being shown, then find out what frame it should
        # be turned off at, and indicate handling is needed if that frame is here already
        if self.maskOn:
            
            # create the parameter name for the current mask and retrieve it
            paramName = MASK_OFF_PARAM % (self.curMaskToShow)
            curMaskOffFrame = int(stimParams[paramName])

            # if the elapsed frames equal or have exceeded the frame in which this
            # mask is to be turned off, then handling is needed
            return elapsedFrames >= curMaskOffFrame
        else:

            # create the parameter name for the current mask and retrieve it
            paramName = MASK_ON_PARAM % (self.curMaskToShow)
            curMaskOnFrame = int(stimParams[paramName])

            # if the elapsed frames equal or have exceeded the frame in which this
            # mask is to be turned on, then handling is needed
            return elapsedFrames >= curMaskOnFrame

    def newTrial(self):
        # reset the trial dependent variables
        self.curMaskToShow = 1
        self.maskOn = False
        
    def handleTime(self, elapsedTime, elapsedFrames, stimParams):

        # get the masks stimulus which contains the images
        masksViewport = self.experiment.getViewport(MASKS_VIEWPORT)
        
        # if there is a mask on, then turn it off
        if self.maskOn:

            # clear the masks viewport and redraw the viewports
            masksViewport.parameters.stimuli = []

            # reset the flag indicating a mask is being shown
            self.maskOn = False

            # increment the counter indicating the mask to show next
            self.curMaskToShow = self.curMaskToShow + 1

            # DEBUGGING
            print self.experiment.getTime() - self.onTime
            self.onTime = 0
        else:

            # get the ID of the mask after the one currently shown from the parameters
            paramName = MASK_ID_PARAM % (self.curMaskToShow)
            maskID = int(stimParams[paramName])

            # put the desired mask into the masksViewport so it is displayed
            masksViewport.parameters.stimuli = [self.masks[maskID-1]]

            # set the flag indicating a mask is being shown
            self.maskOn = True            

            # DEBUGGING
            self.onTime = self.experiment.getTime()

        # redraw the viewport now that a mask has either been added or removed
        self.experiment.redrawViewports()

# TODO - Make a beep handler Time Handler

# TODO - Make a background color change Time Handler

# TODO - Make a play sound file Time Handler

#######################################
# Key Handlers                        #
#######################################

class TextEntryKeyHandler(KeyHandler):

    def __init__(self, experiment):

        # call the base class version to store the experiment
        Handler.__init__(self, experiment)

        # create the viewport that will store the text entry
        self.experiment.addViewport(name=TEXT_ENTRY_VIEWPORT)

    def conditionMet(self, keyCode, keyValue, modifiers, stimParams, responses):
        # just return true here, as it's faster than doing the check twice
        return True

    def handleKey(self, keyCode, keyValue, modifiers, stimParams):

        # get the text entry viewport from the experiment
        textEntryViewport = self.experiment.viewports[TEXT_ENTRY_VIEWPORT]
        textEntry = textEntryViewport.parameters.stimuli[0]

        # the user has pressed a letter (or space) so enter it on the screen
        response = None
        redraw = False
        if (self.isLetter(keyCode)): 
            textEntry.parameters.text+=keyValue
            redraw = True
        # the user pressed return, so exit this loop and move on to the next image
        elif keyCode == pygame.locals.K_BACKSPACE:
            textEntry.parameters.text=textEntry.parameters.text[:-1]
            redraw = True
        elif keyCode == pygame.locals.K_RETURN:
            # store and clear the text from the text entry viewport
            response = textEntry.parameters.text
            textEntry.parameters.text = ''

            # tell the experiment to clear the stimulus from the screen
            self.experiment.clearStimulus()
            
            # set the flags indicating a redraw was necessary and the stim was turned off
            redraw = True
 
        # if the text changes, then redraw the viewports with the new text
        if redraw:
            self.experiment.redrawViewports()

        # return the flag indicating whether the stimulus was turned off,
        # and the response (which defaulted to None)
        return response

    def isLetter(self, key):
        if (key >= pygame.locals.K_a and key <= pygame.locals.K_z) or key == pygame.locals.K_SPACE or key == pygame.locals.K_PERIOD:
            return True
        else:
            return False


class EscapeKeyHandler(KeyHandler):

    def conditionMet(self, keyCode, keyValue, modifiers, stimParams, responses):
        return keyCode == pygame.locals.K_ESCAPE

    def handleKey(self, keyCode, keyValue, modifiers, stimParams):

        # first log the data that has been collected thus far
        self.experiment.logManager.logData(self.experiment.logData)

        # then tell the log manager the experiment is being cancelled
        self.experiment.logManager.cancelLog()

        if self.experiment.peripheralsManager != None:
            self.experiment.peripheralsManager.runStop()

        # now exit the script. This will cause the destructor of the experiment to be called
        # which will close the vision egg screen
        exit()

class ButtonKeyHandler(KeyHandler):

    def __init__(self, experiment, keys, responsesToRecord):
        Handler.__init__(self, experiment)
        self.responseKeys = keys
        self.responsesToRecord

    def conditionMet(self, keyCode, keyValue, modifiers, stimParams, responses):

        # if this handler was specified as only recording certain responses, then
        # return indicate the condition isn't met if the number of response already
        # made wasn't specified
        if len(self.responsesToRecord) > 0 and\
           not(self.responsesToRecord.__contains__(len(responses)+1)):
            return False
        
        # simply see if the key pressed is one of the response Keys
        # (the 4 buttons on the scanner response box)
        return self.responseKeys.__contains__(keyCode)

    def handleKey(self, keyCode, keyValue, modifiers, stimParams):

        # return the string representation of the key pressed as a response to be logged
        return keyValue
    

class Scanner4ButtonKeyHandler(KeyHandler):

    def __init__(self, experiment, responsesToRecord=[]):
        keys = [pygame.locals.K_1, \
                pygame.locals.K_2, \
                pygame.locals.K_3, \
                pygame.locals.K_4]
        ButtonKeyHandler.__init__(self, experiment, keys, responsesToRecord)


class Rate1To9KeyHandler(KeyHandler):

    def __init__(self, experiment, responsesToRecord=[]):
        keys = [pygame.locals.K_1, \
                pygame.locals.K_2, \
                pygame.locals.K_3, \
                pygame.locals.K_4, \
                pygame.locals.K_5, \
                pygame.locals.K_6, \
                pygame.locals.K_7, \
                pygame.locals.K_8, \
                pygame.locals.K_9, \
                pygame.locals.K_KP1, \
                pygame.locals.K_KP2, \
                pygame.locals.K_KP3, \
                pygame.locals.K_KP4, \
                pygame.locals.K_KP5, \
                pygame.locals.K_KP6, \
                pygame.locals.K_KP7, \
                pygame.locals.K_KP8, \
                pygame.locals.K_KP9]
        ButtonKeyHandler.__init__(self, experiment, keys, responsesToRecord)

#######################################
# Response Handlers                   #
#######################################

# TODO - Think about how to make this change the possible key handler. Perhaps allow
# only one handler that records responses, while still allowing n number of key handlers
# which can do anything else (like capture scanner TTLs, Escape button)

class ShowViewportResponseHandler(ResponseHandler):

    def __init__(self, experiment, responses, viewportName, viewport=None, createViewport=False):
        ResponseHanlder.__init__(experiment, responses)
        self.viewportName = viewportName

        # add the viewport to the experiment if the flag indicates so
        if createViewport:
            self.experiment.addViewport(viewportName, viewport)

    def handleResponse(self, responses):

         # find out how many responses have been made
         responseCount = len(responses)

         # determine if this handler's viewport should be shown
         showViewport = self.responses.__contains(responseCount)

         # either show or hide it
         self.experiment.showViewport(self.viewportName, showViewport)
         
    
#######################################
# Trial Finished Handlers             #
#######################################

class TTLTrialFinishedHandler(TrialFinishedHandler):

    def __init__(self, experiment, ttlTotal=2):
        Handler.__init__(self, experiment)
        self.ttlTotal = ttlTotal
        self.ttlCount = 0

    def newTrial(self):
        
        # reset the ttl count for the new trial
        self.ttlCount = 0

    def trialFinished(self, elapsedTime, elapsedFrames, events, responses, stimParams):

            # iterate through all events looking for keydown
            for curEvent in events:

                    # if it's a keydown, then pass to key handlers
                    if curEvent.type == pygame.locals.KEYDOWN:

                        if curEvent.key == pygame.locals.K_5:
                            self.ttlCount = self.ttlCount + 1

            # if the number of TTLs to stop the trial has been reached, then return true
            if self.ttlCount >= self.ttlTotal:
                return True
            else:
                return False
        
class TimeTrialFinishedHandler(TrialFinishedHandler):

    def __init__(self, experiment, seconds=None, frames=None):
        Handler.__init__(self, experiment)
        self.seconds = seconds
        self.frames = frames

    def trialFinished(self, elapsedTime, elapsedFrames, events, responses, stimParams):

            # check if this handler is using seconds or frames, then if the
            # amount of time has elapsed indicated for this handler
            if self.frames != None:
                if elapsedFrames > self.frames:
                    return True
                else:
                    return False
            else:
                if elapsedTime > self.seconds:
                    return True
                else:
                    return False
        
class KeyTrialFinishedHandler(TrialFinishedHandler):

    def __init__(self, experiment, key=None):
        Handler.__init__(self, experiment)
        self.targetKey = key

    def trialFinished(self, elapsedTime, elapsedFrames, events, responses, stimParams):

            # iterate through all events looking for keydown
            for curEvent in events:

                    # check it's a keydown
                    if curEvent.type == pygame.locals.KEYDOWN:

                        # if the target key is that pressed then return true
                        if curEvent.key == self.targetKey:
                            return Ture
                        
            # otherwise the target key wasn't pressed, so return false
            return False
        
class ResponseTrialFinishedHandler(TrialFinishedHandler):

    def __init__(self, experiment, count=1):
        Handler.__init__(self, experiment)
        self.count = count

    def trialFinished(self, elapsedTime, elapsedFrames, events, responses, stimParams):

            # if there have been at least the number of responses specified
            # in the constructor, then the trial is finished
            if len(responses) >= self.count:
                return True
            else:
                return False
         
#######################################
# Null Stim  Handlers                 #
#######################################

class BreakNullStimHandler(NullStimHandler):

    def handleNullStim(self, stimParams):

        # show the instructions indicating the user can take a break
	text = 'Break Time\n\nIf you would like to take a break, please do so now. Press "c" when you are ready to continue.'
	self.experiment.showInstructions(text)

        # return true indicating that this Null stim has been handled, and the next
        # stim can be presented
	return True
        
