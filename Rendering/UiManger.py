from pygame import display, Color, mouse
import pygame
import time
import os

class UiManger:

	def __init__(self, audioManger, imageDrawer, title="Window", icon=None):
		self.Running = True
		self.DebugMode = False

		display.init()
		pygame.font.init()
		pygame.init()
		self.ScaleFactor = 1
		self.AudioPlayer = audioManger
		self.Drawer = imageDrawer

		pygame.display.set_icon(self.Drawer.GetRawImage(icon))
		pygame.display.set_caption(title)
		
		info = pygame.display.Info()
		self.Resolution = [378, 704]
		self.SystemResolution = [info.current_w, info.current_h]
		self.UpdateWindowSize()

		self.PieceList = []
		self.Selectable = []
		self.MouseStartPos = None
		self.SelectIndex = 0
		self.OperationSetUpIndex = None
		self.LastUpdateTime = time.time()
		self.Clock = pygame.time.Clock()
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

		piece.UiMangerSetup(self.AudioPlayer, self.Drawer)
		self.PieceList += [piece]
		return

	def Update(self):
		if not self.Running:
			return False
		eventList = []
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.Quit()
				return False

			elif event.type == pygame.VIDEORESIZE:
				self.UpdateWindowSize(event.w, event.h)

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
			font = pygame.font.SysFont("monospace", 20)
			text = "FPS: "
			text += str(round(self.Clock.get_fps()))
			text += " LastFrame: "
			text += str(round(self.Clock.get_rawtime()/1000,3))
			label = font.render(text, 1, (255, 0, 0))
			self.Window.blit(label, [8, 8])

			if mouse.get_pressed()[0]:
				if self.MouseStartPos == None:
					self.MouseStartPos = list(mouse.get_pos())
					
				size = [mouse.get_pos()[0]-self.MouseStartPos[0],
						mouse.get_pos()[1]-self.MouseStartPos[1]]
				print("mouse Pos / Size: " + str(self.MouseStartPos) + ", " + str(size))
				
			else:
				self.MouseStartPos = None

			
			

		display.update()
		self.Clock.tick()

		self.SolarCovered = False
		self.LastUpdateTime = time.time()
		return True

	def Quit(self):
		pygame.quit()
		self.Running = False
		return
	
	def UpdateWindowSize(self, width=None, hight=None):
		maxWidth = int(self.SystemResolution[0] * 0.6)
		maxHight = int(self.SystemResolution[1] * 0.6)

		minWidth = int(self.SystemResolution[0] * 0.25)
		minHight = int(self.SystemResolution[1] * 0.25)

		if width == None or hight == None:
			width = maxWidth
			hight = maxHight

		if [width, hight] != self.Resolution:

			if width < minWidth:
				width = minWidth
			if hight < minHight:
				hight = minHight

			xRatio = width / self.Resolution[0]
			yRatio = hight / self.Resolution[1]

			if xRatio < yRatio:
				ratio = xRatio
			else:
				ratio = yRatio

			self.Resolution = [int(self.Resolution[0] * ratio), int(self.Resolution[1] * ratio)]
			self.ScaleFactor *= ratio
			self.Window = display.set_mode(self.Resolution, pygame.RESIZABLE)

			if self.DebugMode:
				print("reSized to: "+str(self.Resolution))
		return