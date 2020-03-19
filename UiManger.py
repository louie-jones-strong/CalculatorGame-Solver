from pygame import display, draw, Color, gfxdraw, mouse
import pygame
import os
from enum import Enum
import time
import keyboard
import traceback
import GameSolver
import Operations

class ImageDrawer:
	RawImageCache = {}
	SizedImageCache = {}
	
	def GetSizedImage(self, imageName, size):
		
		sizedKey = imageName + str(size[0])+","+str(size[1])

		if sizedKey not in self.SizedImageCache:

			image = self.GetRawImage(imageName)

			x, y = image.get_size()

			if x != size[0] or y != size[1]:
				image = pygame.transform.scale(image, size)

			self.SizedImageCache[sizedKey] = image
		return self.SizedImageCache[sizedKey]

	def GetRawImage(self, imageName):
		if imageName not in self.RawImageCache:
			path = os.path.join("Images", str(imageName) + ".png")

			if os.path.isfile(path):
				image = pygame.image.load(path)
			else:
				image = pygame.Surface((1, 1))
				image.fill([0,0,0,0])
				image.set_alpha(0)

			self.RawImageCache[imageName] = image

		return self.RawImageCache[imageName]
	
	def DrawImage(self, surface, imageName, pos, size):
		
		if imageName == None:
			return False

		sizedImage = self.GetSizedImage(imageName, size)

		surface.blit(sizedImage, pos)

		return True

