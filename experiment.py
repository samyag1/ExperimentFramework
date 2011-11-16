# system libraries
import time
import os
import sys
import numpy as np
import pygame
import wave
import csv
import math
import pdb

# vision egg libraries
from VisionEgg import Core
from VisionEgg import Textures
from VisionEgg.Core import *
from VisionEgg.FlowControl import Presentation
from VisionEgg.Text import Text
from VisionEgg.WrappedText import WrappedText
from VisionEgg.ResponseControl import *
from VisionEgg.MoreStimuli import *
from VisionEgg.GUI import *

# local modules
from constants import *
from constantsVAMeasurements import *
import peripheralsManager
import logManager
from experimentHandlers import *

# TODO - Figure out what constants are needed by the stimCreation scripts, then generalize those
# scripts as much as can be done.

# TODO - package up into a python installer - makes subdirectories


class Experiment:

#####################################
#  Constructor	                    #
#####################################

	def __init__(self, screenRefreshRate=60, iti=NO_ITI, preloadImages=False, fixationCross=True):

		self.screen = None
		self.stimOrder = []
		self.stimParams = []
		self.screenWidth = None
		self.screenHeight = None
		self.masterImageFilenames = None
		self.imageDim = 0
		self.preloadImages = preloadImages
		self.visualAngle = VISUAL_ANGLE
		self.logManager = logManager.LogManager()
		self.peripheralsManager = None
		self.lastStimPresented = 0
		self.viewports = {}
		self.showViewports = {}
		self.iti = iti
		self.logData = None
		self.nextStim = None
		self.timeHandlers = []
		self.keyHandlers = []
		self.responseHandlers = []
		self.nullStimHandlers = []
		self.trialFinishedHandler = None
		self.screenRefreshRate = screenRefreshRate # This is in HZ
		self.frameInterval = 1.0 / self.screenRefreshRate
		self.fixationCross = fixationCross
		
	# close the screen when the experiment is closing
	def __del__(self):
		
		# close the screen which exits out of Visual Egg
		if self.screen != None:
			self.screen.close()
			self.screen = None
		
		
