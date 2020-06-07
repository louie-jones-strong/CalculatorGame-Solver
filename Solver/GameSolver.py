import Solver.Operations as Operations
from enum import Enum

MaxCharacters = 6

class SolverOrderInfo:

	class eInteractType(Enum):
		Press = 0
		Hold = 1

	def __init__(self, opIndex, interactType, order):
		self.OpIndex = opIndex
		self.InteractType = interactType
		self.Order = order
		return

	def __str__(self):
		text = ""
		if self.InteractType == SolverOrderInfo.eInteractType.Hold:
			text += "Hold "
		#else:
		#	text += "Press "

		text += str(self.Order+1)

		return text


class GameSolver:

	def __init__(self):
		self.Clear()
		return

	def AddSolve(self, solveOrder):
		self.PossibleSolves += [solveOrder]
		if self.BestSolve == None or len(solveOrder) < len(self.BestSolve):
			self.BestSolve = solveOrder
		return

	def Clear(self):
		self.PossibleSolves = []
		self.BestSolve = None
		return

	def Solve(self, levelData):
		self.Clear()
		self.CheckOps(levelData, [])
		return self.BestSolve != None, self.BestSolve

	def CheckOps(self, levelData, solveOrder):

		for opIndex in range(len(levelData.OpList)):
			operation = levelData.OpList[opIndex]
			
			interactType = SolverOrderInfo.eInteractType.Press
			if issubclass(type(operation), Operations.ValueChangeOp):
				newSolveOrder = solveOrder + [SolverOrderInfo(opIndex, interactType, len(solveOrder))]
				self.CheckValueChangeOp(opIndex, levelData, newSolveOrder)

				interactType = SolverOrderInfo.eInteractType.Hold

			if issubclass(type(operation), Operations.OpListChangeOp):
				newSolveOrder = solveOrder + [SolverOrderInfo(opIndex, interactType, len(solveOrder))]
				self.CheckOpListChangeOp(opIndex, levelData, newSolveOrder)
			
		return

	def CheckValueChangeOp(self, opIndex, levelData, solveOrder):
		newCurrentNumber = levelData.OpList[opIndex].DoActionOnValue(levelData.StartingNum)
		
		if int(newCurrentNumber) != newCurrentNumber:
			return
		newCurrentNumber = DoPortalMoves(newCurrentNumber, levelData.PortalFrom, levelData.PortalTo)
		
		if levelData.Goal == newCurrentNumber:
			self.AddSolve(solveOrder)
			return

		elif len(str(newCurrentNumber)) > MaxCharacters:
			return

		elif newCurrentNumber == levelData.StartingNum:
			return
		
		elif int(newCurrentNumber) != newCurrentNumber:
			return

		elif levelData.Moves > 1:
			newLevelData = levelData.Copy()
			newLevelData.Moves -= 1
			newLevelData.StartingNum = newCurrentNumber

			self.CheckOps(newLevelData, solveOrder)

		return

	def CheckOpListChangeOp(self, opIndex, levelData, solveOrder):
		newOpList = levelData.OpList[opIndex].DoActionOnOpList(levelData.OpList, levelData.StartingNum)

		if levelData.OpList == newOpList:
			return
		
		elif levelData.Moves > 1:
			newLevelData = levelData.Copy()
			newLevelData.Moves -= 1
			newLevelData.OpList = newOpList

			self.CheckOps(newLevelData, solveOrder)

		return

def DoPortalMoves(currentNumber, portalFrom, portalTo):
	if portalFrom != None and portalTo != None:
		if portalFrom <= portalTo:
			print("Error portalFrom <= portalTo")
			return currentNumber
			
		if currentNumber < 0:
			currentNumber *= -1
		
		numberString = str(currentNumber)

		if len(numberString) > portalFrom:
			addValue = numberString[ len(numberString)-(portalFrom+1) ]
			addValue = int(addValue)

			before = numberString[ : len(numberString)-(portalFrom+1) ]
			after = numberString[ len(numberString)-portalFrom : ]
			joined = before + after

			currentNumber = int(joined)
			if portalTo > 0:
				addValue = addValue * (10*portalTo)

			currentNumber += addValue
			currentNumber = DoPortalMoves(currentNumber, portalFrom, portalTo)

	return currentNumber
