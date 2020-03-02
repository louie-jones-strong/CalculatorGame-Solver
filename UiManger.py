from pygame import display, draw, Color, gfxdraw, mouse
import pygame
import os

class UiButton:

	def __init__(self, pos, size, normalImage, hoverImage=None, pressImage=None):
		self.Pos = pos
		self.Size = size
		self.NormalImage = pygame.transform.scale(normalImage, size)
		self.HoverImage = pygame.transform.scale(hoverImage, size)
		self.PressImage = pygame.transform.scale(pressImage, size)
		return

	def Update(self, screen):
		pos = mouse.get_pos()
		mouseOverButton = (pos[0] > self.Pos[0] and pos[0] < self.Pos[0] + self.Size[0] and
							pos[1] > self.Pos[1] and pos[1] < self.Pos[1] + self.Size[1])

		mouseDown = mouse.get_pressed()[0]

		if mouseOverButton and mouseDown:
			if self.PressImage != None:
				screen.blit(self.PressImage, self.Pos)
			else:
				screen.blit(self.NormalImage, self.Pos)

		elif mouseOverButton and not mouseDown:
			if self.HoverImage != None:
				screen.blit(self.HoverImage, self.Pos)
			else:
				screen.blit(self.NormalImage, self.Pos)

		elif not mouseOverButton:
			screen.blit(self.NormalImage, self.Pos)
		return

class UiManger:
	ImageCache = {}
	ButtonList = []

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
				button.Update(self.Window)

			display.update()
		return


if __name__ == "__main__":
	try:
		manger = UiManger()
		manger.ButtonList += [UiButton([50,50], [100,100], 
			manger.LoadImage("Button"), 
			manger.LoadImage("Button_Hover"), 
			manger.LoadImage("Button_Pressed"))]

		manger.Run()
	except:
		input("error:")