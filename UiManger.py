from pygame import display, draw, Color, gfxdraw, mouse
import pygame
import os

class UiPiece:#todo make this a sprite to speed it up

	def __init__(self, pos, size, normalImage=None):
		self.Pos = pos
		self.Size = size
		self.NormalImage = normalImage
		self.HoverImage = None
		self.PressImage = None
		self.OnClick = None
		self.OnClickData = None
		self.FadedImage = None
		self.GetIsFade = None

		if self.NormalImage != None:
			self.NormalImage = pygame.transform.scale(self.NormalImage, self.Size)
		return

	def SetUpButton(self, hoverImage=None, pressImage=None, onClick=None, onClickData=None):
		self.HoverImage = hoverImage
		self.PressImage = pressImage
		self.OnClick = onClick
		self.OnClickData = onClickData

		if self.HoverImage != None:
			self.HoverImage = pygame.transform.scale(self.HoverImage, self.Size)
		if self.PressImage != None:
			self.PressImage = pygame.transform.scale(self.PressImage, self.Size)
		return

	def SetUpFade(self, fadedImage, getIsFade):
		self.FadedImage = fadedImage
		self.GetIsFade = getIsFade
		#todo make a fade time
		if self.FadedImage != None:
			self.FadedImage = pygame.transform.scale(self.FadedImage, self.Size)
		return
		
	def Update(self, screen, debugMode):
		pos = mouse.get_pos()
		mouseOverButton = (pos[0] > self.Pos[0] and pos[0] < self.Pos[0] + self.Size[0] and
							pos[1] > self.Pos[1] and pos[1] < self.Pos[1] + self.Size[1])

		mouseDown = mouse.get_pressed()[0]
		if mouseOverButton and mouseDown:
			if self.OnClick != None:
				if self.OnClickData == None:
					self.OnClick()
				else:
					self.OnClick(self.OnClickData)

			if self.PressImage != None:
				screen.blit(self.PressImage, self.Pos)
			elif self.NormalImage != None:
				screen.blit(self.NormalImage, self.Pos)
		
		elif self.GetIsFade != None and self.GetIsFade():
			if self.FadedImage != None:
				screen.blit(self.FadedImage, self.Pos)

		elif mouseOverButton and not mouseDown:
			if self.HoverImage != None:
				screen.blit(self.HoverImage, self.Pos)
			elif self.NormalImage != None:
				screen.blit(self.NormalImage, self.Pos)

		else:
			if self.NormalImage != None:
				screen.blit(self.NormalImage, self.Pos)

		if debugMode:
			rect = [self.Pos[0], self.Pos[1], self.Size[0], self.Size[1]]
			draw.rect(screen, [255, 0, 0], rect, 2)
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
		return

	def Update(self):
		if not self.Running:
			return

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.Quit()
				return

		self.Window.blit(self.BackGround, [0, 0])

		for button in self.PieceList:
			button.Update(self.Window, self.DebugMode)
		
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
		piece.SetUpButton(onClick=self.SetSolarCovered)
		manger.PieceList += [piece]

		piece = UiPiece([40, 90], [90, 50], manger.LoadImage("FunGuy_Normal"))
		piece.SetUpFade(manger.LoadImage("FunGuy_Faded"), self.GetSolarCovered)
		manger.PieceList += [piece]

		piece = UiPiece([140, 90], [90, 50], manger.LoadImage("TopStats_Normal"))
		piece.SetUpFade(manger.LoadImage("TopStats_Faded"), self.GetSolarCovered)
		manger.PieceList += [piece]

		piece = UiPiece([245, 90], [90, 50], manger.LoadImage("TopStats_Normal"))
		piece.SetUpFade(manger.LoadImage("TopStats_Faded"), self.GetSolarCovered)
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
		piece.SetUpButton(onClick=self.SetUpOperationSelectScreen, onClickData=0)
		manger.PieceList += [piece]

		piece = UiPiece([246, 375], [113, 100])
		manger.PieceList += [piece]

		#row 2
		piece = UiPiece([20, 485], [113, 100])
		manger.PieceList += [piece]

		piece = UiPiece([133, 485], [113, 100])
		piece.SetUpButton(onClick=self.SetUpOperationSelectScreen, onClickData=1)
		manger.PieceList += [piece]

		piece = UiPiece([246, 485], [113, 100])
		piece.SetUpButton(onClick=self.SetUpOperationSelectScreen, onClickData=2)
		manger.PieceList += [piece]

		#row 3
		piece = UiPiece([20, 595], [113, 100],
                  manger.LoadImage("Button"))
		manger.PieceList += [piece]

		piece = UiPiece([133, 595], [113, 100])
		piece.SetUpButton(onClick=self.SetUpOperationSelectScreen, onClickData=3)
		manger.PieceList += [piece]

		piece = UiPiece([246, 595], [113, 100])
		piece.SetUpButton(onClick=self.SetUpOperationSelectScreen, onClickData=4)
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
		#row 1
		piece = UiPiece([20, 375], [113, 100],
                  manger.LoadImage("Button"))
		piece.SetUpButton(onClick=self.SetOperation, onClickData=0)
		manger.PieceList += [piece]

		piece = UiPiece([133, 375], [113, 100],
                  manger.LoadImage("Button"))
		piece.SetUpButton(onClick=self.SetOperation, onClickData=1)
		manger.PieceList += [piece]

		piece = UiPiece([246, 375], [113, 100],
                  manger.LoadImage("Button"))
		piece.SetUpButton(onClick=self.SetOperation, onClickData=2)
		manger.PieceList += [piece]
		return


if __name__ == "__main__":
	try:
		manger = UiManger()
		manger.DebugMode = True
		manger.SetUpMainScreen()
		while manger.Running:
			manger.Update()

	except:
		input("error:")
