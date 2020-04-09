import traceback
import Solver.GameSolver as GameSolver
import Solver.Operations as Operations
import os
import Rendering.AudioPlayer as AudioPlayer
import Rendering.ImageDrawer as ImageDrawer
import Rendering.UiManger as UiManger
import Rendering.UiPiece as Piece
import json

class Main:
	Version = "1.1"

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

		self.LevelsData  = {}
		if os.path.isfile(self.LevelDataPath):
			file = open(self.LevelDataPath, "r")
			self.LevelsData = json.load(file)
			file.close()

			if self.DebugMode:
				for levelData in self.LevelsData.items():
					print(levelData)


		self.Level = 0
		self.ClearLevel()
		if os.path.isfile(self.PlayerPrefsPath):
			file = open(self.PlayerPrefsPath, "r")
			playerData = json.load(file)
			file.close()

			if self.DebugMode:
				print(playerData)
			
			if "Version" in playerData and playerData["Version"] == self.Version:
				self.AudioPlayer.Volume = playerData["Volume"]
				if str(playerData["Level"]) in self.LevelsData:
					self.LoadLevelFromData(self.LevelsData[str(playerData["Level"])])
				else:
					self.Level = playerData["Level"]

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
		return self.Manger.Update()

# ui called functions
	def SetSolarCovered(self):
		self.SolarCovered = True
		return
	def GetSolarCovered(self):
		return self.SolarCovered
	def UpdateMovesNum(self, moves):
		self.Moves = int(moves)
		return
	def UpdateGoalNum(self, goal):
		self.Goal = int(goal)
		return
	def UpdateStartingNum(self, startingNum):
		self.StartingNum = int(startingNum)
		return
	def ClickedSolve(self):
		if self.DebugMode:
			print("Sovle Clicked")

		if not self.CheckIsLevelValid():
			if self.DebugMode:
				print("not vaild To Sovle Atm")

			self.AudioPlayer.PlayEvent("CannotDoAction")
			return
		
		found, solveOperationList = GameSolver.Solve(self.Moves, self.OperationsList, self.StartingNum, self.Goal)

		if self.DebugMode:
			print("===================")
			print("")
			print("Found: "+str(found))
			print("")
			print("")

		self.SolveOrder = []
		for loop in range(5):
			self.SolveOrder += [""]

		solveLoop = 0
		for opIndex in solveOperationList:
			solveOp = solveOperationList[solveLoop]

			if self.DebugMode:
				solveOp = self.OperationsList[opIndex]
				print(str(solveLoop) +") "+ solveOp.ToString())

			if len(self.SolveOrder[opIndex]) > 0:
				self.SolveOrder[opIndex] += "," 
			self.SolveOrder[opIndex] += str(solveLoop+1)

			solveLoop += 1

			
		self.SetUpMainScreen()
		return
	def ChangeVolume(self, delta):
		volume = self.AudioPlayer.Volume + delta

		if volume > 10:
			volume = 10
		
		if volume < 0:
			volume = 0

		if volume == self.AudioPlayer.Volume:
			return

		self.AudioPlayer.Volume = volume
		self.SavePlayerPrefs()
		self.SetupSettingsScreen()
		return
	def ChangeLevelSelect(self, delta):
		level = self.Level + delta
		if level < 0:
			level = 0

		self.Level = level

		self.ClearLevel()
		key = str(self.Level)
		if key in self.LevelsData:
			self.LoadLevelFromData(self.LevelsData[key])

		self.SavePlayerPrefs()
		self.SetupSettingsScreen()
		return
	def DebugModeToggle(self):
		self.DebugMode = not self.DebugMode
		self.Manger.DebugMode = self.DebugMode
		self.AudioPlayer.DebugMode = self.DebugMode
		self.SetupSettingsScreen()
		return
	def ClearClicked(self):
		self.Level = 0
		self.ClearLevel()
		self.SavePlayerPrefs()
		self.SetUpMainScreen()
		return
	def SetOperation(self, gridIndex):
		if self.DebugMode:
			print("set SetOperation: ["+str(self.OperationSetUpIndex)+"] to " + str(gridIndex))

		op = Operations.MakeOperation(gridIndex)
		if op == None:
			self.OperationsList[self.OperationSetUpIndex] = Operations.MakeOperation(0)
			self.SetUpMainScreen()

		else:
			self.OperationsList[self.OperationSetUpIndex] = op
			self.SetUpOperationInfoScreen()

		return
	def UpdateSetting1(self, value):
		op = self.OperationsList[self.OperationSetUpIndex]
		op.SetSetting(0, value)
		self.SetUpOperationInfoScreen(clearSelected=False)
		return
	def UpdateSetting2(self, value):
		op = self.OperationsList[self.OperationSetUpIndex]
		op.SetSetting(1, value)
		self.SetUpOperationInfoScreen(clearSelected=False)
		return
	def ClickDoneOpSetup(self):
		op = self.OperationsList[self.OperationSetUpIndex]
		if op.IsValid():
			self.SetUpMainScreen()
		else:
			self.AudioPlayer.PlayEvent("CannotDoAction")
		return
	def SaveLevelData(self):
		if not self.CheckIsLevelValid() or self.Level in self.LevelsData or self.Level == 0:
			if self.DebugMode:
				print("not vaild To Level Data")
			self.AudioPlayer.PlayEvent("CannotDoAction")
			return
		
		self.LevelsData[str(self.Level)] = self.GetlevelDictData()

		if self.DebugMode:
			for levelData in self.LevelsData.items():
				print(levelData)

		
		file = open(self.LevelDataPath, "w")
		json.dump(self.LevelsData, file, indent=4, sort_keys=True)
		file.close()
		return
	def ToggleOpClickAction(self):
		if self.DebugMode:
			print("Toggle Op Click Action")
		self.OpDoesAction = not self.OpDoesAction
		self.SetUpMainScreen()
		return
	def OperationClicked(self, opIndex):
		if self.OpDoesAction:
			op = self.OperationsList[opIndex]
			if type(op) != Operations.Operation and self.Moves > 0:
				self.Moves = self.Moves-1

				self.StartingNum = op.DoActionOnValue(self.StartingNum)
				self.OperationsList = op.DoActionOnOpList(self.OperationsList, self.StartingNum)

				self.SetUpMainScreen()
		else:
			self.SetUpOperationSelectScreen(opIndex)
		return