#####################################
#  Public Interface	            #
#####################################

	def addTimeHandler(self, handler):
		self.timeHandlers.append(handler)
		
	def addKeyHandler(self, handler):
		self.keyHandlers.append(handler)

	def addResponseHandler(self, handler):
		self.responseHandlers.append(handler)

	def addNullStimHandler(self, handler):
		self.nullStimHandlers.append(handler)

	def setTrialFinishedHandler(self, handler):
		self.trialFinishedHandler = handler


	def showViewport(self, name, show):
		'''
		'''
		
		# error checking
		if not(self.viewports.has_key(name)):
			raise ValueError('Trying to show or hide a viewport that hasn\'t been added to the experiment.')
		
		# if the given viewport is to be shown, then add it to the
		# list of viewports that are to be shown
		if show:
			if not(self.showViewports.has_key(name)):
				self.showViewports[name] = self.viewports[name]
		# otherwise the viewport is to be hidden, so remove it from
		# the list of viewports to be shown
		else:
			if self.showViewports.has_key(name):
				self.showViewports.pop(name)

		# redraw the viewports now that one has changed
		self.drawViewports()

	def getViewport(self, name):
		# error checking
		if not(self.viewports.has_key(name)):
			raise ValueError('Trying to get a viewport that hasn\'t been added to the experiment.')
		return self.viewports[name]

	# TODO - Think about making a factory class to produce the default viewports 
	def addViewport(self, name, viewport=None, show=True):

		if viewport == EMPTY_VIEWPORT:
			newViewport = Viewport(screen=self.screen)
		elif viewport != None:
			newViewport = viewport
		# check for the predefined viewport names, and create 
		# the one specified if it doesn't already exist
		elif viewport == None:

			if name == FIXATION_VIEWPORT:
				# create the fixation viewport
				fixStim = Text(text="+",
					    color=FIXATION_COLOR,
					    position=(self.screenWidth/2,self.screenHeight/2),
					    font_size=50,    
					    anchor='center')
				newViewport = Viewport(screen=self.screen, stimuli=[fixStim])
			# TODO - create an arousal scale (same 1-9 with different labels)
			# TODO - create an approach/avoid scale (with 1-9)
			# TODO - create a general 1-9 viewport with different values for
			# labels at positions Left, Center, Right
			elif name == VALENCE_SCALE_VIEWPORT:
				
				# create the rating scaleviewport
				scaleStim = []
				# TODO - make this a constant
				fontSize = 30
				negStim = Text(text="Negative",
					    color=FIXATION_COLOR,
					    position=(0, self.screenHeight),
					    font_size=fontSize,    
					    anchor='upperleft')
				scaleStim.append(negStim)
				neutText = 'Neutral'
				neutXPos = (self.screenWidth / 2.0)
				#neutXPos = -.5*(len(neutText*fontSize))
				neutStim = Text(text=neutText,
					    color=FIXATION_COLOR,
					    position=(neutXPos,self.screenHeight),
					    font_size=fontSize,    
					    anchor='top')
				scaleStim.append(neutStim)
				posText = 'Positive'
				posStim = Text(text=posText,
					    color=FIXATION_COLOR,
					    position=(self.screenWidth,self.screenHeight),
					    font_size=fontSize,    
					    anchor='upperright')
				scaleStim.append(posStim)

				# TODO = Make this a constant
				possibleRatingCount = 9
				numInterval = (self.screenWidth-fontSize) / (possibleRatingCount-1)
				firstLineY = fontSize + 5
				for num in xrange(0,possibleRatingCount):
					curPos = numInterval*num+ 0.5*fontSize
					posStim = Text(text=str(num+1),
					    color=FIXATION_COLOR,
					    position=(curPos,self.screenHeight-firstLineY),
					    font_size=fontSize,    
					    anchor='top')
					scaleStim.append(posStim)

				newViewport = Viewport(screen=self.screen, stimuli=scaleStim)
			elif name == TEXT_ENTRY_VIEWPORT:

				# create the rating scaleviewport
				textEntry = Text(text="",
					    color=(1,1,1),
					    position=(self.screenWidth/2, 0),
					    font_size=30,    
					    anchor='bottom')

				newViewport = Viewport(screen=self.screen, stimuli=[textEntry])
				
		# if the current viewport is not already in the dictionary of viewports
		# then add it and return true indicating it was added
		if not(self.viewports.has_key(name)):
			self.viewports[name] = newViewport
			if show:
				self.showViewports[name] = newViewport
			return True
		else:
			return False

