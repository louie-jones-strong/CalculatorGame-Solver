from pygame import mouse, draw
import pygame
from enum import Enum

class UiPiece:
	class eState(Enum):
		Normal = 0
		Hover = 1
		press = 2
		Fade = 3

	def __init__(self, pos, size, normalImage=None, hoverImage=None):
		self.State = UiPiece.eState.Normal
		self.LastState = self.State
		self.BasePos = pos
		self.BaseSize = size
		self.NormalImage = normalImage
		self.HoverImage = hoverImage


		self.PressImage = None
		self.LastFrameMouseDown = False
		self.TimeInState = 0
		self.Selected = False
		self.Selectable = False
		self.EnterCanClick = False
		self.HideLabel = False
		return

	def UiMangerSetup(self, audioPlayer, imageDrawer):
		self.AudioPlayer = audioPlayer
		self.Drawer = imageDrawer
		return

	OnClick = None
	OnClickData = None
	def SetUpButtonClick(self, pressImage=None, onClick=None, onClickData=None, enterCanClick=False):
		self.PressImage = pressImage

		self.OnClick = onClick
		self.OnClickData = onClickData
		self.EnterCanClick = enterCanClick
		return

	OnHold = None
	OnHoldData = None
	MinHoldTime = 0
	def SetUpButtonHold(self, pressImage=None, onHold=None,
			onHoldData=None, minHoldTime=1, maxTimeBetweenHold=0.25):
		self.PressImage = pressImage

		self.OnHold = onHold
		self.OnHoldData = onHoldData
		self.MinHoldTime = minHoldTime
		self.MaxTimeBetweenHold = maxTimeBetweenHold
		return

	ButtonDownAudioEvent = None
	ButtonUpAudioEvent = None
	def SetupAudio(self, buttonDownEvent, buttonUpEvent):
		self.ButtonDownAudioEvent = buttonDownEvent
		self.ButtonUpAudioEvent = buttonUpEvent
		return

	LabelColour = (255,255,255)
	Message = None
	EditableMessage = None
	GetMessageText = None
	def SetUpLabel(self, message, editableMessage, labelColour=(255, 255, 255),
			xLabelAnchor=0, yLabelAnchor=0, textUpdatedFunc=None, getMessage=None, hideLabel=False):
		self.Message = str(message)
		self.EditableMessage = editableMessage
		self.EditableIsNegtive = False
		self.LabelColour = labelColour
		self.XLabelAnchor = xLabelAnchor
		self.YLabelAnchor = yLabelAnchor
		self.TextUpdatedFunc = textUpdatedFunc
		self.GetMessageText = getMessage
		self.HideLabel = hideLabel
		return

	FadedImage = None
	GetIsFade = None
	def SetUpFade(self, getIsFade, fadedImage=""):
		self.FadedImage = fadedImage
		self.GetIsFade = getIsFade
		#todo make a fade time
		return

	def Update(self, screen, debugMode, deltaTime, scaleFactor):
		self.TimeInState += deltaTime
		self.TimeSinceLastHold += deltaTime

		self.Pos = [int(self.BasePos[0]*scaleFactor),
				int(self.BasePos[1]*scaleFactor)]
		self.Size = [int(self.BaseSize[0]*scaleFactor),
				int(self.BaseSize[1]*scaleFactor)]

		pos = mouse.get_pos()
		mouseDown = mouse.get_pressed()[0]
		mouseOverButton = (pos[0] > self.Pos[0] and pos[0] < self.Pos[0] + self.Size[0] and
							pos[1] > self.Pos[1] and pos[1] < self.Pos[1] + self.Size[1])

		if mouseOverButton:
			if self.LastFrameMouseDown and not mouseDown:
				self.TriggerOnClick(True)
			if self.State == UiPiece.eState.press and self.TimeInState >= self.MinHoldTime:
				self.TriggerOnHold()

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
		if (self.Selected and
			self.EditableMessage != None and
			self.State != UiPiece.eState.Fade):

			for event in events:
				if event.type == pygame.KEYDOWN:

					if event.key == pygame.K_BACKSPACE:
						self.EditableMessage = int(self.EditableMessage/10)

					elif event.unicode == "-":
						self.EditableIsNegtive = not self.EditableIsNegtive

					else:
						try:
							temp = int(event.unicode)
							if type(self.EditableMessage) is str:
								self.EditableMessage += str(temp)

							else:
								self.EditableMessage *= 10
								self.EditableMessage += int(temp)

						except Exception as e:
							pass


					number = self.EditableMessage
					if self.EditableIsNegtive:
						number *= -1

					if self.TextUpdatedFunc != None:
						self.TextUpdatedFunc(number)

		if self.GetMessageText != None:
			self.Message = str(self.GetMessageText())
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

		if self.State != UiPiece.eState.Fade and self.Message != None and not self.HideLabel:
			font = pygame.font.SysFont("monospace", 200)
			text = str(self.Message)
			if self.EditableIsNegtive:
				text += "-"

			if self.EditableMessage != None:
				text += str(self.EditableMessage)

			label = font.render(text, 1, self.LabelColour)

			xRatio = 1
			if label.get_width() != 0:
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

		if self.Selectable and self.Selected and self.State != UiPiece.eState.Fade:
			rect = [self.Pos[0], self.Pos[1], self.Size[0], self.Size[1]]
			draw.rect(screen, [255, 255, 255], rect, 2)

		if debugMode:
			font = pygame.font.SysFont("monospace", 10)

			text = self.State.name
			if self.Selectable:
				text += " " + str(self.Selected)

			if self.Message != None or self.EditableMessage != None:
				text += " \""

				if self.Message != None:
					text += str(self.Message)

				if self.EditableMessage != None:
					text += str(self.EditableMessage)

				text += "\""

			label = font.render(text, 1, (255, 0, 0))
			screen.blit(label, [self.Pos[0]+3, self.Pos[1]])
		return

	def SetUpSelect(self):
		self.Selectable = True
		return

	def TriggerOnClick(self, fromMouse):
		if self.EnterCanClick or fromMouse:
			if self.TimeInState < self.MinHoldTime or self.OnHold == None:
				if self.OnClick != None:
					if self.OnClickData == None:
						self.OnClick()
					else:
						self.OnClick(self.OnClickData)
		return

	TimeSinceLastHold = 0
	def TriggerOnHold(self):
		if self.OnHold != None:
			if self.TimeSinceLastHold > self.MaxTimeBetweenHold:

				self.TimeSinceLastHold = 0
				if self.OnHoldData == None:
					self.OnHold()
				else:
					self.OnHold(self.OnHoldData)
		return
