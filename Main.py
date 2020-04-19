import traceback
import Solver.GameSolver as GameSolver
import Solver.Operations as Operations
import Solver.LevelData as LevelData
import os
import Rendering.SharedRendering.AudioPlayer as AudioPlayer
import Rendering.SharedRendering.ImageDrawer as ImageDrawer
import Rendering.SharedRendering.UiManger as UiManger
import Rendering.SharedRendering.UiPiece as Piece
import Rendering.UiSegmentDisplay as UiSegmentDisplay
import json
from enum import Enum

class Main:
	Version = "1.1"

	class eScreen(Enum):
		Main = 0
		PickOp = 1
		EditOp = 2
		Setting = 3

	def __init__(self):
		path = "Assets"
		dataPath = os.path.join(path, "Data")
		if not os.path.exists(dataPath):
			os.makedirs(dataPath)

		self.LevelDataPath = os.path.join(dataPath, "LevelData.json")
		self.PlayerPrefsPath = os.path.join(dataPath, "PlayerPrefs.json")
		self.DebugMode = False
		self.IsDev = False

		self.AudioPlayer = AudioPlayer.AudioPlayer(os.path.join(path, "Audio"), self.DebugMode)
		self.AudioPlayer.SetupMultiEvent("ButtonDown", ["ButtonDown1", "ButtonDown2"])
		self.AudioPlayer.SetupMultiEvent("ButtonUp", ["ButtonUp1", "ButtonUp2"])

		drawer = ImageDrawer.ImageDrawer(os.path.join(path, "Images"))


		self.Manger = UiManger.UiManger(self.AudioPlayer, drawer, "Calculator: The Game", "Icon")
		self.Manger.DebugMode = self.DebugMode
		self.SegmentDisplay = None

		self.Solver =  GameSolver.GameSolver()

		self.Level = 0
		self.ClearLevel()

		self.LevelsData  = {}
		if os.path.isfile(self.LevelDataPath):
			file = open(self.LevelDataPath, "r")
			dataDict = json.load(file)
			file.close()

			anyNeededMigration = False
			for key, value in dataDict.items():

				levelData = LevelData.LevelData()

				if levelData.Deserialize(value):
					anyNeededMigration = True

				self.LevelsData[key] = levelData

			if anyNeededMigration:
				self.SaveAllLevelData()

		if os.path.isfile(self.PlayerPrefsPath):
			file = open(self.PlayerPrefsPath, "r")
			playerData = json.load(file)
			file.close()

			if self.DebugMode:
				print(playerData)
			
			if "Version" in playerData and playerData["Version"] == self.Version:
				self.AudioPlayer.Volume = playerData["Volume"]
				self.Level = playerData["Level"]

				if str(self.Level) in self.LevelsData:
					self.CurretLevelData = self.LevelsData[str(self.Level)]

				if "IsDev" in playerData:
					self.IsDev = playerData["IsDev"]

		self.AudioPlayer.PlayEvent("Intro")
		self.OperationSetUpIndex = None
		self.SolarCovered = False
		self.OpDoesAction = False
		self.SetUpMainScreen()
		return

	def Update(self):
		self.SolarCovered = False
		
		if self.SegmentDisplay != None:
			self.SegmentDisplay.Update(self.CurretLevelData)

		return self.Manger.Update()

