from pygame import display, draw, Color, gfxdraw, mouse
import pygame
import os
from enum import Enum
import time
import keyboard
import traceback
import GameSolver
import Operations

class UiPiece:#todo make this a sprite to speed it up  

	class eState(Enum):
		Normal = 0
		Hover = 1
		press = 2
		Fade = 3


	def __init__(self, pos, size, normalImage=None):
		self.State = UiPiece.eState.Normal
		self.LastState = self.State
		self.Pos = pos
		self.Size = size
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
		self.SelectedImage = None

		if self.NormalImage != None:
			self.NormalImage = pygame.transform.scale(self.NormalImage, self.Size)
		return

	def SetUpButton(self, buttonHoldAllowed, hoverImage=None, pressImage=None, onClick=None, onClickData=None):
		self.ButtonHoldAllowed = buttonHoldAllowed
		self.HoverImage = hoverImage
		self.PressImage = pressImage
		self.OnClick = onClick
		self.OnClickData = onClickData

		if self.HoverImage != None:
			self.HoverImage = pygame.transform.scale(self.HoverImage, self.Size)
		if self.PressImage != None:
			self.PressImage = pygame.transform.scale(self.PressImage, self.Size)
		return

	def SetUpLabel(self, message, editableMessage, colour=(255, 255, 255), xLabelAnchor=0, yLabelAnchor=0, textUpdatedFunc=None):
		self.Message = str(message)
		self.EditableMessage = str(editableMessage)
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
		if self.FadedImage != None:
			self.FadedImage = pygame.transform.scale(self.FadedImage, self.Size)
		return
		
	def Update(self, screen, debugMode, deltaTime):
		self.TimeInState += deltaTime

		pos = mouse.get_pos()
		mouseDown = mouse.get_pressed()[0]
		mouseOverButton = (pos[0] > self.Pos[0] and pos[0] < self.Pos[0] + self.Size[0] and
							pos[1] > self.Pos[1] and pos[1] < self.Pos[1] + self.Size[1])

		if (mouseOverButton and 
			((self.LastFrameMouseDown and not mouseDown) or
			(mouseDown and self.ButtonHoldAllowed))):
			if self.OnClick != None:
				if self.OnClickData == None:
					self.OnClick()
				else:
					self.OnClick(self.OnClickData)

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
						self.EditableMessage = self.EditableMessage[:-1]

					elif event.unicode == "-":
						self.EditableIsNegtive = not self.EditableIsNegtive

					else:
						self.EditableMessage += event.unicode
					
					if self.EditableIsNegtive:
						print("-"+self.EditableMessage)
					else:
						print(self.EditableMessage)

					if self.TextUpdatedFunc != None:
						self.TextUpdatedFunc(self.EditableMessage)

			if len(text) > len("keys Pressed: ") and debugMode:
				print(text)
		return

	def Draw(self, screen, debugMode):
		if self.State == UiPiece.eState.Normal:
			if self.NormalImage != None:
				screen.blit(self.NormalImage, self.Pos)
		
		elif self.State == UiPiece.eState.Hover:
			if self.HoverImage != None:
				screen.blit(self.HoverImage, self.Pos)
			elif self.NormalImage != None:
				screen.blit(self.NormalImage, self.Pos)

		elif self.State == UiPiece.eState.press:
			if self.PressImage != None:
				screen.blit(self.PressImage, self.Pos)
			elif self.NormalImage != None:
				screen.blit(self.NormalImage, self.Pos)

		elif self.State == UiPiece.eState.Fade:
			if self.FadedImage != None:
				screen.blit(self.FadedImage, self.Pos)
			elif self.NormalImage != None:
				screen.blit(self.NormalImage, self.Pos)

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

		if self.Selectable and self.Selected:
			if self.SelectedImage != None:
				screen.blit(self.SelectedImage, self.Pos)


		if debugMode:
			rect = [self.Pos[0], self.Pos[1], self.Size[0], self.Size[1]]
			draw.rect(screen, [255, 0, 0], rect, 2)

			font = pygame.font.SysFont("monospace", 10)

			text = self.State.name 
			if self.Selectable:
				text += " " + str(self.Selected)

			label = font.render(text, 1, (255, 0, 0))
			screen.blit(label, [self.Pos[0]+3, self.Pos[1]])
		return

	def SetUpSelect(self, selectedImage=None):
		self.Selectable = True
		self.SelectedImage = selectedImage

		if self.SelectedImage != None:
			self.SelectedImage = pygame.transform.scale(self.SelectedImage, self.Size)
		return

