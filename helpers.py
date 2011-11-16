
#####################################
#  Define functions	            #
#####################################

def readAvailAudio( stream, buffer, chunk ):

#TODO - bug here
	readableFrames = stream.get_read_available()
	chunkCount = readableFrames / chunk
	chunkRemainder = readableFrames % chunk
	print readableFrames
	for curChunk in xrange(chunkCount):
		curAudioChunk = stream.read(chunk)
		buffer.append(curAudioChunk)
	curAudioChunk = stream.read(chunkRemainder)
	buffer.append(curAudioChunk)
	


def writeAudioFile(audioData, audioFilename, audioStream, highLatencyChunk, audio):

	# close out the audio stream
	readAvailAudio(audioStream, audioData, highLatencyChunk)
	remainingAudio = audioStream.get_read_available()
	remainingData = audioStream.read(remainingAudio)
	audioData.append(remainingData)
	audioStream.close()

	# close the audio object
	audio.terminate()

	# open the wav file
	audioFilePath = os.path.join(LOGS_PATH, audioFilename)
	audioOutputFile = wave.open(audioFilePath, 'wb')

	# set the audio parameters into the file metadata
	audioOutputFile.setnchannels(AUDIO_CHANNELS)
	audioOutputFile.setsampwidth(audio.get_sample_size(AUDIO_FORMAT))
	audioOutputFile.setframerate(AUDIO_RATE)

	# write out the data in string form to the file
	audioFileData = ''.join(audioData)
	audioOutputFile.writeframes(audioFileData)

	# close the wav file
	audioOutputFile.close()




def showExampleImage(valence, imageIndex, screen, imagesList):

	# create the image viewport which will be updated with the ImageTextures created in the imagesList
	imageViewport = ve.Core.Viewport(screen=screen,)

	# create the fixation viewport
	screenWidth, screenHeight = screen.size
	fixStim = Text(text="+",
		    color=FIXATION_COLOR,
		    position=(screenWidth/2,screenHeight/2),
		    font_size=50,    
		    anchor='center')
	fixViewport = Viewport (screen=screen, stimuli=[fixStim])

	# show the image and fixation viewports
	screen.clear()
	imageViewport.parameters.stimuli = [imagesList[imageIndex]]
	imageViewport.draw()
	fixViewport.draw()

	# display the new image, which indicates the start of the trial
	ve.Core.swap_buffers()

	# wait for the user to respond to the image
	buttonPressed = -1
	while buttonPressed == -1:		

		# get all the events from the pygame event queue and iterate through all of them looking for keydown
		events = pygame.event.get()
		for curEvent in events: 
			if curEvent.type == pygame.locals.KEYDOWN:
				# if the operator has pressed escape, then just exit the run writing to the log
				if curEvent.key == pygame.locals.K_ESCAPE:
					screen.close()
					exit()

				# the user has pressed one of the input buttons, so store it for logging purposes
				elif (curEvent.key == pygame.locals.K_1): 
					buttonPressed = 1
				elif (curEvent.key == pygame.locals.K_2):
					buttonPressed = 2
				elif (curEvent.key == pygame.locals.K_3):
					buttonPressed = 3
#				elif (curEvent.key == pygame.locals.K_4):
#					buttonPressed = 4
				

	valencePressed = None
	if buttonPressed == 1:
		valencePressed = NEGATIVE
	elif buttonPressed == 2:
		valencePressed = NEUTRAL
	elif buttonPressed == 3:
		valencePressed = POSITIVE

	responseText = ''
	if valencePressed == valence:
		responseText = 'Correct. Most people agree that the image you previously viewed is %s.' % (valence)
	else:
		responseText = 'You choose %s, is that what you meant to choose? Most poeple think the image previously viewed is %s.' % (valencePressed, valence)

	# show the response text as an instruction, using the default 'c' key (controlled by the operator)
	# as the key to move on
	showInstruct(responseText,50,screen)