# ui called functions
	def SetSolarCovered(self):
		self.SolarCovered = True
		return
	def GetIsFaded(self):
		return self.SolarCovered
	def UpdateMovesNum(self, moves):
		self.CurretLevelData.Moves = int(moves)
		return
	def UpdateGoalNum(self, goal):
		self.CurretLevelData.Goal = int(goal)
		return
	def UpdateStartingNum(self, startingNum):
		self.CurretLevelData.StartingNum = int(startingNum)
		return
	def ClickedSolve(self):
		if self.DebugMode:
			print("Sovle Clicked")

		if not self.CurretLevelData.IsValid():
			if self.DebugMode:
				print("not vaild To Sovle Atm")

			self.AudioPlayer.PlayEvent("CannotDoAction")
			return
		
		found, solveOperationList = self.Solver.Solve(self.CurretLevelData)

		self.SolveOrder = []
		for loop in range(5):
			self.SolveOrder += [""]

		solveLoop = 0
		for opIndex in solveOperationList:
			solveOp = solveOperationList[solveLoop]

			if self.DebugMode:
				solveOp = self.CurretLevelData.OpList[opIndex]
				print(str(solveLoop) +") "+ str(solveOp))

			if len(self.SolveOrder[opIndex]) > 0:
				self.SolveOrder[opIndex] += "," 
			self.SolveOrder[opIndex] += str(solveLoop+1)

			solveLoop += 1

			
		self.SetUpMainScreen()
		return
	def ChangeVolume(self, delta):
		volume = self.AudioPlayer.Volume + delta

		if volume > self.AudioPlayer.MaxVolume:
			volume = self.AudioPlayer.MaxVolume
		
		if volume < 0:
			volume = 0

		if volume == self.AudioPlayer.Volume:
			return

		self.AudioPlayer.Volume = volume
		self.SavePlayerPrefs()
		return
	def GetVolume(self):
		return self.AudioPlayer.Volume
	def ChangeLevelSelect(self, delta):
		level = self.Level + delta

		if level < 0 or level > len(self.LevelsData)+1:
			return

		self.Level = level

		self.ClearLevel()
		key = str(self.Level)
		if key in self.LevelsData:
			self.CurretLevelData = self.LevelsData[key]

		self.SavePlayerPrefs()
		return
	def GetLevel(self):
		return self.Level
	def DebugModeToggle(self):
		self.DebugMode = not self.DebugMode
		self.Manger.DebugMode = self.DebugMode
		self.AudioPlayer.DebugMode = self.DebugMode
		self.SetupSettingsScreen()
		return
	def ClearClicked(self):
		self.ClearLevel()

		if self.Level < len(self.LevelsData)+1:

			if self.OpDoesAction:
				key = str(self.Level)
				if key in self.LevelsData:
					self.CurretLevelData = self.LevelsData[key]

			else:
				self.ClearLevel()
				self.SavePlayerPrefs()

		self.SetUpMainScreen()
		return
	def SetOperation(self, gridIndex):
		if self.DebugMode:
			print("set SetOperation: ["+str(self.OperationSetUpIndex)+"] to " + str(gridIndex))

		op = Operations.MakeOperation(gridIndex)
		if op == None:
			self.CurretLevelData.OpList[self.OperationSetUpIndex] = Operations.MakeOperation(0)
			self.SetUpMainScreen()

		else:
			self.CurretLevelData.OpList[self.OperationSetUpIndex] = op
			self.SetUpOperationInfoScreen()

		return
	def UpdateSetting1(self, value):
		op = self.CurretLevelData.OpList[self.OperationSetUpIndex]
		op.SetSetting(0, value)
		return
	def UpdateSetting2(self, value):
		op = self.CurretLevelData.OpList[self.OperationSetUpIndex]
		op.SetSetting(1, value)
		return
	def ClickDoneOpSetup(self):
		op = self.CurretLevelData.OpList[self.OperationSetUpIndex]
		if op.IsValid():
			self.SetUpMainScreen()
		else:
			self.AudioPlayer.PlayEvent("CannotDoAction")
		return
	def SaveLevelData(self):
		if not self.CurretLevelData.IsValid() or self.Level in self.LevelsData or self.Level == 0:
			if self.DebugMode:
				print("not vaild To Level Data")
			self.AudioPlayer.PlayEvent("CannotDoAction")
			return
		
		self.CurretLevelData.Level = self.Level
		self.LevelsData[str(self.Level)] = self.CurretLevelData

		if self.DebugMode:
			for levelData in self.LevelsData.items():
				print(levelData)

		self.SaveAllLevelData()
		return
	def ToggleOpClickAction(self):
		if self.DebugMode:
			print("Toggle Op Click Action")
		self.OpDoesAction = not self.OpDoesAction
		self.SetUpMainScreen()
		return
	def OperationClicked(self, opIndex):

		if self.OpDoesAction:
			if self.DebugMode:
				print("OperationClicked")
			op = self.CurretLevelData.OpList[opIndex]
			if type(op) != Operations.Operation and self.CurretLevelData.Moves > 0:
				self.CurretLevelData.Moves = self.CurretLevelData.Moves-1

				if issubclass(type(op), Operations.ValueChangeOp):
					self.CurretLevelData.StartingNum = op.DoActionOnValue(self.CurretLevelData.StartingNum)

				elif issubclass(type(op), Operations.OpListChangeOp):
					self.CurretLevelData.OpList = op.DoActionOnOpList(self.CurretLevelData.OpList, self.CurretLevelData.StartingNum)

				self.SetUpMainScreen()
		else:
			self.SetUpOperationSelectScreen(opIndex)
		return
	def OperationHold(self, opIndex):
		if self.OpDoesAction:
			if self.DebugMode:
				print("OperationHold")

			op = self.CurretLevelData.OpList[opIndex]
			if type(op) == Operations.Store and self.CurretLevelData.Moves > 0:
				self.CurretLevelData.Moves = self.CurretLevelData.Moves-1

				if issubclass(type(op), Operations.OpListChangeOp):
					self.CurretLevelData.OpList = op.DoActionOnOpList(self.CurretLevelData.OpList, self.CurretLevelData.StartingNum)

				self.SetUpMainScreen()
		else:
			self.SetUpOperationSelectScreen(opIndex)
		return
	def SetFromPortal(self, index):
		
		if index != self.CurretLevelData.PortalFrom:
			self.CurretLevelData.PortalFrom = index

		else:
			self.CurretLevelData.PortalFrom = None

		return
	def SetToPortal(self, index):

		if index != self.CurretLevelData.PortalTo:
			self.CurretLevelData.PortalTo = index

		else:
			self.CurretLevelData.PortalTo = None

		return

