from pygame import mixer
import random
import os

class AudioPlayer:
	
	def __init__(self, audioAssetFolder, debugMode):
		self.AudioAssetFolder = audioAssetFolder
		mixer.init()
		self.AudioCache = {}
		self.MultiEventDict = {}
		self.Volume = 10
		self.DebugMode = debugMode
		return

	def PlayEvent(self, eventName):
		if eventName == None:
			return

		if eventName in self.MultiEventDict:
			subEventList = self.MultiEventDict[eventName]
			index = random.randint(0, len(subEventList)-1)
			eventName = subEventList[index]

		if eventName not in self.AudioCache:
			path = os.path.join("Assets", "Audio", str(eventName) + ".wav")
			audioEvent = mixer.Sound(path)
			self.AudioCache[eventName] = audioEvent

		audioEvent = self.AudioCache[eventName]

		if self.DebugMode:
			print("Play audio Event: "+str(eventName))
		audioEvent.set_volume(self.Volume/10)
		audioEvent.play()
		return

	def SetupMultiEvent(self, eventName, subEventNames):

		eventList = []
		for subEventName in subEventNames:
			path = os.path.join("Assets", "Audio", str(subEventName) + ".wav")
			audioEvent = mixer.Sound(path)

			if audioEvent != None:
				eventList += [subEventName]

		if len(eventList) > 0:
			self.MultiEventDict[eventName] = eventList
		return