#Functions used by a few

	def GetlevelDictData(self):
		levelDataDict = {}
		levelDataDict["Level"] = self.Level
		levelDataDict["Moves"] = self.Moves
		levelDataDict["Goal"] = self.Goal
		levelDataDict["StartingNumber"] = self.StartingNum

		operationsData = []
		for op in self.OperationsList:
			operationsData += [op.Serialize()]

		levelDataDict["Operations"] = operationsData
		return levelDataDict

	def LoadLevelFromData(self, data):

		self.Level = data["Level"] 
		self.StartingNum = data["StartingNumber"] 
		self.Goal = data["Goal"] 
		self.Moves = data["Moves"] 

		operationsData = data["Operations"]

		self.OperationsList = []
		for opData in operationsData:
			self.OperationsList += [Operations.OpDeserialization(opData)]

		return

	def ClearLevel(self):
		self.StartingNum = 0
		self.Goal = 0
		self.Moves = 0
		self.OperationsList = []
		self.SolveOrder = []
		for loop in range(5):
			self.OperationsList += [Operations.MakeOperation(0)]
			self.SolveOrder += [""]
		return

	def MakeGridPiece(self, xIndex, yIndex, image=None, yStart=375):
		xStart = 20
		
		boxWidth = 110
		boxHight = 100
		xSpacing = 5
		ySpacing = 10

		x = (boxWidth+xSpacing) * xIndex + xStart
		y = (boxHight+ySpacing) * yIndex + yStart

		return Piece.UiPiece([x, y], [boxWidth, boxHight], image)
	
	def CheckIsLevelValid(self):
		numValidOps = 0
		for op in self.OperationsList:
			if op.IsValid():
				numValidOps += 1
				
		return self.Moves > 0 and self.Goal != self.StartingNum and numValidOps > 0

	def SavePlayerPrefs(self):
		playerData = {}
		playerData["Version"] = self.Version
		playerData["Volume"] = self.AudioPlayer.Volume
		playerData["Level"] = self.Level

		file = open(self.PlayerPrefsPath, "w")
		json.dump(playerData, file, indent=4, sort_keys=True)
		file.close()
		return

