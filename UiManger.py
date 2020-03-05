from pygame import display, draw, Color, gfxdraw, mouse
import pygame
import os
from enum import Enum
import time

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

	def SetUpLabel(self, message, colour=(255, 255, 255)):
		font = pygame.font.SysFont("monospace", 50)
		self.Label = font.render(str(message), 1, colour)
		self.Label = pygame.transform.scale(self.Label, self.Size)
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

		if self.State != UiPiece.eState.Fade and self.Label != None:
			screen.blit(self.Label, self.Pos)


		if debugMode:
			rect = [self.Pos[0], self.Pos[1], self.Size[0], self.Size[1]]
			draw.rect(screen, [255, 0, 0], rect, 2)

			font = pygame.font.SysFont("monospace", 15)
			label = font.render(self.State.name, 1, (255, 0, 0))
			screen.blit(label, [self.Pos[0]+3, self.Pos[1]])
		return

class UiManger:
	ImageCache = {}
	PieceList = []
	DebugMode = False
	SolarCovered = False
	MouseStartPos = None

	def LoadImage(self, imageName, scaleFactor=1):
		if imageName not in self.ImageCache:
			path = os.path.join("Images", str(imageName)+".png")
			self.ImageCache[imageName] = pygame.image.load(path)

		image = self.ImageCache[imageName]
		if scaleFactor != 1:
			x, y = image.get_size()
			x = int(x*scaleFactor)
			y = int(y*scaleFactor)
			image = pygame.transform.scale(image, (x, y))

		return image

	def __init__(self):
		self.Running = True
		display.init()
		pygame.font.init()

		self.BackGround = self.LoadImage("BackGround", 0.35)
		self.Resolution = self.BackGround.get_size()

		#window
		self.Window = display.set_mode(self.Resolution)

		self.OperationsList = [None, None, None, None, None]
		self.OperationSetUpIndex = None
		self.LastUpdateTime = time.time()
		return

	def Update(self):
		if not self.Running:
			return

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.Quit()
				return

		deltaTime = self.LastUpdateTime - time.time()

		self.Window.blit(self.BackGround, [0, 0])

		for button in self.PieceList:
			button.Update(self.Window, self.DebugMode, deltaTime)
		
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

	def SetUpShared(self):
		manger.PieceList = []

		piece = UiPiece([220, 30], [105, 35])
		piece.SetUpButton(True, onClick=self.SetSolarCovered)
		manger.PieceList += [piece]

		piece = UiPiece([40, 90], [90, 50], manger.LoadImage("FunGuy_Normal"))
		piece.SetUpFade(self.GetSolarCovered, manger.LoadImage("FunGuy_Faded"))
		manger.PieceList += [piece]

		piece = UiPiece([140, 90], [90, 50], manger.LoadImage("TopStats_Normal"))
		piece.SetUpFade(self.GetSolarCovered, manger.LoadImage("TopStats_Faded"))
		piece.SetUpLabel("Moves:")
		manger.PieceList += [piece]

		piece = UiPiece([245, 90], [90, 50], manger.LoadImage("TopStats_Normal"))
		piece.SetUpFade(self.GetSolarCovered, manger.LoadImage("TopStats_Faded"))
		piece.SetUpLabel("Goal:")
		manger.PieceList += [piece]

		piece = UiPiece([50, 180], [270, 55])
		piece.SetUpFade(self.GetSolarCovered)
		piece.SetUpLabel("888888", (0, 0, 0))
		manger.PieceList += [piece]
		return

	def SetUpMainScreen(self):
		print("Setup Main Screen")
		self.SetUpShared()
		#button Grid
		#row 1
		piece = UiPiece([20, 375], [113, 100])
		manger.PieceList += [piece]

		piece = UiPiece([133, 375], [113, 100])
		piece.SetUpButton(False, onClick=self.SetUpOperationSelectScreen, onClickData=0)
		piece.SetUpLabel(self.OperationsList[0])
		manger.PieceList += [piece]

		piece = UiPiece([246, 375], [113, 100])
		manger.PieceList += [piece]

		#row 2
		piece = UiPiece([20, 485], [113, 100])
		manger.PieceList += [piece]

		piece = UiPiece([133, 485], [113, 100])
		piece.SetUpButton(False, onClick=self.SetUpOperationSelectScreen, onClickData=1)
		piece.SetUpLabel(self.OperationsList[1])
		manger.PieceList += [piece]

		piece = UiPiece([246, 485], [113, 100])
		piece.SetUpButton(False, onClick=self.SetUpOperationSelectScreen, onClickData=2)
		piece.SetUpLabel(self.OperationsList[2])
		manger.PieceList += [piece]

		#row 3
		piece = UiPiece([20, 595], [113, 100],
                  manger.LoadImage("Button"))
		piece.SetUpButton(False, manger.LoadImage("Button_Hover"),
                    manger.LoadImage("Button_Pressed"))
		piece.SetUpLabel("Solve!")
		manger.PieceList += [piece]

		piece = UiPiece([133, 595], [113, 100])
		piece.SetUpButton(False, onClick=self.SetUpOperationSelectScreen, onClickData=3)
		piece.SetUpLabel(self.OperationsList[3])
		manger.PieceList += [piece]

		piece = UiPiece([246, 595], [113, 100])
		piece.SetUpButton(False, onClick=self.SetUpOperationSelectScreen, onClickData=4)
		piece.SetUpLabel(self.OperationsList[4])
		manger.PieceList += [piece]

		return
	
	def SetOperation(self, gridIndex):
		print("set SetOperation: ["+str(self.OperationSetUpIndex)+"] to " + str(gridIndex))
		self.OperationsList[self.OperationSetUpIndex] = gridIndex

		self.SetUpMainScreen()
		return

	def SetUpOperationSelectScreen(self, gridIndex):
		print("Setup Operation Screen index: " + str(gridIndex))
		self.OperationSetUpIndex = gridIndex
		
		self.SetUpShared()

		#button Grid
		loop = 0
		for y in range(3):
			for x in range(3):

				piece = UiPiece([20+x*115, 375+y*110], [110, 100],
					manger.LoadImage("Button"))

				piece.SetUpButton(False, manger.LoadImage("Button_Hover"),
					manger.LoadImage("Button_Pressed"),
					onClick=self.SetOperation, onClickData=loop)
				piece.SetUpLabel(loop)
				manger.PieceList += [piece]


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
		input("error: "+str(e))