# NOTE: The below 4 public interface methods should be called in the order they appear here
# although the startPhysio method only need be called if physio logging is desired

	def initVisionEgg(self):
		'''
		'''
		
		# set the resolution and make it full screen
		VisionEgg.config.VISIONEGG_SCREEN_W = 1024	
		VisionEgg.config.VISIONEGG_SCREEN_H = 768
		VisionEgg.config.VISIONEGG_FULLSCREEN = 0# TODO 1

		# figure out the screen size and set the background color to grey
		self.screen = Core.get_default_screen()
		self.screen.parameters.bgcolor = BACKGROUND_COLOR 
		self.screen.clear()
		self.screenWidth, self.screenHeight = self.screen.size

		# add handler to shut the experiment down and
		# log all responses to date when escape is pressed
		# THIS MUST BE ADDED TO ALL EXPERIMENTS TO AVOID POSSIBILITY OF FREEZING YOUR PC
		self.addKeyHandler(EscapeKeyHandler(self))

		# if the user wants to use a fixation cross, then add that here
		if self.fixationCross:
			# add the fixation cross viewport
			self.addViewport(name=FIXATION_VIEWPORT)

	def openLogFile(self, logFilename):

		# use the logManager to open the log file and store the last trial responded to
		self.lastStimPresented = self.logManager.openLogFile(logFilename)

		# create the log data object
		self.logData = logManager.LogData()

	def loadInputFiles(self, stimFilename, imagesFilename, visualAngleFilename):
		'''
		'''
		
		# open the given stim file
		stimPath = os.path.join(STIMULI_PATH, stimFilename)
		stimFile = open( stimPath, 'r')
		csvreader = csv.reader(stimFile)

		# read in the first line of the stim params file
		firstStimLine = csvreader.next()

		# if the symbol indicating that this first line is the list of
		# stim parameter names, then read the file line by line creating
		# the stimOrder list as well as the list of dictionaries which
		# are the stimParams
		if firstStimLine[0] == PARAM_LIST_START_SYMBOL: 
			
			# read in the rest of the file line by line
			for stimLine in csvreader:

				# the first param should always be the stim ID
				# so store it in the stim order list
				self.stimOrder.append(int(stimLine[0]))

				# now go through the rest of the params in the current 
				# line and store them into a dictionary for this stim
				# using the parameter name from the first line as the key
				curStimParams = {}
				for i in xrange(1,len(stimLine)):
					curStimParams[firstStimLine[i]] = stimLine[i]

				# add the populated dictionary to the stimParams list
				self.stimParams.append(curStimParams)
		else:
			for x in firstStimLine: self.stimOrder.append(int(x))

		# get the filenames from the imageNames file
		imagesPath = os.path.join(STIMULI_PATH, imagesFilename)
		f = open(imagesPath, 'r')
		csvreader = csv.reader(f)

		# read in the image filenames
		self.masterImageFilenames = csvreader.next()

		# open the visual measurements file
		visualAnglePath = os.path.join(LOGS_PATH, visualAngleFilename)
		vaFile = open(visualAnglePath, 'r')
		csvreader = csv.reader(vaFile)

		# read in the visual angle measurements
		vaMeasurements = []
		vaRead = csvreader.next()
		for x in vaRead: vaMeasurements.append(float(x))
		vaFile.close()

		# calculate the dimensions of the images based on the measurements
		# read in from the measurements files
		self.imageDim = self.calcImageSize(vaMeasurements)

		# if the images are to be preloaded, then do that now
 		if self.preloadImages:
			self.imagesList = self.preloadImages()
		# otherwise, preload just the first image
		else:
			self.nextStim = self.loadImage(stimID=1)
			
	#show instruction and wait for a key press
	def showInstructions(self, string, wrap=50, responseButtons=[pygame.locals.K_c]):
		'''
		'''

		x = self.screen.size[0]/2
		y = self.screen.size[1]/2
		fSize = 30
		str = string.split("\n")
		if(wrap > 0):
			newStr = []
			for s in str:
				tmp = s
				while(len(tmp) > wrap):
					pivit = tmp[wrap]
					c = 0
					while(pivit != " "):
						pivit = tmp[wrap - c]
						c = c + 1
					newStr.append(tmp[:((wrap - c) + 1)])
					tmp = tmp[((wrap - c) + 1):]
				newStr.append(tmp)
		else:
			newStr = str

		alltStim = []
		for s in range(len(newStr)):
			tStim = Text(text=newStr[s], color=(160.0,160.0,160.0), position=(x,y + ((len(newStr)*fSize)/2 - (s*fSize)/1.5)), font_size = fSize, anchor='center')
			alltStim.append(tStim)
		viewport = Viewport(screen=self.screen, stimuli=alltStim)

		self.screen.clear()
		viewport.draw()
		swap_buffers()

		#wait for response to start 
		subjectPress = False
		while(not(subjectPress)):
			events = pygame.event.get()
			for curEvent in events: 
				if curEvent.type == pygame.locals.KEYDOWN:
					if curEvent.key == pygame.locals.K_ESCAPE:
						self.logManager.cancelLog()
						self.screen.close()
						exit()
					elif (responseButtons.__contains__(curEvent.key)):
						subjectPress = True

	# this method can be used in liue of the previous four methods when a standard
	# initialization of the experiment will happen. This is just for code compactability
	def quickInit(self, logFilename, stimFilename, imagesFilename, visualAngleFilename, instructions):
		self.openLogFile(logFilename)
		self.initVisionEgg()
		self.loadInputFiles(stimFilename, imagesFilename, visualAngleFilename)
		self.showInstructions(instructions)

	def startPhysio(self):
		'''
		Call this to initialize physio data recording
		'''
		# create the Peripherals manager
		self.peripheralsManager = peripheralsManager.PeripheralsManager()

	def waitForScanner(self):
		'''
		'''

		#display a waiting message to the user
		self.screen.clear()
		waitStim = Text(text="waiting for scanner...",
			    color=(1,1,1,1.0),
			    position=(self.screenWidth/2,self.screenHeight/2),
			    font_size=50,    
			    anchor='center')
		waitViewport = Viewport(screen=self.screen, stimuli=[waitStim])

		waitViewport.draw()
		swap_buffers()

		# wait for the scanner's TTL sequence
		lastdummy = self.waitDummies(PRESCAN_DUMMIES)

		# now clear the screen
		self.screen.clear()
		swap_buffers()

	def runExperiment(self):
		'''
		'''
		
		# if signaling physio, indicate the run has started
		if self.peripheralsManager != None:
			# tell the physio system that the run has begun
			self.peripheralsManager.runStart()

		# create the image viewport which will be updated with
		# the ImageTextures created in the imagesList
		stimViewport = Viewport(screen=self.screen)
		self.viewports[STIMULUS_VIEWPORT] = stimViewport
		
		# Loop through all the stimuli in the StimOrder list, where each
		# stimuli is considered one trial. This may start with a stimulus
		# other than the first if the user had selected to continue from
		# a previous log file
		for curTrial in xrange(self.lastStimPresented,len(self.stimOrder)):

			############################
			# Trial Setup		   #

			# tell the handlers that a new trial is starting so they
			# can reset themselves
			self.handlersNewTrial()

			# record the time the trial starts
			trialStartTime = self.getTime()

			# log the start of the trial in the log
			self.logData.trialStartTimes.append(trialStartTime)

			# get the first stimuli and figure out what to do with it
			curStimID = self.stimOrder[curTrial]

			# get the stimParams for the current stim
			curStimParams = self.stimParams[curTrial]

			# make sure the stimlus viewport is shown
			self.showViewports[STIMULUS_VIEWPORT] = stimViewport

			# if it's a null stim then call the Null Stim handler
			if curStimID == NULL_STIM_ID:

				# iterate through all the null handlers
				nextStim = False
				for handler in self.nullStimHandlers:
					result = handler.handleNullStim(curStimParams)

					# the Null Handler returns true if everything that should
					# be done for a NULL stimulus is done in the handler, which
					# means that the loop should move on to the next stimulus 
					if result:
						nextStim = True

				# update the logData indicating it was a NULL trial
				self.logData.stimOnTimes.append(NULL_LOG_ID)
				self.logData.stimOffTimes.append(NULL_LOG_ID)
				self.logData.stimFilenames.append(NULL_FILENAME)
				
				# move on to the next stimlus
				if nextStim:
					# first log the off time of the stim
					self.logData.trialStopTimes.append(self.getTime())
					# create the current trial's response lists,
					# as they are needed for proper logging
					curResponseTimes = []
					curResponseValues = []
					self.logData.responseTimes.append(curResponseTimes)
					self.logData.responseValues.append(curResponseValues)
					continue
				
			# otherwise it's a regular stimuli, so load it into the image viewport
			else:
				# determine the filename of the current stim being presented
				curFilename = self.masterImageFilenames[abs(curStimID)-1]

				# if all the images are preloaded, then get the current stim
				# from the preloaded list
				curStim = None
				if self.preloadImages:
					curStim = self.imagesList[abs(curStimID)-1]
				# otherwise, just get the next stim, which was already preloaded
				else:
					curStim = self.nextStim
					
				# load it in the back buffer so it's ready to load
				stimViewport.parameters.stimuli = [curStim]

				# update the logData
				self.logData.stimOnTimes.append(trialStartTime)
				self.logData.stimFilenames.append(curFilename)
				
			# redraw all the viewports, including the stimulus viewport
			self.redrawViewports()

			##################################    
			# Trial has begun		 #

			# if physio signalling is happening, indicate that the trial has started
			if self.peripheralsManager != None:
				self.peripheralsManager.stimOn()

			# create the current trial's response lists, as more than one response
			# is valid
			curResponseTimes = []
			curResponseValues = []
			self.logData.responseTimes.append(curResponseTimes)
			self.logData.responseValues.append(curResponseValues)

			# Loop until the trial finished handler determines that
			# the trial is over
			trialFinished = False
			stimOff = False
			handlerStartTime = self.getTime()
			while not(trialFinished):		

				# get the current time
				curTime = self.getTime()
				elapsedTime = curTime - handlerStartTime

				# determine the number of frames that have elapsed
				elapsedFrames = int(math.floor(elapsedTime / self.frameInterval))

				# get all the events from the event queue. Could be mouse, keyboard
				events = pygame.event.get()

				# check all handlers for response and needed actions 
				trialFinished = self.checkHandlers(elapsedTime,
								   elapsedFrames,
								   events,
								   curResponseValues,
								   curResponseTimes,
								   curStimParams)


			# in case the stim hasn't been cleared from the screen by a helper
			# do that now, and record the time if it is cleared now
			self.clearStimulus()
				
			# if all images aren't preloaded, then just preload the next one
			# now that the current stim has been displayed, if there is a next one
			nextStim = curTrial + 1
			nextStimLoadTime = 0
			if not(self.preloadImages) and nextStim < len(self.stimOrder):
				nextStimID = self.stimOrder[nextStim]
				preloadTime = self.getTime()
				self.nextStim = self.loadImage(stimID=abs(nextStimID))
				nextStimLoadTime = self.getTime() - preloadTime

			# Now that the trial is finished, wait for the ITI time, if any
			# subtracting the time it took to load the next stimuli (if any)
			if self.iti != NO_ITI:
				time.sleep(self.iti-nextStimLoadTime)

			# increment the trial counter in the log data, so the logger knows
			# how many trials to log (in case the user presses escape
			# in the middle of a trial
			self.logData.trialCount = self.logData.trialCount + 1

			# record the stim the trial has ended
			self.logData.trialStopTimes.append(self.getTime())
			
		########################################
		# Write the Log	and clean up	       #

		# tell the physio system that the run has ended
		if self.peripheralsManager != None:
			self.peripheralsManager.runStop()

		# clear the fixation, make screen blank
		self.screen.clear()
		swap_buffers()

		#log the current block
		self.logManager.logRun(self.logData)

		# tell the LogManager to close the log file
		self.logManager.closeLog()
		
	# waits for n number of dummy scans. used at the beginning of a run 
	def waitDummies(self, dummyCount):
		'''
		'''
		for curDum in xrange(dummyCount):
			self.waitTTL(1)
			self.logManager.writeDummy(curDum+1, self.getTime())

	def stimulusShown(self):
		'''
		'''
		
		# if the stimulus viewport has a stimulus, then return true
		return (self.showViewports.has_key(STIMULUS_VIEWPORT))
		
	def clearStimulus(self):
		'''
		'''
		# see if there is a stimulus present
		stimPresent = self.stimulusShown()

		# clear it if there is one
		if stimPresent:

			# remove the stimulus viewport from the displayed viewports
			stimViewport = self.showViewports.pop(STIMULUS_VIEWPORT)

			# clear out the stimulus from the viewport
			stimViewport.parameters.stimuli = []

			# redraw the viewports, which will effectively
			# remove the stimulus from the screen
			self.redrawViewports()        

			# store the time in the log data
			self.logData.stimOffTimes.append(self.getTime())

			# if physio signalse are being sent, alert it
			if self.peripheralsManager != None:
				self.peripheralsManager.stimOff()

		# return true if a stimulus was cleared
		return stimPresent