#screens 
	def SetupSettingsScreen(self):
		self.SetUpShared(False)

		#volume control row 1
		piece = self.MakeGridPiece(0, 0, image="Button")
		piece.SetUpButton(False, "Button_Hover",
                    "Button_Pressed",
					onClick=self.ChangeVolume, onClickData=-1)
		piece.SetUpLabel("-", "", xLabelAnchor=0.5, yLabelAnchor=0.5)
		piece.SetupAudio("ButtonDown", "ButtonUp")
		self.Manger.AddPiece(piece, False)

		piece = self.MakeGridPiece(1, 0, image="Button_Black")
		piece.SetUpLabel("Volume", "", xLabelAnchor=0.5, yLabelAnchor=0)
		self.Manger.AddPiece(piece, False)

		piece = Piece.UiPiece([133, 395], [113, 80])
		piece.SetUpLabel(str(self.AudioPlayer.Volume), "", xLabelAnchor=0.5, yLabelAnchor=0.5)
		self.Manger.AddPiece(piece, False)

		piece = self.MakeGridPiece(2, 0, image="Button")
		piece.SetUpButton(False, "Button_Hover",
                    "Button_Pressed",
					onClick=self.ChangeVolume, onClickData=1)
		piece.SetUpLabel("+", "", xLabelAnchor=0.5, yLabelAnchor=0.5)
		piece.SetupAudio("ButtonDown", "ButtonUp")
		self.Manger.AddPiece(piece, False)

		#level select row 2
		piece = self.MakeGridPiece(0, 1, image="Button")
		piece.SetUpButton(False, "Button_Hover",
                    "Button_Pressed",
					onClick=self.ChangeLevelSelect, onClickData=-1)
		piece.SetUpLabel("-", "", xLabelAnchor=0.5, yLabelAnchor=0.5)
		piece.SetupAudio("ButtonDown", "ButtonUp")
		self.Manger.AddPiece(piece, False)

		piece = self.MakeGridPiece(1, 1, image="Button_Black")
		piece.SetUpLabel("Level", "", xLabelAnchor=0.5, yLabelAnchor=0)
		self.Manger.AddPiece(piece, False)

		piece = Piece.UiPiece([133, 510], [113, 80])
		piece.SetUpLabel(self.Level, "", xLabelAnchor=0.5, yLabelAnchor=0.5)
		self.Manger.AddPiece(piece, False)

		piece = self.MakeGridPiece(2, 1, image="Button")
		piece.SetUpButton(False, "Button_Hover",
                    "Button_Pressed",
					onClick=self.ChangeLevelSelect, onClickData=1)
		piece.SetUpLabel("+", "", xLabelAnchor=0.5, yLabelAnchor=0.5)
		piece.SetupAudio("ButtonDown", "ButtonUp")
		self.Manger.AddPiece(piece, False)


		#row 3
		piece = self.MakeGridPiece(0, 2, image="Settings_Button")
		piece.SetUpButton(False, "Settings_Hover",
                    "Settings_Pressed",
					onClick=self.SetUpMainScreen)
		piece.SetupAudio("ButtonDown", "ButtonUp")
		self.Manger.AddPiece(piece, False)

		if self.IsDev:
			debugButton = "Button_"
			if self.DebugMode:
				debugButton += "Green"
			else:
				debugButton += "Red"

			piece = self.MakeGridPiece(1, 2, image=debugButton)
			piece.SetUpButton(False,
						onClick=self.DebugModeToggle)
			piece.SetUpLabel("Debug", "", yLabelAnchor=0.5, xLabelAnchor=0.5)
			piece.SetupAudio("ButtonDown", "ButtonUp")
			self.Manger.AddPiece(piece, False)

			piece = self.MakeGridPiece(2, 2, image="Button_Green")
			piece.SetUpButton(False, onClick=self.SaveLevelData)
			piece.SetUpLabel("Save Level", "", yLabelAnchor=0.5, xLabelAnchor=0.5)
			piece.SetupAudio("ButtonDown", "ButtonUp")
			self.Manger.AddPiece(piece, False)
		return

	def SetUpShared(self, selectable=True, clearSelected=True):
		self.Manger.ClearPieceList(clearSelected)

		piece = Piece.UiPiece([0, 0], [378, 704], "BackGround")
		self.Manger.AddPiece(piece, False)

		piece = Piece.UiPiece([55, 35], [145, 30])
		piece.SetUpLabel("LEVEL:", self.Level)
		self.Manger.AddPiece(piece, False)

		piece = Piece.UiPiece([220, 30], [105, 35])
		piece.SetUpButton(True, onClick=self.SetSolarCovered)
		self.Manger.AddPiece(piece, False)

		piece = Piece.UiPiece([40, 90], [90, 50], "FunGuy_Normal")
		piece.SetUpFade(self.GetSolarCovered, "FunGuy_Faded")
		self.Manger.AddPiece(piece, False)

		piece = Piece.UiPiece([140, 90], [90, 50], "TopStats_Normal")
		piece.SetUpFade(self.GetSolarCovered, "TopStats_Faded")
		piece.SetUpLabel("Moves:", self.Moves, textUpdatedFunc=self.UpdateMovesNum)
		self.Manger.AddPiece(piece, selectable)

		piece = Piece.UiPiece([245, 90], [90, 50], "TopStats_Normal")
		piece.SetUpFade(self.GetSolarCovered, "TopStats_Faded")
		piece.SetUpLabel("Goal:", self.Goal, textUpdatedFunc=self.UpdateGoalNum)
		self.Manger.AddPiece(piece, selectable)

		piece = Piece.UiPiece([38 , 180], [302, 75])
		piece.SetUpFade(self.GetSolarCovered)
		piece.SetUpLabel("", self.StartingNum, (0, 0, 0), 1, 0.5, textUpdatedFunc=self.UpdateStartingNum)
		self.Manger.AddPiece(piece, selectable)
		return

	def SetUpMainScreen(self):
		if self.DebugMode:
			print("Setup Main Screen")
		self.SetUpShared()
		#button Grid
		#row 1
		piece = self.MakeGridPiece(0, 0, image="Button")
		piece.SetUpButton(False, "Button_Hover",
                    "Button_Pressed",
					onClick=self.ClickedSolve,
					enterCanClick=True)
		piece.SetupAudio("ButtonDown", "ButtonUp")
		piece.SetUpLabel("Solve", "", yLabelAnchor=0.5)
		self.Manger.AddPiece(piece, True)

		op = self.OperationsList[0]
		piece = self.MakeGridPiece(1, 0, image=op.BaseImage)
		piece.SetUpButton(False, onClick=self.OperationClicked, onClickData=0)
		piece.SetUpLabel(op.ToString(), "", xLabelAnchor=0.5, yLabelAnchor=0.5)
		piece.SetupAudio("ButtonDown", "ButtonUp")
		self.Manger.AddPiece(piece, False)

		piece = Piece.UiPiece([166, 450], [80, 25])
		piece.SetUpLabel(self.SolveOrder[0], "", xLabelAnchor=1, yLabelAnchor=0.5)
		self.Manger.AddPiece(piece, False)

		piece = self.MakeGridPiece(2, 0, image="Button_Red")
		piece.SetUpButton(False, "Button_Red_Hover",
                    "Button_Red_Pressed",
					onClick=self.ClearClicked)
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
			piece.SetUpButton(False,
						onClick=self.ToggleOpClickAction)
			piece.SetupAudio("ButtonDown", "ButtonUp")
			piece.SetUpLabel("Do Action", "", yLabelAnchor=0.5)
			self.Manger.AddPiece(piece, True)

		op = self.OperationsList[1]
		piece = self.MakeGridPiece(1, 1, image=op.BaseImage)
		piece.SetUpButton(False, onClick=self.OperationClicked, onClickData=1)
		piece.SetUpLabel(op.ToString(), "", xLabelAnchor=0.5, yLabelAnchor=0.5)
		piece.SetupAudio("ButtonDown", "ButtonUp")
		self.Manger.AddPiece(piece, False)
		
		piece = Piece.UiPiece([166, 560], [80, 25])
		piece.SetUpLabel(self.SolveOrder[1], "", xLabelAnchor=1, yLabelAnchor=0.5)
		piece.SetupAudio("ButtonDown", "ButtonUp")
		self.Manger.AddPiece(piece, False)

		op = self.OperationsList[2]
		piece = self.MakeGridPiece(2, 1, image=op.BaseImage)
		piece.SetUpButton(False, onClick=self.OperationClicked, onClickData=2)
		piece.SetUpLabel(op.ToString(), "", xLabelAnchor=0.5, yLabelAnchor=0.5)
		piece.SetupAudio("ButtonDown", "ButtonUp")
		self.Manger.AddPiece(piece, False)

		piece = Piece.UiPiece([279, 560], [80, 25])
		piece.SetUpLabel(self.SolveOrder[2], "", xLabelAnchor=1, yLabelAnchor=0.5)
		self.Manger.AddPiece(piece, False)

		#row 3
		piece = self.MakeGridPiece(0, 2, image="Settings_Button")
		piece.SetUpButton(False, "Settings_Hover",
                    "Settings_Pressed",
					onClick=self.SetupSettingsScreen)
		piece.SetupAudio("ButtonDown", "ButtonUp")
		self.Manger.AddPiece(piece, False)

		op = self.OperationsList[3]
		piece = self.MakeGridPiece(1, 2, image=op.BaseImage)
		piece.SetUpButton(False, onClick=self.OperationClicked, onClickData=3)
		piece.SetUpLabel(op.ToString(), "", xLabelAnchor=0.5, yLabelAnchor=0.5)
		piece.SetupAudio("ButtonDown", "ButtonUp")
		self.Manger.AddPiece(piece, False)
		
		piece = Piece.UiPiece([166, 670], [80, 25])
		piece.SetUpLabel(self.SolveOrder[3], "", xLabelAnchor=1, yLabelAnchor=0.5)
		self.Manger.AddPiece(piece, False)

		op = self.OperationsList[4]
		piece = self.MakeGridPiece(2, 2, image=op.BaseImage)
		piece.SetUpButton(False, onClick=self.OperationClicked, onClickData=4)
		piece.SetUpLabel(op.ToString(), "", xLabelAnchor=0.5, yLabelAnchor=0.5)
		piece.SetupAudio("ButtonDown", "ButtonUp")
		self.Manger.AddPiece(piece, False)

		piece = Piece.UiPiece([279, 670], [80, 25])
		piece.SetUpLabel(self.SolveOrder[4], "", xLabelAnchor=1, yLabelAnchor=0.5)
		self.Manger.AddPiece(piece, False)

		return
	
	def SetUpOperationSelectScreen(self, opIndex):
		if self.DebugMode:
			print("Setup Operation Screen index: " + str(opIndex))
		self.OperationSetUpIndex = opIndex
		
		self.SetUpShared(False)

		#button Grid
		yStart = 155
		yNumber = 5

		piece = Piece.UiPiece([10, yStart-10], [360, yNumber*110+10],
			"Popup_BackGround")
		self.Manger.AddPiece(piece, False)

		loop = 1
		for y in range(yNumber):
			for x in range(3):
				
				op = Operations.MakeOperation(loop)
				
				if op != None:
					piece = self.MakeGridPiece(x, y, image=op.BaseImage, yStart=yStart)
					piece.SetUpButton(False, onClick=self.SetOperation, onClickData=loop)
					piece.SetUpLabel(op.ToString(), "", xLabelAnchor=0.5, yLabelAnchor=0.5)
					piece.SetupAudio("ButtonDown", "ButtonUp")
					self.Manger.AddPiece(piece, False)
				else:
					piece = self.MakeGridPiece(x, y, image="Button_Red", yStart=yStart)
					piece.SetUpButton(False, "Button_Red_Hover",
						"Button_Red_Pressed",
						onClick=self.SetOperation, 
						onClickData=loop)
					piece.SetUpLabel("Back", "", xLabelAnchor=0.5, yLabelAnchor=0.5)
					piece.SetupAudio("ButtonDown", "ButtonUp")
					self.Manger.AddPiece(piece, False)
					return


				loop += 1
		return

	def SetUpOperationInfoScreen(self, clearSelected=True):
		if len(self.OperationsList[self.OperationSetUpIndex].Setting) == 0:
			self.SetUpMainScreen()

		else:
			self.SetUpShared(False, clearSelected)

			op = self.OperationsList[self.OperationSetUpIndex]

			#backGround
			piece = Piece.UiPiece([10, 370], [360, 220],
							"Popup_BackGround")
			self.Manger.AddPiece(piece, False)


			#row two
			piece = self.MakeGridPiece(0, 1, image="Button")
			piece.SetUpLabel("", op.GetSetting(0), xLabelAnchor=0.5, yLabelAnchor=0.5, textUpdatedFunc=self.UpdateSetting1)
			piece.SetupAudio("ButtonDown", "ButtonUp")
			self.Manger.AddPiece(piece, True)

			piece = self.MakeGridPiece(1, 1, image=op.BaseImage)
			piece.SetUpLabel(op.ToString(), "", xLabelAnchor=0.5, yLabelAnchor=0.5)
			self.Manger.AddPiece(piece, False)
			
			if len(self.OperationsList[self.OperationSetUpIndex].Setting) == 2:
				piece = self.MakeGridPiece(2, 1, image="Button")
				piece.SetUpLabel("", op.GetSetting(1), xLabelAnchor=0.5, yLabelAnchor=0.5, textUpdatedFunc=self.UpdateSetting2)
				piece.SetupAudio("ButtonDown", "ButtonUp")
				self.Manger.AddPiece(piece, True)


			#finsh button
			piece = self.MakeGridPiece(2, 0, image="Button")
			piece.SetUpButton(False, "Button_Hover",
                    "Button_Pressed",
					onClick=self.ClickDoneOpSetup,
					enterCanClick=True)
			piece.SetUpLabel("Done", "", xLabelAnchor=0.5, yLabelAnchor=0.5)
			piece.SetupAudio("ButtonDown", "ButtonUp")
			self.Manger.AddPiece(piece, True)

			#Back Button
			piece = self.MakeGridPiece(0, 0, image="Button_Red")
			piece.SetUpButton(False, "Button_Red_Hover",
				"Button_Red_Pressed",
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