class UiPiece:

	class eState(Enum):
		Normal = 0
		Hover = 1
		press = 2
		Fade = 3


	def __init__(self, imageDrawer, pos, size, normalImage=None):
		self.Drawer = imageDrawer
		self.State = UiPiece.eState.Normal
		self.LastState = self.State
		self.BasePos = pos
		self.BaseSize = size
		self.NormalImage = normalImage
		self.HoverImage = None
		self.PressImage = None
		self.OnClick = None
		self.OnClickData = None
		self.FadedImage = None
		self.GetIsFade = None
		self.LastFrameMouseDown = False
		self.ButtonHoldAllowed = False
		self.Label = None
		self.TimeInState = 0
		self.Selected = False
		self.Selectable = False
		self.Colour = (255,255,255)
		self.Message = None
		self.EditableMessage = None
		self.EnterCanClick = False
		return

	def SetUpButton(self, buttonHoldAllowed, hoverImage=None, pressImage=None, onClick=None, onClickData=None, enterCanClick=False):
		self.ButtonHoldAllowed = buttonHoldAllowed
		self.HoverImage = hoverImage
		self.PressImage = pressImage
		self.OnClick = onClick
		self.OnClickData = onClickData
		self.EnterCanClick = enterCanClick
		return

	def SetUpLabel(self, message, editableMessage, colour=(255, 255, 255), xLabelAnchor=0, yLabelAnchor=0, textUpdatedFunc=None):
		self.Message = str(message)
		self.EditableMessage = editableMessage
		self.EditableIsNegtive = False
		self.Colour = colour
		self.XLabelAnchor = xLabelAnchor
		self.YLabelAnchor = yLabelAnchor
		self.TextUpdatedFunc = textUpdatedFunc
		return

	def SetUpFade(self, getIsFade, fadedImage=None):
		self.FadedImage = fadedImage
		self.GetIsFade = getIsFade
		#todo make a fade time
		return
		
	def Update(self, screen, debugMode, deltaTime, scaleFactor):
		self.TimeInState += deltaTime

		self.Pos = [int(self.BasePos[0]*scaleFactor),
				int(self.BasePos[1]*scaleFactor)]
		self.Size = [int(self.BaseSize[0]*scaleFactor),
				int(self.BaseSize[1]*scaleFactor)]

		pos = mouse.get_pos()
		mouseDown = mouse.get_pressed()[0]
		mouseOverButton = (pos[0] > self.Pos[0] and pos[0] < self.Pos[0] + self.Size[0] and
							pos[1] > self.Pos[1] and pos[1] < self.Pos[1] + self.Size[1])

		if (mouseOverButton and 
			((self.LastFrameMouseDown and not mouseDown) or
			(mouseDown and self.ButtonHoldAllowed))):
			self.TriggerOnClick(True)

		if mouseOverButton and mouseDown:
			self.State = UiPiece.eState.press
		
		elif self.GetIsFade != None and self.GetIsFade():
			self.State = UiPiece.eState.Fade

		elif mouseOverButton and not mouseDown:
			self.State = UiPiece.eState.Hover

		else:
			self.State = UiPiece.eState.Normal

		if self.State != self.LastState:
			self.TimeInState = 0

		self.LastState = self.State


		self.LastFrameMouseDown = mouseDown

		self.Draw(screen, debugMode)
		return self.Selectable and self.State == UiPiece.eState.press

	def UpdateLabel(self, events, debugMode):
		if self.Selected and self.EditableMessage != None:
			
			text = "keys Pressed: "
			for event in events:
				if event.type == pygame.KEYDOWN:
					text += str(event.unicode)
					text += ", "

					if event.key == pygame.K_BACKSPACE:
						self.EditableMessage = int(self.EditableMessage/10)

					elif event.unicode == "-":
						self.EditableIsNegtive = not self.EditableIsNegtive

					else:
						try:
							num = int(event.unicode)
							self.EditableMessage *= 10
							self.EditableMessage += int(event.unicode)
						except Exception as e:
							pass
					

					number = self.EditableMessage
					if self.EditableIsNegtive:
						number *= -1
					
					print(number)

					if self.TextUpdatedFunc != None:
						self.TextUpdatedFunc(number)

			if len(text) > len("keys Pressed: ") and debugMode:
				print(text)
		return

	def Draw(self, screen, debugMode):
		if self.State == UiPiece.eState.Normal:
			self.Drawer.DrawImage(screen, self.NormalImage, self.Pos, self.Size)
		
		elif self.State == UiPiece.eState.Hover:
			if not self.Drawer.DrawImage(screen, self.HoverImage, self.Pos, self.Size):
				self.Drawer.DrawImage(screen, self.NormalImage, self.Pos, self.Size)

		elif self.State == UiPiece.eState.press:
			if not self.Drawer.DrawImage(screen, self.PressImage, self.Pos, self.Size):
				self.Drawer.DrawImage(screen, self.NormalImage, self.Pos, self.Size)

		elif self.State == UiPiece.eState.Fade:
			if not self.Drawer.DrawImage(screen, self.FadedImage, self.Pos, self.Size):
				self.Drawer.DrawImage(screen, self.NormalImage, self.Pos, self.Size)

		if self.State != UiPiece.eState.Fade and self.Message != None:
			font = pygame.font.SysFont("monospace", 50)
			text = str(self.Message)
			if self.EditableIsNegtive:
				text = "-"
			
			text += str(self.EditableMessage)

			label = font.render(text, 1, self.Colour)
			
			xRatio = self.Size[0] / label.get_width()
			yRatio = self.Size[1] / label.get_height()

			if xRatio < yRatio:
				ratio = xRatio
			else:
				ratio = yRatio
				
			newSize = [int(label.get_width() * ratio), int(label.get_height() * ratio)]
			label = pygame.transform.scale(label, newSize)

			xOffSet = (self.Size[0] - label.get_width()) * self.XLabelAnchor
			yOffSet = (self.Size[1] - label.get_height()) * self.YLabelAnchor
			pos = [self.Pos[0] + xOffSet, self.Pos[1] + yOffSet]
			screen.blit(label, pos)

		if debugMode:
			rect = [self.Pos[0], self.Pos[1], self.Size[0], self.Size[1]]
			draw.rect(screen, [255, 0, 0], rect, 2)

		if self.Selectable and self.Selected:
			rect = [self.Pos[0], self.Pos[1], self.Size[0], self.Size[1]]
			draw.rect(screen, [255, 255, 255], rect, 2)

		if debugMode:
			font = pygame.font.SysFont("monospace", 10)

			text = self.State.name 
			if self.Selectable:
				text += " " + str(self.Selected)

			label = font.render(text, 1, (255, 0, 0))
			screen.blit(label, [self.Pos[0]+3, self.Pos[1]])
		return

	def SetUpSelect(self):
		self.Selectable = True
		return

	def TriggerOnClick(self, fromMouse):
		if self.EnterCanClick or fromMouse:
			if self.OnClick != None:
				if self.OnClickData == None:
					self.OnClick()
				else:
					self.OnClick(self.OnClickData)
		return