#####################################
#  Helper Functions	            #
#####################################
	def checkHandlers(self, elapsedTime, elapsedFrames, events, curResponseValues, curResponseTimes, curStimParams):
	
		#####################################
		# check the time related events first

		# iterate through all the time handlers
		for curHandler in self.timeHandlers:

			# check if the handler's condition has been met
			if curHandler.conditionMet(elapsedTime,
						   elapsedFrames,
						   curStimParams,
						   curResponseValues):

				# tell the current handler to handler the time event
				# it's return value indicates whether it turned
				# off the stimulus
				curHandler.handleTime(elapsedTime, elapsedFrames, curStimParams)

		#######################################
		# check the input related events second


		# iterate through all events looking for keydown
		for curEvent in events:

			# if it's a keydown, then pass to key handlers
			if curEvent.type == pygame.locals.KEYDOWN:

				# iterate through all the key handlers
				for curHandler in self.keyHandlers:

					# check if the current handler's condition is
					# met for handling, then let it handle the key press
					if curHandler.conditionMet(curEvent.key,
								   curEvent.unicode, 
								   curEvent.mod,
								   curStimParams,
								   curResponseValues):

						# handle the key press
						response = curHandler.handleKey(curEvent.key,
										curEvent.unicode,
										curEvent.mod,
										curStimParams)

						# if there is a response to be logged, record it
						if response != None:
							curResponseValues.append(response)
							curResponseTimes.append(self.getTime())

		#####################################
		# check the response related events last

		# iterate through all the time handlers
		for curHandler in self.responseHandlers:

			# tell the current handler to handler the response event
			curHandler.handleResponse(curResponseValues)

		# use the trial finished handler to determine if the end of trial
		# has been reached
		trialFinished = self.trialFinishedHandler.trialFinished(elapsedTime,
									elapsedFrames,
									events,
									curResponseValues,
									curStimParams)
		return trialFinished


	def handlersNewTrial(self):
		'''
		'''

		# iterate through all the time handlers
		for curHandler in self.timeHandlers:

			# tell the current handler a new trial is starting
			# which allows the handlers to reset themselves
			curHandler.newTrial()

		# iterate through all the key handlers
		for curHandler in self.keyHandlers:

			# tell the current handler a new trial is starting
			# which allows the handlers to reset themselves
			curHandler.newTrial()

		# iterate through all the NULL Stim handlers
		for curHandler in self.nullStimHandlers:

			# tell the current handler a new trial is starting
			# which allows the handlers to reset themselves
			curHandler.newTrial()
			
		# tell the trial finished handler a new trial is starting
		# which allows it to reset itself
		self.trialFinishedHandler.newTrial()

	# the time functions return different values on Windows vs Linux/Mac
	# so this function standardizes things
	def getTime(self):
		p = sys.platform
		if(p[0:3] == 'Win'):
			return time.clock()
		else:
			return time.time()

	def waitTTL(self, ttlCount):
		curTTL = 0;
		while(curTTL < ttlCount):
			events = pygame.event.get()
			for curEvent in events: 
				if curEvent.type == pygame.locals.KEYDOWN:
					if curEvent.key == pygame.locals.K_ESCAPE:
						self.logManager.cancelLog()
						if self.peripheralsManager != None:
							# tell the physio system that the run has begun
							self.peripheralsManager.runStop()

						exit()
					elif curEvent.key == pygame.locals.K_5:
						curTTL = curTTL + 1

	def calcImageSize(self, vaMeasurements):

		eyeToMirror = vaMeasurements[EYE_TO_MIRROR_INDEX]
		mirrorToScreen = vaMeasurements[MIRROR_TO_SCREEN_INDEX]
		screenHeightInches = vaMeasurements[SCREEN_HEIGHT_INDEX]

		# do the trig to find half the size the image needs to be
		# in inches for the given visual angle
		adjacent = eyeToMirror+mirrorToScreen
		theta = np.deg2rad(VISUAL_ANGLE/2.0)
		opposite = math.tan(theta)*adjacent

		# twice the opposite side of the triangle calculated
		#above is the size the image should be in inches
		imageDimInches = 2.0* opposite

		# calculate how many pixels per inch the current monitor is displaying
		pixelPerInchRatio = self.screenHeight / screenHeightInches

		# multiple the needed inches in height by the pixel per inch
		# ratio to get the necessary image size in pixels
		imageDimPixels =  int(imageDimInches * pixelPerInchRatio)
		return imageDimPixels

	# preloads the simulus set to save on time during the experiment
	def preloadImages(self):

		# TODO - put handling in to catch exceptions due to too many images
		# to preload, and print out a nice warning, telling them they can't
		# preload
		
		preloadedstimuli = []

		for i in xrange(len(self.masterImageFilenames)):

			# add one since the loadImage method takes the stimID, which is 1 based
			# not 0 based (since 0 is the NULL_STIM_ID)
			stim = loadImage(stimID=(i+1))
			preloadedstimuli.append(stim)
		return preloadedstimuli

	def loadImage(self, stimID=None, filename=None):

		if filename != None:
			curFilename = filename
		else:
			imageFilename = self.masterImageFilenames[stimID-1]
			curFilename = os.path.join(IMAGES_PATH, imageFilename)
		texture = Textures.Texture(curFilename)
		textureSize = (self.imageDim,self.imageDim)

		# TODO - figure out scenario in which I didn't want to use
		# the calculated image dimension, and use the native dimension
		if self.imageDim is None:
			textureSize = texture.size
		stim = Textures.TextureStimulus(texture=texture,
					    size=textureSize,
					    anchor='center',
					    position=(self.screenWidth/2,self.screenHeight/2))
		stim.draw()

		return stim

	def redrawViewports(self):

		# clear the back buffer of all the data in it
		self.screen.clear()

		print self.showViewports.keys()
		# iterate through all the viewports present and draw each on
		for curViewport in self.showViewports.values():
			curViewport.draw()

		# now swap the backbuffer into video memory
		swap_buffers()
		
