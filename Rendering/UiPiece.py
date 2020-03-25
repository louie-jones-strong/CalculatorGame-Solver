from pygame import mouse, draw
import pygame
from enum import Enum

class UiPiece:

	class eState(Enum):
		Normal = 0
		Hover = 1
		press = 2
		Fade = 3


	def __init__(self, pos, size, normalImage=None):
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
		self.AudioPlayer = None
		self.ButtonDownAudioEvent = None
		self.ButtonUpAudioEvent = None
		return
	
	def UiMangerSetup(self, audioPlayer, imageDrawer):
		self.AudioPlayer = audioPlayer
		self.Drawer = imageDrawer
		return

	def SetUpButton(self, buttonHoldAllowed, hoverImage=None, pressImage=None, onClick=None, onClickData=None, enterCanClick=False):
		self.ButtonHoldAllowed = buttonHoldAllowed
		self.HoverImage = hoverImage
		self.PressImage = pressImage
		self.OnClick = onClick
		self.OnClickData = onClickData
		self.EnterCanClick = enterCanClick
		return

	def SetupAudio(self, buttonDownEvent, buttonUpEvent):
		self.ButtonDownAudioEvent = buttonDownEvent
		self.ButtonUpAudioEvent = buttonUpEvent
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

		if self.AudioPlayer != None:
			if self.State == UiPiece.eState.press and self.LastState != UiPiece.eState.press:
				self.AudioPlayer.PlayEvent(self.ButtonDownAudioEvent)

			elif self.State != UiPiece.eState.press and self.LastState == UiPiece.eState.press:
				self.AudioPlayer.PlayEvent(self.ButtonUpAudioEvent)

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
							self.EditableMessage *= 10
							self.EditableMessage += int(event.unicode)
						except Exception as e:
							pass
					

					number = self.EditableMessage
					if self.EditableIsNegtive:
						number *= -1

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
			font = pygame.font.SysFont("monospace", 200)
			text = str(self.Message)
			if self.EditableIsNegtive:
				text += "-"
			
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