class UiManger:
	PieceList = []
	Selectable = []
	DebugMode = False
	SolarCovered = False
	MouseStartPos = None
	SelectIndex = 0

	def __init__(self):
		self.Running = True

		display.init()
		pygame.font.init()
		pygame.init()
		self.ScaleFactor = 1
		self.Drawer = ImageDrawer()
		pygame.display.set_icon(self.Drawer.GetRawImage("Icon"))
		pygame.display.set_caption("Calculator: The Game")

		self.Resolution = [378, 704]
		#window
		self.Window = display.set_mode(self.Resolution, pygame.RESIZABLE)#todo  add pygame.NOFRAME

		self.ClearClicked()

		self.OperationSetUpIndex = None
		self.LastUpdateTime = time.time()
		return

	def ClearPieceList(self, clearSelected=True):
		self.PieceList = []
		self.Selectable = []
		if clearSelected:
			self.SelectIndex = 0
		return

	def AddPiece(self, piece, selectable):
		if selectable:
			self.Selectable += [len(self.PieceList)]
			piece.SetUpSelect()
		self.PieceList += [piece]
		return

	def Update(self):
		if not self.Running:
			return
		eventList = []
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.Quit()
				return

			elif event.type == pygame.VIDEORESIZE:
				windowSize = [event.w, event.h]
				if windowSize != self.Resolution:
					xRatio = windowSize[0] / self.Resolution[0]
					yRatio = windowSize[1] / self.Resolution[1]

					if xRatio < yRatio:
						ratio = xRatio
					else:
						ratio = yRatio

					self.Resolution = [int(self.Resolution[0] * ratio), int(self.Resolution[1] * ratio)]
					self.ScaleFactor *= ratio
					self.Window = display.set_mode(self.Resolution, pygame.RESIZABLE)

					if self.DebugMode:
						print("reSized to: "+str(self.Resolution))

			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					piece = self.PieceList[self.Selectable[self.SelectIndex]]
					piece.TriggerOnClick(False)

					self.SelectIndex += 1
					if self.SelectIndex >= len(self.Selectable):
						self.SelectIndex = 0

					if self.DebugMode:
						print("Enter pressed index: "+str(self.SelectIndex) + " ->" + str(self.Selectable[self.SelectIndex]))
				else:
					eventList += [event]

			else:
				eventList += [event]

		deltaTime = self.LastUpdateTime - time.time()

		loop = 0
		for piece in self.PieceList:
			if piece.Update(self.Window, self.DebugMode, deltaTime, self.ScaleFactor):
				index = self.Selectable.index(loop)
				if index != self.SelectIndex:
					self.SelectIndex = index
					if self.DebugMode:
						print("piece pressed index: "+str(self.SelectIndex) + " ->" + str(self.Selectable[self.SelectIndex]))

			piece.UpdateLabel(eventList, self.DebugMode)
			loop += 1
		
		if len(self.Selectable) > 0:
			loop = 0
			for piece in self.PieceList:
				piece.Selected = loop == self.Selectable[self.SelectIndex]
				loop += 1

		if self.DebugMode:
			if mouse.get_pressed()[0]:
				if self.MouseStartPos == None:
					self.MouseStartPos = list(mouse.get_pos())
					
				size = [mouse.get_pos()[0]-self.MouseStartPos[0],
						mouse.get_pos()[1]-self.MouseStartPos[1]]
				print("mouse Pos / Size: " + str(self.MouseStartPos) + ", " + str(size))
				
			else:
				self.MouseStartPos = None

			
			

		display.update()

		self.SolarCovered = False
		self.LastUpdateTime = time.time()
		return

	def Quit(self):
		pygame.quit()
		self.Running = False
		return
	
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

		isVaild = self.Moves > 0 and self.Goal != self.StartingNum
		for operation in self.OperationsList:
			if operation != None:
				isVaild = True
				break
		
		if not isVaild:
			if self.DebugMode:
				print("not vaild To Sovle Atm")
			return
		
		found, operationList = GameSolver.Solve(self.Moves, self.OperationsList, self.StartingNum, self.Goal)

		if self.DebugMode:
			print("===================")
			print("")
			print("Found: "+str(found))
			print("")
			print("")

			
			for loop in range(len(operationList)):
				op = operationList[loop]
				print(op.ToString())

				if len(self.SolveOrder[opIndex]) > 0:
					self.SolveOrder[opIndex] += ", "
				self.SolveOrder[opIndex] += str(loop+1)

		return

	def ClearClicked(self):
		self.StartingNum = 0
		self.Goal = 0
		self.Moves = 0
		self.OperationsList = []
		self.SolveOrder = []
		for loop in range(5):
			self.OperationsList += [Operations.MakeOperation(0)]
			self.SolveOrder += [""]

		self.SetUpMainScreen()
		return

	def SetUpShared(self, selectable=True, clearSelected=True):
		self.ClearPieceList(clearSelected)

		piece = UiPiece(self.Drawer, [0, 0], [378, 704], "BackGround")
		self.AddPiece(piece, False)

		piece = UiPiece(self.Drawer, [55, 35], [145, 30])
		piece.SetUpLabel("LEVEL:", 0)
		self.AddPiece(piece, False)

		piece = UiPiece(self.Drawer, [220, 30], [105, 35])
		piece.SetUpButton(True, onClick=self.SetSolarCovered)
		self.AddPiece(piece, False)

		piece = UiPiece(self.Drawer, [40, 90], [90, 50], "FunGuy_Normal")
		piece.SetUpFade(self.GetSolarCovered, "FunGuy_Faded")
		self.AddPiece(piece, False)

		piece = UiPiece(self.Drawer, [140, 90], [90, 50], "TopStats_Normal")
		piece.SetUpFade(self.GetSolarCovered, "TopStats_Faded")
		piece.SetUpLabel("Moves:", self.Moves, textUpdatedFunc=self.UpdateMovesNum)
		self.AddPiece(piece, selectable)

		piece = UiPiece(self.Drawer, [245, 90], [90, 50], "TopStats_Normal")
		piece.SetUpFade(self.GetSolarCovered, "TopStats_Faded")
		piece.SetUpLabel("Goal:", self.Goal, textUpdatedFunc=self.UpdateGoalNum)
		self.AddPiece(piece, selectable)

		piece = UiPiece(self.Drawer, [38 , 180], [302, 75])
		piece.SetUpFade(self.GetSolarCovered)
		piece.SetUpLabel("", self.StartingNum, (0, 0, 0), 1, 0.5, textUpdatedFunc=self.UpdateStartingNum)
		self.AddPiece(piece, selectable)
		return

	def SetUpMainScreen(self):
		print("Setup Main Screen")
		self.SetUpShared()
		#button Grid
		#row 1
		piece = UiPiece(self.Drawer, [20, 375], [113, 100])
		self.AddPiece(piece, False)

		op = self.OperationsList[0]
		piece = UiPiece(self.Drawer, [133, 375], [113, 100], op.BaseImage)
		piece.SetUpButton(False, onClick=self.SetUpOperationSelectScreen, onClickData=0)
		piece.SetUpLabel(op.ToString(), "", xLabelAnchor=0.5, yLabelAnchor=0.5)
		self.AddPiece(piece, False)

		piece = UiPiece(self.Drawer, [133, 375], [50, 35])
		piece.SetUpLabel(self.SolveOrder[0], "", xLabelAnchor=0.5, yLabelAnchor=0.5)
		self.AddPiece(piece, False)

		piece = UiPiece(self.Drawer, [246, 375], [113, 100],
                  "Button_Clear")
		piece.SetUpButton(False, "Button_Clear_Hover",
                    "Button_Clear_Pressed",
					onClick=self.ClearClicked)
		self.AddPiece(piece, False)

		#row 2
		piece = UiPiece(self.Drawer, [20, 485], [113, 100])
		self.AddPiece(piece, False)

		op = self.OperationsList[1]
		piece = UiPiece(self.Drawer, [133, 485], [113, 100], op.BaseImage)
		piece.SetUpButton(False, onClick=self.SetUpOperationSelectScreen, onClickData=1)
		piece.SetUpLabel(op.ToString(), "", xLabelAnchor=0.5, yLabelAnchor=0.5)
		self.AddPiece(piece, False)
		
		piece = UiPiece(self.Drawer, [133, 485], [50, 35])
		piece.SetUpLabel(self.SolveOrder[1], "", xLabelAnchor=0.5, yLabelAnchor=0.5)
		self.AddPiece(piece, False)

		op = self.OperationsList[2]
		piece = UiPiece(self.Drawer, [246, 485], [113, 100], op.BaseImage)
		piece.SetUpButton(False, onClick=self.SetUpOperationSelectScreen, onClickData=2)
		piece.SetUpLabel(op.ToString(), "", xLabelAnchor=0.5, yLabelAnchor=0.5)
		self.AddPiece(piece, False)

		piece = UiPiece(self.Drawer, [246, 485], [50, 35])
		piece.SetUpLabel(self.SolveOrder[2], "", xLabelAnchor=0.5, yLabelAnchor=0.5)
		self.AddPiece(piece, False)

		#row 3
		piece = UiPiece(self.Drawer, [20, 595], [113, 100],
                  "Button")
		piece.SetUpButton(False, "Button_Hover",
                    "Button_Pressed",
					onClick=self.ClickedSolve,
					enterCanClick=True)
		piece.SetUpLabel("Solve!", "", yLabelAnchor=0.5)
		self.AddPiece(piece, True)

		op = self.OperationsList[3]
		piece = UiPiece(self.Drawer, [133, 595], [113, 100], op.BaseImage)
		piece.SetUpButton(False, onClick=self.SetUpOperationSelectScreen, onClickData=3)
		piece.SetUpLabel(op.ToString(), "", xLabelAnchor=0.5, yLabelAnchor=0.5)
		self.AddPiece(piece, False)
		
		piece = UiPiece(self.Drawer, [133, 595], [50, 35])
		piece.SetUpLabel(self.SolveOrder[3], "", xLabelAnchor=0.5, yLabelAnchor=0.5)
		self.AddPiece(piece, False)

		op = self.OperationsList[4]
		piece = UiPiece(self.Drawer, [246, 595], [113, 100], op.BaseImage)
		piece.SetUpButton(False, onClick=self.SetUpOperationSelectScreen, onClickData=4)
		piece.SetUpLabel(op.ToString(), "", xLabelAnchor=0.5, yLabelAnchor=0.5)
		self.AddPiece(piece, False)

		piece = UiPiece(self.Drawer, [246, 595], [50, 35])
		piece.SetUpLabel(self.SolveOrder[4], "", xLabelAnchor=0.5, yLabelAnchor=0.5)
		self.AddPiece(piece, False)

		return
	
	def SetOperation(self, gridIndex):
		print("set SetOperation: ["+str(self.OperationSetUpIndex)+"] to " + str(gridIndex))
		self.OperationsList[self.OperationSetUpIndex] = Operations.MakeOperation(gridIndex)

		self.SetUpOperationInfoScreen()
		return

	def SetUpOperationSelectScreen(self, gridIndex):
		print("Setup Operation Screen index: " + str(gridIndex))
		self.OperationSetUpIndex = gridIndex
		
		self.SetUpShared(False)

		#button Grid
		xStart = 20
		yStart = 265

		piece = UiPiece(self.Drawer, [xStart-10, yStart-10], [360, 450],
			"Popup_BackGround")
		self.AddPiece(piece, False)

		loop = 1
		for y in range(4):
			for x in range(3):
				
				op = Operations.MakeOperation(loop)
				
				if op != None:
					piece = UiPiece(self.Drawer, [xStart+x*115, yStart+y*110], [110, 100],
						op.BaseImage)
					piece.SetUpButton(False, onClick=self.SetOperation, onClickData=loop)
					piece.SetUpLabel(op.ToString(), "", xLabelAnchor=0.5, yLabelAnchor=0.5)
					self.AddPiece(piece, False)


				loop += 1
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

	def SetUpOperationInfoScreen(self, clearSelected=True):
		if self.OperationsList[self.OperationSetUpIndex].NumberOfSetting == 0:
			self.SetUpMainScreen()

		else:
			self.SetUpShared(False, clearSelected)

			op = self.OperationsList[self.OperationSetUpIndex]

			#backGround
			piece = UiPiece(self.Drawer, [10, 370], [360, 220],
							"Popup_BackGround")
			self.AddPiece(piece, False)


			#row two
			piece = UiPiece(self.Drawer, [20, 485], [110, 100],
							"Button")
			piece.SetUpLabel("", op.GetSetting(0), xLabelAnchor=0.5, yLabelAnchor=0.5, textUpdatedFunc=self.UpdateSetting1)
			self.AddPiece(piece, True)

			piece = UiPiece(self.Drawer, [135, 485], [110, 100],
							op.BaseImage)
			piece.SetUpLabel(op.ToString(), "", xLabelAnchor=0.5, yLabelAnchor=0.5)
			self.AddPiece(piece, False)
			
			if self.OperationsList[self.OperationSetUpIndex].NumberOfSetting == 2:
				piece = UiPiece(self.Drawer, [250, 485], [110, 100],
                                    "Button")
				piece.SetUpLabel("", op.GetSetting(1), xLabelAnchor=0.5, yLabelAnchor=0.5, textUpdatedFunc=self.UpdateSetting2)
				self.AddPiece(piece, True)


			#finsh button
			piece = UiPiece(self.Drawer, [250, 380], [110, 100],
							"Button")
			piece.SetUpButton(False, "Button_Hover",
                    "Button_Pressed",
					onClick=self.SetUpMainScreen,
					enterCanClick=True)
			piece.SetUpLabel("Done", "", xLabelAnchor=0.5, yLabelAnchor=0.5)
			self.AddPiece(piece, True)
		return


if __name__ == "__main__":
	try:
		manger = UiManger()
		manger.DebugMode = True
		while manger.Running:
			manger.Update()

	except Exception as e:
		strTrace = traceback.format_exc()
		print(strTrace)
		input("error: "+str(e))
