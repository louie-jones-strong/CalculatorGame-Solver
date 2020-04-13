import Rendering.SharedRendering.UiPiece as UiPiece

class UiSegmentDisplay:

	def __init__(self, uiManger, maxCharacters, pos, size):
		gap = 10
		subSize = [int((size[0]-(gap*(maxCharacters-1)))/maxCharacters), size[1]]
		xpos = pos[0]
		
		self.NumPieceList = []
		for loop in range(maxCharacters):
			subPos = [xpos, pos[1]]
			piece = UiPiece.UiPiece(subPos, subSize, normalImage="Number_Empty")
			uiManger.AddPiece(piece, False)
			self.NumPieceList += [piece]

			xpos += subSize[0] + gap
		return

	LastNumber = None
	def Update(self, number):

		if self.LastNumber == number:
			return
		LastNumber = number

		stringNum = str(number)

		for loop in range(len(self.NumPieceList)):
			
			index = -(loop+1)

			image = "Number_"
			if len(stringNum) < abs(index):
				image += "Empty"
			else:
				image += stringNum[index]
			
			self.NumPieceList[index].NormalImage = image

		return