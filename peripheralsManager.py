from labjackBIC import *


RUN_CHANNEL = 0
STIM_CHANNEL = 1
BUTTON_CHANNELS = [2,3,4,5]
BUTTON_INDICES = [0,1,2,3]
EYETRACKER_CAL_CHANNEL = 6

#Wrapper class around the LabJackBIC which establishes a mapping between channels and script events such as run on/off, stim on/off and button presses
class PeripheralsManager:

	# TODO - create a GallantLab EyeTracker class and integrate it into
	def __init__(self, enableBioPac=True, enableEyeTracker=True, buttons=BUTTON_INDICES):

		self.buttons = []
		for button in buttons:
			self.buttons.append(BUTTON_CHANNELS[button])

		# create a LabJackBIC to communicate with the Peripherals
		self.labjack = LabJackBIC()

		self.enableBioPac = enableBioPac
		self.enableEyeTracker = enableEyeTracker

		# clear the channels for both the Biopac and EyeTracker
		if self.enableBioPac:
			self.labjack.clearChannels(BIOPAC_DEVICE_ID)
		if self.enableEyeTracker:
			self.labjack.clearChannels(EYETRACKER_DEVICE_ID)

	def runStart(self):

		if self.enableBioPac:
			self.labjack.channelOn(BIOPAC_DEVICE_ID, RUN_CHANNEL)
		if self.enableEyeTracker:
			self.labjack.channelOn(EYETRACKER_DEVICE_ID, RUN_CHANNEL)
	
	def runStop(self):

		if self.enableBioPac:
			self.labjack.channelOff(BIOPAC_DEVICE_ID, RUN_CHANNEL)
		if self.enableEyeTracker:
			self.labjack.channelOff(EYETRACKER_DEVICE_ID, RUN_CHANNEL)

	# TODO - consider adding a trial start and trial stop event too

	def stimOn(self):

		for button in self.buttons:
			if self.enableBioPac:
				self.labjack.channelOff(BIOPAC_DEVICE_ID, button)
			if self.enableEyeTracker:
				self.labjack.channelOff(EYETRACKER_DEVICE_ID, button)
			
		if self.enableBioPac:
			self.labjack.channelOn(BIOPAC_DEVICE_ID, STIM_CHANNEL)
		if self.enableEyeTracker:
			self.labjack.channelOn(EYETRACKER_DEVICE_ID, STIM_CHANNEL)
		
	def stimOff(self):

		if self.enableBioPac:
			self.labjack.channelOff(BIOPAC_DEVICE_ID, STIM_CHANNEL)
		if self.enableEyeTracker:
			self.labjack.channelOff(EYETRACKER_DEVICE_ID, STIM_CHANNEL)

	def buttonPress(self, index):

		if index >= len(self.buttons):
			raise ValueError('Invalid index passed to the buttonPress method of PeripheralsManager: %i' %(index))

		if self.enableBioPac:
			self.labjack.channelOn(BIOPAC_DEVICE_ID, self.buttons[index])
		if self.enableEyeTracker:
			self.labjack.channelOn(EYETRACKER_DEVICE_ID, self.buttons[index])

	def eyeTrackerCalOn(self):

		if self.enableBioPac:
			self.labjack.channelOn(BIOPAC_DEVICE_ID, EYETRACKER_CAL_CHANNEL)
		if self.enableEyeTracker:
			self.labjack.channelOn(EYETRACKER_DEVICE_ID, EYETRACKER_CAL_CHANNEL)

	def eyeTrackerCalOff(self):

		if self.enableBioPac:
			self.labjack.channelOff(BIOPAC_DEVICE_ID, EYETRACKER_CAL_CHANNEL)
		if self.enableEyeTracker:
			self.labjack.channelOff(EYETRACKER_DEVICE_ID, EYETRACKER_CAL_CHANNEL)
	
