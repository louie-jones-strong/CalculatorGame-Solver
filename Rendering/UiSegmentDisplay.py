import Rendering.SharedRendering.UiPiece as UiPiece


class Character:
	Number = None
	ToPortal = None
	FromPortal = None

class UiSegmentDisplay:

	def __init__(self, uiManger, maxCharacters, pos, size, setFromPortal, setToPortal):
		gap = 10
		subNumberSize = [int((size[0]-(gap*(maxCharacters-1)))/maxCharacters), size[1]]
		subPortalSize = [30, 15]
		xpos = pos[0]
		xPortalPos = pos[0]
		xPortalPos += int((subNumberSize[0] - subPortalSize[0]) / 2)

		self.CharacterList = []
		for loop in range(maxCharacters):
			character = Character()

			index = maxCharacters-(loop+1)


			subNumberPos = [xpos, pos[1]]
			#number
			piece = UiPiece.UiPiece(subNumberPos, subNumberSize, normalImage="Number_Empty")
			uiManger.AddPiece(piece, False)
			character.Number = piece

			if loop > 0:
				subPortalPos = [xPortalPos, pos[1]-(subPortalSize[1]+5)]
				#to portal
				piece = UiPiece.UiPiece(subPortalPos, subPortalSize, normalImage="Portal_False")
				piece.SetUpButtonClick(onClick=setToPortal, onClickData=index)
				uiManger.AddPiece(piece, False)
				character.ToPortal = piece

			if loop < maxCharacters-1:
				subPortalPos = [xPortalPos, pos[1]+size[1]+5]
				#from portal
				piece = UiPiece.UiPiece(subPortalPos, subPortalSize, normalImage="Portal_False")
				piece.SetUpButtonClick(onClick=setFromPortal, onClickData=index)
				uiManger.AddPiece(piece, False)
				character.FromPortal = piece

			self.CharacterList += [character]
			xpos += subNumberSize[0] + gap
			xPortalPos += subNumberSize[0] + gap
		return

	LastNumber = None
	LastToPortal = None
	LastFromPortal = None
	def Update(self, levelData):

		number = levelData.StartingNum
		fromPortal = levelData.PortalFrom
		toPortal = levelData.PortalTo

		if (self.LastNumber == number and 
			self.LastFromPortal == fromPortal and 
			self.LastToPortal == toPortal):
			return
		self.LastNumber = number
		self.LastFromPortal = fromPortal
		self.LastToPortal = toPortal

		stringNum = str(number)

		for loop in range(len(self.CharacterList)):
			
			index = len(self.CharacterList)-(loop+1)

			image = "Number_"
			if len(stringNum) <= index:
				image += "Empty"
			else:
				image += stringNum[index]
			
			self.CharacterList[loop].Number.NormalImage = image

			if self.CharacterList[loop].FromPortal != None:
				isPortal = index == fromPortal
				self.CharacterList[loop].FromPortal.NormalImage = "Portal_"+str(isPortal)
			
			if self.CharacterList[loop].ToPortal != None:
				isPortal = index == toPortal
				self.CharacterList[loop].ToPortal.NormalImage = "Portal_"+str(isPortal)
			

		return