#Functions used by a few
	def ClearLevel(self):
		self.CurretLevelData = LevelData.LevelData()
		self.CurretLevelData.Level = self.Level
		self.SolveOrder = []
		for loop in range(5):
			self.SolveOrder += [""]
		return

	def MakeGridPiece(self, xIndex, yIndex, image=None, hoverImage=None, yStart=375):
		xStart = 20
		
		boxWidth = 110
		boxHight = 100
		xSpacing = 5
		ySpacing = 10

		x = (boxWidth+xSpacing) * xIndex + xStart
		y = (boxHight+ySpacing) * yIndex + yStart

		return Piece.UiPiece([x, y], [boxWidth, boxHight], normalImage=image, hoverImage=hoverImage)

	def SavePlayerPrefs(self):
		playerData = {}
		playerData["Version"] = self.Version
		playerData["Volume"] = self.AudioPlayer.Volume
		playerData["Level"] = self.Level
		if self.IsDev:
			playerData["IsDev"] = True

		file = open(self.PlayerPrefsPath, "w")
		json.dump(playerData, file, indent=4, sort_keys=True)
		file.close()
		return
	def SaveAllLevelData(self):
		dataDict = {}
		for key, value in self.LevelsData.items():
			dataDict[key] = value.Serialize()

		file = open(self.LevelDataPath, "w")
		json.dump(dataDict, file, indent=4, sort_keys=True)
		file.close()
		return

