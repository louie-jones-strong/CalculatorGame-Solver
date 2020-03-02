from pygame import display, draw, Color, gfxdraw, mouse
import pygame
import os

class UiButton:#todo make this a sprite to speed it up

	def __init__(self, pos, size, normalImage=None, hoverImage=None, pressImage=None):
		self.Pos = pos
		self.Size = size
		self.NormalImage = normalImage
		self.HoverImage = hoverImage
		self.PressImage = pressImage

		if self.NormalImage != None:
			self.NormalImage = pygame.transform.scale(self.NormalImage, size)
		if self.HoverImage != None:
			self.HoverImage = pygame.transform.scale(self.HoverImage, size)
		if self.PressImage != None:
			self.PressImage = pygame.transform.scale(self.PressImage, size)
		return

	def Update(self, screen, debugMode):
		pos = mouse.get_pos()
		mouseOverButton = (pos[0] > self.Pos[0] and pos[0] < self.Pos[0] + self.Size[0] and
							pos[1] > self.Pos[1] and pos[1] < self.Pos[1] + self.Size[1])

		mouseDown = mouse.get_pressed()[0]

		if mouseOverButton and mouseDown:
			if self.PressImage != None:
				screen.blit(self.PressImage, self.Pos)
			elif self.NormalImage != None:
				screen.blit(self.NormalImage, self.Pos)

		elif mouseOverButton and not mouseDown:
			if self.HoverImage != None:
				screen.blit(self.HoverImage, self.Pos)
			elif self.NormalImage != None:
				screen.blit(self.NormalImage, self.Pos)

		elif not mouseOverButton:
			if self.NormalImage != None:
				screen.blit(self.NormalImage, self.Pos)

		if debugMode:
			rect = [self.Pos[0], self.Pos[1], self.Size[0], self.Size[1]]
			draw.rect(screen, [255, 0, 0], rect, 2)
		return

class UiManger:
	ImageCache = {}
	ButtonList = []
	DebugMode = False

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

		backGround = self.LoadImage("BackGround", 0.35)
		self.Resolution = backGround.get_size()

		#window
		self.Window = display.set_mode(self.Resolution)
		
		self.Window.blit(backGround, [0,0])
		return

	def Run(self):
		while self.Running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					self.Running = False
					return False

			for button in self.ButtonList:
				button.Update(self.Window, self.DebugMode)

			if self.DebugMode and mouse.get_pressed()[0]:
				print("mouse pos: "+str(mouse.get_pos()))

			display.update()
		return


if __name__ == "__main__":
	try:
		manger = UiManger()
		manger.DebugMode = True

		manger.ButtonList += [UiButton([20,375], [110,100], 
			manger.LoadImage("Button"), 
			manger.LoadImage("Button_Hover"), 
			manger.LoadImage("Button_Pressed"))]

		manger.ButtonList += [UiButton([220,30], [105,35])]

		manger.Run()
	except:
		input("error:")