class UiManger:
	ImageCache = {}
	PieceList = []
	Selectable = []
	DebugMode = False
	SolarCovered = False
	MouseStartPos = None
	SelectIndex = 0

	def LoadImage(self, imageName, scaleFactor=1):
		if imageName not in self.ImageCache:
			path = os.path.join("Images", str(imageName)+".png")

			if os.path.isfile(path):
				self.ImageCache[imageName] = pygame.image.load(path)
			else:
				self.ImageCache[imageName] = pygame.Surface((1, 1))
				self.ImageCache[imageName].fill([0,0,0,0])
				self.ImageCache[imageName].set_alpha(0)

		image = self.ImageCache[imageName]
		if scaleFactor != 1:
			x, y = image.get_size()
			x = int(x*scaleFactor)
			y = int(y*scaleFactor)
			image = pygame.transform.scale(image, (x, y))

		return image

	def __init__(self):
		self.Running = True
		self.LastEnterDown = False
		display.init()
		pygame.font.init()
		pygame.init()
		self.StartingNum = 0
		self.Goal = 0
		self.Moves = 0

		self.BackGround = self.LoadImage("BackGround", 0.35)
		self.Resolution = self.BackGround.get_size()

		#window
		self.Window = display.set_mode(self.Resolution)

		self.OperationsList = []
		self.OperationsList += [Operations.MakeOperation(0)]
		self.OperationsList += [Operations.MakeOperation(0)]
		self.OperationsList += [Operations.MakeOperation(0)]
		self.OperationsList += [Operations.MakeOperation(0)]
		self.OperationsList += [Operations.MakeOperation(0)]
		self.OperationSetUpIndex = None
		self.LastUpdateTime = time.time()
		return

	def ClearPieceList(self):
		self.PieceList = []
		self.Selectable = []
		self.SelectIndex = 0
		return

	def AddPiece(self, piece, selectable):
		if selectable:
			self.Selectable += [len(self.PieceList)]
			piece.SetUpSelect(self.LoadImage("Button_Selected"))
		self.PieceList += [piece]
		return

	def Update(self):
		if not self.Running:
			return

		eventList =[]
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.Quit()
				return
			
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
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

		self.Window.blit(self.BackGround, [0, 0])

		self.LastEnterDown = keyboard.is_pressed("enter")

		loop = 0
		for piece in self.PieceList:
			if piece.Update(self.Window, self.DebugMode, deltaTime):
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

			for operation in operationList:
				print(operation.ToString())
		return

	def SetUpShared(self):
		self.ClearPieceList()

		piece = UiPiece([55, 35], [145, 30])
		piece.SetUpLabel("LEVEL:", 0)
		self.AddPiece(piece, False)

		piece = UiPiece([220, 30], [105, 35])
		piece.SetUpButton(True, onClick=self.SetSolarCovered)
		self.AddPiece(piece, False)

		piece = UiPiece([40, 90], [90, 50], manger.LoadImage("FunGuy_Normal"))
		piece.SetUpFade(self.GetSolarCovered, manger.LoadImage("FunGuy_Faded"))
		self.AddPiece(piece, False)

		piece = UiPiece([140, 90], [90, 50], manger.LoadImage("TopStats_Normal"))
		piece.SetUpFade(self.GetSolarCovered, manger.LoadImage("TopStats_Faded"))
		piece.SetUpLabel("Moves:", self.Moves, textUpdatedFunc=self.UpdateMovesNum)
		self.AddPiece(piece, True)

		piece = UiPiece([245, 90], [90, 50], manger.LoadImage("TopStats_Normal"))
		piece.SetUpFade(self.GetSolarCovered, manger.LoadImage("TopStats_Faded"))
		piece.SetUpLabel("Goal:", self.Goal, textUpdatedFunc=self.UpdateGoalNum)
		self.AddPiece(piece, True)

		piece = UiPiece([38 , 180], [302, 75])
		piece.SetUpFade(self.GetSolarCovered)
		piece.SetUpLabel("", self.StartingNum, (0, 0, 0), 1, 0.5, textUpdatedFunc=self.UpdateStartingNum)
		self.AddPiece(piece, True)
		return

	def SetUpMainScreen(self):
		print("Setup Main Screen")
		self.SetUpShared()
		#button Grid
		#row 1
		piece = UiPiece([20, 375], [113, 100])
		self.AddPiece(piece, False)

		op = self.OperationsList[0]
		piece = UiPiece([133, 375], [113, 100], manger.LoadImage(op.BaseImage))
		piece.SetUpButton(False, onClick=self.SetUpOperationSelectScreen, onClickData=0)
		piece.SetUpLabel(op.ToString(), "", xLabelAnchor=0.5, yLabelAnchor=0.5)
		self.AddPiece(piece, False)

		piece = UiPiece([246, 375], [113, 100])
		self.AddPiece(piece, False)

		#row 2
		piece = UiPiece([20, 485], [113, 100])
		self.AddPiece(piece, False)

		op = self.OperationsList[1]
		piece = UiPiece([133, 485], [113, 100], manger.LoadImage(op.BaseImage))
		piece.SetUpButton(False, onClick=self.SetUpOperationSelectScreen, onClickData=1)
		piece.SetUpLabel(op.ToString(), "", xLabelAnchor=0.5, yLabelAnchor=0.5)
		self.AddPiece(piece, False)

		op = self.OperationsList[2]
		piece = UiPiece([246, 485], [113, 100], manger.LoadImage(op.BaseImage))
		piece.SetUpButton(False, onClick=self.SetUpOperationSelectScreen, onClickData=2)
		piece.SetUpLabel(op.ToString(), "", xLabelAnchor=0.5, yLabelAnchor=0.5)
		self.AddPiece(piece, False)

		#row 3
		piece = UiPiece([20, 595], [113, 100],
                  manger.LoadImage("Button"))
		piece.SetUpButton(False, manger.LoadImage("Button_Hover"),
                    manger.LoadImage("Button_Pressed"),
					onClick=self.ClickedSolve)
		piece.SetUpLabel("Solve!", "", yLabelAnchor=0.5)
		self.AddPiece(piece, True)

		op = self.OperationsList[3]
		piece = UiPiece([133, 595], [113, 100], manger.LoadImage(op.BaseImage))
		piece.SetUpButton(False, onClick=self.SetUpOperationSelectScreen, onClickData=3)
		piece.SetUpLabel(op.ToString(), "", xLabelAnchor=0.5, yLabelAnchor=0.5)
		self.AddPiece(piece, False)

		op = self.OperationsList[4]
		piece = UiPiece([246, 595], [113, 100], manger.LoadImage(op.BaseImage))
		piece.SetUpButton(False, onClick=self.SetUpOperationSelectScreen, onClickData=4)
		piece.SetUpLabel(op.ToString(), "", xLabelAnchor=0.5, yLabelAnchor=0.5)
		self.AddPiece(piece, False)

		return
	
	def SetOperation(self, gridIndex):
		print("set SetOperation: ["+str(self.OperationSetUpIndex)+"] to " + str(gridIndex))
		self.OperationsList[self.OperationSetUpIndex] = Operations.MakeOperation(gridIndex)

		self.SetUpMainScreen()
		return

	def SetUpOperationSelectScreen(self, gridIndex):
		print("Setup Operation Screen index: " + str(gridIndex))
		self.OperationSetUpIndex = gridIndex
		
		self.SetUpShared()

		#button Grid
		xStart = 20
		yStart = 265

		piece = UiPiece([xStart-10, yStart-10], [360, 450],
			manger.LoadImage("Popup_BackGround"))
		self.AddPiece(piece, False)

		loop = 1
		for y in range(4):
			for x in range(3):
				
				op = Operations.MakeOperation(loop)
				
				if op != None:
					piece = UiPiece([xStart+x*115, yStart+y*110], [110, 100],
						manger.LoadImage(op.BaseImage))
					piece.SetUpButton(False, onClick=self.SetOperation, onClickData=loop)
					piece.SetUpLabel(op.ToString(), "", xLabelAnchor=0.5, yLabelAnchor=0.5)
					self.AddPiece(piece, False)


				loop += 1
		return


if __name__ == "__main__":
	try:
		manger = UiManger()
		manger.DebugMode = True
		manger.SetUpMainScreen()
		while manger.Running:
			manger.Update()

	except Exception as e:
		strTrace = traceback.format_exc()
		print(strTrace)
		input("error: "+str(e))
