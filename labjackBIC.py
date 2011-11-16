# LabJack.py
# Class to interface with our LabJack U6 device which we use to communicate with peripherals in the scanner (currently the Biopac and Eye Tracker). This is a wrapper around the python library that comes from the manufacturer. Below is the information on how the wiring of the cables was done. along with links to find the pin layouts for the various devices.

#1. Cable 1: It should have a DB37 male connector to a DB 37 female connector. The male side connects to the LabJack. Here is a #link to it's pin-layout:
#http://labjack.com/support/u6/users-guide/2.11
#And more info on the specifications of the device's digital IO:
#http://labjack.com/support/u6/users-guide/2.8
#The female side will connect to the Biopac. Here is a page that discusses it's pin layout. Scroll to the bottom and select the #specifications tab and read through the garbage to get to the info:
#http://www.biopac.com/isolated-digital-interface-specifications#LowerTab
#For this cable we'll want the following connections
#Male   ->    Female		LabJack Pin Name
#6              3 			FIO0
#24             4 			FIO1
#5              5 			FIO2
#23             6 			FIO3
#4              7 			FIO4
#22             8 			FIO5
#3              9 			FIO6
#21             10			FIO7
#1              19			GND
#19             21			GND
#
#2. Cable 2: It should be a DB15 male connector to open ended wires on the other side (these we'll connect to that VoltagePro board #on the back of the Eye-Tracker PC with screw terminals). Again, the male side connects to the LabJack, and here's the page to it's #pin layou:
#http://labjack.com/support/u6/users-guide/2.12
#
#Here's a list of the pins I'd like connected, and how to label them (is it possible to put some sort of durable label on the open #ends?)
#
#Male -> Open			LabJack Pin Name
#4         Channel 1			EIO0
#12        Channel 2			EIO1
#5         Channel 3			EIO2
#13        Channel 4			EIO3
#6         Channel 5			EIO4
#14        Channel 6			EIO5
#7         Channel 7			EIO6
#15        Channel 8			EIO7
#8         Ground			GND
#####################################################################################################################################


import u6

#################################################
#		Constants			#
#################################################

# since the scanner's TLL pulses are fed into channel 1 in both the Biopac and the EyeTracker's Voltage Pro board
# I'll call what's really channel 2 on the peripherals channel 1 for the purposes of this class
BIOPAC_CHANNELS = [1,2,3,4,5,6,7]
EYETRACKER_CHANNELS = [9,10,11,12,13,14,15]

BIOPAC_DEVICE_ID = 0
EYETRACKER_DEVICE_ID = 1

DIGITAL_CHANNEL_DIRECTION_OUTPUT = 1
ON_STATE = 1
OFF_STATE = 0

class LabJackBIC:


	def __init__(self):

		# create an instance of the LabJack driver which will do all the communication	
		self.jack = u6.U6()

		# the FIO0-FIO7 inputs are flexible, meaning they can be analog or digital, so ensure
		# they are all digital by sending a zero for the FIO Analog parameter
#		self.jack.configIO(FIOAnalog = 0)

		# now set all the channels to output, since each digital IO channel supports input and output
		for channel in BIOPAC_CHANNELS:
			self.jack.getFeedback(u6.BitDirWrite(channel,DIGITAL_CHANNEL_DIRECTION_OUTPUT))
		for channel in EYETRACKER_CHANNELS:
			self.jack.getFeedback(u6.BitDirWrite(channel,DIGITAL_CHANNEL_DIRECTION_OUTPUT))

	def channelOn(self, device, channelNo):

		# make sure the channelNo is valid
		if channelNo < 0 or channelNo > len(BIOPAC_CHANNELS):
			raise ValueError('Invalid channel number passed to the LabJackBIC channelOn method: $i' %(channelNo))

		# based on which device is being used, determine the channel number to pass to the driver
		channel = None
		if device == BIOPAC_DEVICE_ID:
			channel = BIOPAC_CHANNELS[channelNo]
		elif device == EYETRACKER_DEVICE_ID:
			channel = EYETRACKER_CHANNELS[channelNo]
		else:
			raise ValueError('Invalid Device ID passed to the LabJackBIC channelOn method: %i' %(device))

		# set the given channel to the On state
		self.jack.getFeedback(u6.BitStateWrite(IONumber=channel, State=ON_STATE))

	def channelOff(self, device, channelNo):

		# make sure the channelNo is valid
		if channelNo < 0 or channelNo > len(BIOPAC_CHANNELS):
			raise ValueError('Invalid channel number passed to the LabJackBIC channelOff method: $i' %(channelNo))

		# based on which device is being used, determine the channel number to pass to the driver
		channel = None
		if device == BIOPAC_DEVICE_ID:
			channel = BIOPAC_CHANNELS[channelNo]
		elif device == EYETRACKER_DEVICE_ID:
			channel = EYETRACKER_CHANNELS[channelNo]
		else:
			raise ValueError('Invalid Device ID passed to the LabJackBIC channelOff method: %i' %(device))

		# set the given channel to the On state
		self.jack.getFeedback(u6.BitStateWrite(IONumber=channel, State=OFF_STATE))

	def clearChannels(self, device):


		# based on which device is being used, determine the channel number to pass to the driver
		channels = None
		if device == BIOPAC_DEVICE_ID:
			channels = BIOPAC_CHANNELS
		elif device == EYETRACKER_DEVICE_ID:
			channels = EYETRACKER_CHANNELS
		else:
			raise ValueError('Invalid Device ID passed to the LabJackBIC clearChannels method: %i' %(device))

		# set the given channel to the On state
		for channel in channels:
			self.jack.getFeedback(u6.BitStateWrite(IONumber=channel, State=OFF_STATE))
		