#screens
	def SetupSettingsScreen(self):
		self.ScreenState = Main.eScreen.Setting

		self.SetUpShared(False, showPaused=True)
		minHoldTime = 0.5
		timeBetweenHold = 0.075

		#volume control row 1
		piece = self.MakeGridPiece(0, 0, image="Button", hoverImage="Button_Hover")
		piece.SetUpButtonClick("Button_Pressed", onClick=self.ChangeVolume, onClickData=-1)
		piece.SetUpButtonHold("Button_Pressed", onHold=self.ChangeVolume, 
			onHoldData=-1, minHoldTime=minHoldTime, maxTimeBetweenHold=timeBetweenHold)
		piece.SetUpLabel("-", "", xLabelAnchor=0.5, yLabelAnchor=0.5)
		piece.SetupAudio("ButtonDown", "ButtonUp")
		self.Manger.AddPiece(piece, False)

		piece = self.MakeGridPiece(1, 0, image="Button_Black")
		piece.SetUpLabel("Volume", "", xLabelAnchor=0.5, yLabelAnchor=0)
		self.Manger.AddPiece(piece, False)

		piece = Piece.UiPiece([133, 395], [113, 80])
		piece.SetUpLabel(str(self.AudioPlayer.Volume), "", xLabelAnchor=0.5, yLabelAnchor=0.5, getMessage=self.GetVolume)
		self.Manger.AddPiece(piece, False)

		piece = self.MakeGridPiece(2, 0, image="Button", hoverImage="Button_Hover")
		piece.SetUpButtonClick("Button_Pressed", onClick=self.ChangeVolume, onClickData=1)
		piece.SetUpButtonHold("Button_Pressed", onHold=self.ChangeVolume, 
			onHoldData=1, minHoldTime=minHoldTime, maxTimeBetweenHold=timeBetweenHold)
		piece.SetUpLabel("+", "", xLabelAnchor=0.5, yLabelAnchor=0.5)
		piece.SetupAudio("ButtonDown", "ButtonUp")
		self.Manger.AddPiece(piece, False)

		#level select row 2
		piece = self.MakeGridPiece(0, 1, image="Button", hoverImage="Button_Hover")
		piece.SetUpButtonClick("Button_Pressed", onClick=self.ChangeLevelSelect, onClickData=-1)
		piece.SetUpButtonHold("Button_Pressed", onHold=self.ChangeLevelSelect, 
			onHoldData=-1, minHoldTime=minHoldTime, maxTimeBetweenHold=timeBetweenHold)
		piece.SetUpLabel("-", "", xLabelAnchor=0.5, yLabelAnchor=0.5)
		piece.SetupAudio("ButtonDown", "ButtonUp")
		self.Manger.AddPiece(piece, False)

		piece = self.MakeGridPiece(1, 1, image="Button_Black")
		piece.SetUpLabel("Level", "", xLabelAnchor=0.5, yLabelAnchor=0)
		self.Manger.AddPiece(piece, False)

		piece = Piece.UiPiece([133, 510], [113, 80])
		piece.SetUpLabel(self.Level, "", xLabelAnchor=0.5, yLabelAnchor=0.5, getMessage=self.GetLevel)
		self.Manger.AddPiece(piece, False)

		piece = self.MakeGridPiece(2, 1, image="Button", hoverImage="Button_Hover")
		piece.SetUpButtonClick("Button_Pressed", onClick=self.ChangeLevelSelect, onClickData=1)
		piece.SetUpButtonHold("Button_Pressed", onHold=self.ChangeLevelSelect, 
			onHoldData=1, minHoldTime=minHoldTime, maxTimeBetweenHold=timeBetweenHold)
		piece.SetUpLabel("+", "", xLabelAnchor=0.5, yLabelAnchor=0.5)
		piece.SetupAudio("ButtonDown", "ButtonUp")
		self.Manger.AddPiece(piece, False)


		#row 3
		piece = self.MakeGridPiece(0, 2, image="Settings_Button", hoverImage="Settings_Hover")
		piece.SetUpButtonClick("Settings_Pressed", onClick=self.SetUpMainScreen)
		piece.SetupAudio("ButtonDown", "ButtonUp")
		self.Manger.AddPiece(piece, False)

		if self.IsDev:
			debugButton = "Button_"
			if self.DebugMode:
				debugButton += "Green"
			else:
				debugButton += "Red"

			piece = self.MakeGridPiece(1, 2, image=debugButton)
			piece.SetUpButtonClick(onClick=self.DebugModeToggle)
			piece.SetUpLabel("Debug", "", yLabelAnchor=0.5, xLabelAnchor=0.5)
			piece.SetupAudio("ButtonDown", "ButtonUp")
			self.Manger.AddPiece(piece, False)

			piece = self.MakeGridPiece(2, 2, image="Button_Green")
			piece.SetUpButtonClick(onClick=self.SaveLevelData)
			piece.SetUpLabel("Save Level", "", yLabelAnchor=0.5, xLabelAnchor=0.5)
			piece.SetupAudio("ButtonDown", "ButtonUp")
			self.Manger.AddPiece(piece, False)
		return

	def SetUpShared(self, selectable=True, clearSelected=True, showPaused=False):
		self.Manger.ClearPieceList(clearSelected)

		piece = Piece.UiPiece([0, 0], [378, 704], "BackGround")
		self.Manger.AddPiece(piece, False)

		piece = Piece.UiPiece([55, 35], [145, 30])
		piece.SetUpLabel("LEVEL:", self.Level)
		self.Manger.AddPiece(piece, False)

		piece = Piece.UiPiece([0, 0], [145, 15])
		piece.SetUpLabel("V"+str(self.Version) + ","+str(self.CurretLevelData.Version), "", labelColour=[0,0,0])
		self.Manger.AddPiece(piece, False)

		piece = Piece.UiPiece([220, 30], [105, 35])
		piece.SetUpButtonHold(onHold=self.SetSolarCovered, minHoldTime=0, maxTimeBetweenHold=0)
		self.Manger.AddPiece(piece, False)

		if showPaused:
			piece = Piece.UiPiece([40, 90], [90, 50], "FunGuy_Faded")
			self.Manger.AddPiece(piece, False)

			piece = Piece.UiPiece([140, 90], [90, 50], "TopStats_Faded")
			self.Manger.AddPiece(piece, selectable)

			piece = Piece.UiPiece([245, 90], [90, 50], "TopStats_Faded")
			self.Manger.AddPiece(piece, selectable)
		else:
			piece = Piece.UiPiece([40, 90], [90, 50], "FunGuy_Normal")
			piece.SetUpFade(self.GetIsFaded, "FunGuy_Faded")
			self.Manger.AddPiece(piece, False)

			piece = Piece.UiPiece([140, 90], [90, 50], "TopStats_Normal")
			piece.SetUpFade(self.GetIsFaded, "TopStats_Faded")
			piece.SetUpLabel("Moves:", self.CurretLevelData.Moves, textUpdatedFunc=self.UpdateMovesNum)
			self.Manger.AddPiece(piece, selectable)

			piece = Piece.UiPiece([245, 90], [90, 50], "TopStats_Normal")
			piece.SetUpFade(self.GetIsFaded, "TopStats_Faded")
			piece.SetUpLabel("Goal:", self.CurretLevelData.Goal, textUpdatedFunc=self.UpdateGoalNum)
			self.Manger.AddPiece(piece, selectable)

		piece = Piece.UiPiece([38 , 180], [302, 75])
		piece.SetUpFade(self.GetIsFaded)

		if showPaused:
			piece.SetUpLabel("PAUSED", "", (0, 0, 0), 0.5, 0.5)

		else:
			piece.SetUpLabel("", self.CurretLevelData.StartingNum, (0, 0, 0), 1, 0.5, textUpdatedFunc=self.UpdateStartingNum, hideLabel=True)
			
		self.Manger.AddPiece(piece, selectable)

		if not showPaused:
			self.SegmentDisplay = UiSegmentDisplay.UiSegmentDisplay(self.Manger, 
				GameSolver.MaxCharacters, [45 , 180], [295, 75], self.SetFromPortal, self.SetToPortal, self.GetIsFaded)


		return

	def SetUpMainScreen(self):
		self.ScreenState = Main.eScreen.Main

		if self.DebugMode:
			print("Setup Main Screen")
		self.SetUpShared()
		#button Grid
		#row 1
		piece = self.MakeGridPiece(0, 0, image="Button", hoverImage="Button_Hover")
		piece.SetUpButtonClick("Button_Pressed", onClick=self.ClickedSolve, enterCanClick=True)
		piece.SetupAudio("ButtonDown", "ButtonUp")
		piece.SetUpLabel("Solve", "", yLabelAnchor=0.5)
		self.Manger.AddPiece(piece, True)

		op = self.CurretLevelData.OpList[0]
		piece = self.MakeGridPiece(1, 0, image=op.BaseImage)
		piece.SetUpButtonClick(onClick=self.OperationClicked, onClickData=0)
		piece.SetUpButtonHold(onHold=self.OperationHold, onHoldData=0)
		piece.SetUpLabel(str(op), "", xLabelAnchor=0.5, yLabelAnchor=0.5)
		piece.SetupAudio("ButtonDown", "ButtonUp")
		self.Manger.AddPiece(piece, False)

		piece = Piece.UiPiece([166, 450], [80, 25])
		piece.SetUpLabel(self.SolveOrder[0], "", xLabelAnchor=1, yLabelAnchor=0.5)
		self.Manger.AddPiece(piece, False)

		piece = self.MakeGridPiece(2, 0, image="Button_Red", hoverImage="Button_Red_Hover")
		piece.SetUpButtonClick("Button_Red_Pressed", onClick=self.ClearClicked)
		piece.SetUpLabel("Clear", "", xLabelAnchor=0.5, yLabelAnchor=0.5)
		piece.SetupAudio("ButtonDown", "ButtonUp")
		self.Manger.AddPiece(piece, False)

		#row 2

		if self.IsDev:
			toggleButton = "Button_"
			if self.OpDoesAction:
				toggleButton += "Green"
			else:
				toggleButton += "Red"
			piece = self.MakeGridPiece(0, 1, image=toggleButton)
			piece.SetUpButtonClick(onClick=self.ToggleOpClickAction)
			piece.SetupAudio("ButtonDown", "ButtonUp")
			piece.SetUpLabel("Do Action", "", yLabelAnchor=0.5)
			self.Manger.AddPiece(piece, False)

		op = self.CurretLevelData.OpList[1]
		piece = self.MakeGridPiece(1, 1, image=op.BaseImage)
		piece.SetUpButtonClick(onClick=self.OperationClicked, onClickData=1)
		piece.SetUpButtonHold(onHold=self.OperationHold, onHoldData=1)
		piece.SetUpLabel(str(op), "", xLabelAnchor=0.5, yLabelAnchor=0.5)
		piece.SetupAudio("ButtonDown", "ButtonUp")
		self.Manger.AddPiece(piece, False)
		
		piece = Piece.UiPiece([166, 560], [80, 25])
		piece.SetUpLabel(self.SolveOrder[1], "", xLabelAnchor=1, yLabelAnchor=0.5)
		piece.SetupAudio("ButtonDown", "ButtonUp")
		self.Manger.AddPiece(piece, False)

		op = self.CurretLevelData.OpList[2]
		piece = self.MakeGridPiece(2, 1, image=op.BaseImage)
		piece.SetUpButtonClick(onClick=self.OperationClicked, onClickData=2)
		piece.SetUpButtonHold(onHold=self.OperationHold, onHoldData=2)
		piece.SetUpLabel(str(op), "", xLabelAnchor=0.5, yLabelAnchor=0.5)
		piece.SetupAudio("ButtonDown", "ButtonUp")
		self.Manger.AddPiece(piece, False)

		piece = Piece.UiPiece([279, 560], [80, 25])
		piece.SetUpLabel(self.SolveOrder[2], "", xLabelAnchor=1, yLabelAnchor=0.5)
		self.Manger.AddPiece(piece, False)

		#row 3
		piece = self.MakeGridPiece(0, 2, image="Settings_Button", hoverImage="Settings_Hover")
		piece.SetUpButtonClick("Settings_Pressed", onClick=self.SetupSettingsScreen)
		piece.SetupAudio("ButtonDown", "ButtonUp")
		self.Manger.AddPiece(piece, False)

		op = self.CurretLevelData.OpList[3]
		piece = self.MakeGridPiece(1, 2, image=op.BaseImage)
		piece.SetUpButtonClick(onClick=self.OperationClicked, onClickData=3)
		piece.SetUpButtonHold(onHold=self.OperationHold, onHoldData=3)
		piece.SetUpLabel(str(op), "", xLabelAnchor=0.5, yLabelAnchor=0.5)
		piece.SetupAudio("ButtonDown", "ButtonUp")
		self.Manger.AddPiece(piece, False)
		
		piece = Piece.UiPiece([166, 670], [80, 25])
		piece.SetUpLabel(self.SolveOrder[3], "", xLabelAnchor=1, yLabelAnchor=0.5)
		self.Manger.AddPiece(piece, False)

		op = self.CurretLevelData.OpList[4]
		piece = self.MakeGridPiece(2, 2, image=op.BaseImage)
		piece.SetUpButtonClick(onClick=self.OperationClicked, onClickData=4)
		piece.SetUpButtonHold(onHold=self.OperationHold, onHoldData=4)
		piece.SetUpLabel(str(op), "", xLabelAnchor=0.5, yLabelAnchor=0.5)
		piece.SetupAudio("ButtonDown", "ButtonUp")
		self.Manger.AddPiece(piece, False)

		piece = Piece.UiPiece([279, 670], [80, 25])
		piece.SetUpLabel(self.SolveOrder[4], "", xLabelAnchor=1, yLabelAnchor=0.5)
		self.Manger.AddPiece(piece, False)

		return
	
	def SetUpOperationSelectScreen(self, opIndex):
		self.ScreenState = Main.eScreen.PickOp

		if self.DebugMode:
			print("Setup Operation Screen index: " + str(opIndex))
		self.OperationSetUpIndex = opIndex
		
		self.SetUpShared(False)

		#button Grid
		yStart = 45
		yNumber = 6

		piece = Piece.UiPiece([10, yStart-10], [360, yNumber*110+10],
			"Popup_BackGround")
		self.Manger.AddPiece(piece, False)

		loop = 1
		for y in range(yNumber):
			for x in range(3):
				
				op = Operations.MakeOperation(loop)
				
				if op != None:
					piece = self.MakeGridPiece(x, y, image=op.BaseImage, yStart=yStart)
					piece.SetUpButtonClick(onClick=self.SetOperation, onClickData=loop)
					piece.SetUpLabel(str(op), "", xLabelAnchor=0.5, yLabelAnchor=0.5)
					piece.SetupAudio("ButtonDown", "ButtonUp")
					self.Manger.AddPiece(piece, False)
				else:
					piece = self.MakeGridPiece(x, y, image="Button_Red", hoverImage="Button_Red_Hover", yStart=yStart)
					piece.SetUpButtonClick("Button_Red_Pressed", onClick=self.SetOperation, onClickData=loop)
					piece.SetUpLabel("Back", "", xLabelAnchor=0.5, yLabelAnchor=0.5)
					piece.SetupAudio("ButtonDown", "ButtonUp")
					self.Manger.AddPiece(piece, False)
					return


				loop += 1
		return

	def SetUpOperationInfoScreen(self, clearSelected=True):
		self.ScreenState = Main.eScreen.EditOp
		op = self.CurretLevelData.OpList[self.OperationSetUpIndex]

		settingToEdit = []
		for index in range(len(op.Setting)):
			setting = op.Setting[index]

			if not setting.IsTempValue:
				settingToEdit += [index]

		if len(settingToEdit) == 0:
			self.SetUpMainScreen()

		else:
			self.SetUpShared(False, clearSelected)

			#backGround
			piece = Piece.UiPiece([10, 370], [360, 220],
							"Popup_BackGround")
			self.Manger.AddPiece(piece, False)


			#row two
			piece = self.MakeGridPiece(0, 1, image="Button")
			piece.SetUpLabel("", op.GetSetting(settingToEdit[0]), xLabelAnchor=0.5, yLabelAnchor=0.5, textUpdatedFunc=self.UpdateSetting1)
			piece.SetupAudio("ButtonDown", "ButtonUp")
			self.Manger.AddPiece(piece, True)

			piece = self.MakeGridPiece(1, 1, image=op.BaseImage)
			piece.SetUpLabel(str(op), "", xLabelAnchor=0.5, yLabelAnchor=0.5, getMessage=op.__str__)
			self.Manger.AddPiece(piece, False)
			
			if len(settingToEdit) == 2:
				piece = self.MakeGridPiece(2, 1, image="Button")
				piece.SetUpLabel("", op.GetSetting(settingToEdit[1]), xLabelAnchor=0.5, yLabelAnchor=0.5, textUpdatedFunc=self.UpdateSetting2)
				piece.SetupAudio("ButtonDown", "ButtonUp")
				self.Manger.AddPiece(piece, True)


			#finsh button
			piece = self.MakeGridPiece(2, 0, image="Button", hoverImage="Button_Hover")
			piece.SetUpButtonClick("Button_Pressed",
					onClick=self.ClickDoneOpSetup,
					enterCanClick=True)
			piece.SetUpLabel("Done", "", xLabelAnchor=0.5, yLabelAnchor=0.5)
			piece.SetupAudio("ButtonDown", "ButtonUp")
			self.Manger.AddPiece(piece, True)

			#Back Button
			piece = self.MakeGridPiece(0, 0, image="Button_Red", hoverImage="Button_Red_Hover")
			piece.SetUpButtonClick("Button_Red_Pressed",
				onClick=self.SetUpOperationSelectScreen,
				onClickData=self.OperationSetUpIndex)
			piece.SetUpLabel("Back", "", xLabelAnchor=0.5, yLabelAnchor=0.5)
			piece.SetupAudio("ButtonDown", "ButtonUp")
			self.Manger.AddPiece(piece, False)
		return


if __name__ == "__main__":
	try:
		manger = Main()

		running = True
		while running:
			running = manger.Update()

	except Exception as e:
		strTrace = traceback.format_exc()
		print(strTrace)
