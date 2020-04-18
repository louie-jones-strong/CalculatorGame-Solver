import Solver.Operations as Operations

MaxCharacters = 6

class GameSolver:

	def __init__(self):
		self.Clear()
		return

	def AddSolve(self, solveOrder):
		self.PossibleSolves += [solveOrder]
		if len(solveOrder) < len(self.BestSolve) or len(self.BestSolve) == 0:
			self.BestSolve = solveOrder
		return

	def Clear(self):
		self.PossibleSolves = []
		self.BestSolve = []
		return

	def Solve(self, levelData):
		self.Clear()
		found = self.CheckOps(levelData, [])
		return found, self.BestSolve

	def CheckOps(self, levelData, solveOrder):

		for opIndex in range(len(levelData.OpList)):
			operation = levelData.OpList[opIndex]

			if issubclass(type(operation), Operations.ValueChangeOp):
				found = self.CheckValueChangeOp(opIndex, levelData, solveOrder+[opIndex])
				if found:
					return True

			if issubclass(type(operation), Operations.OpListChangeOp):
				found = self.CheckOpListChangeOp(opIndex, levelData, solveOrder+[opIndex])
				if found:
					return True
			
		return False

	def CheckValueChangeOp(self, opIndex, levelData, solveOrder):
		newCurrentNumber = levelData.OpList[opIndex].DoActionOnValue(levelData.StartingNum)
		
		newCurrentNumber = DoPortalMoves(newCurrentNumber, levelData.PortalFrom, levelData.PortalTo)
		
		if levelData.Goal == newCurrentNumber:
			self.AddSolve(solveOrder)
			return True

		elif len(str(newCurrentNumber)) > MaxCharacters:
			return False

		elif newCurrentNumber == levelData.StartingNum:
			return False
		
		elif int(newCurrentNumber) != newCurrentNumber:
			return False

		elif levelData.Moves > 1:
			newLevelData = levelData.Copy()
			newLevelData.Moves -= 1
			newLevelData.StartingNum = newCurrentNumber

			found = self.CheckOps(newLevelData, solveOrder)

			if found:
				return True

		return False

	def CheckOpListChangeOp(self, opIndex, levelData, solveOrder):
		newOpList = levelData.OpList[opIndex].DoActionOnOpList(levelData.OpList, levelData.StartingNum)

		if levelData.OpList == newOpList:
			return False
		
		elif levelData.Moves > 1:
			newLevelData = levelData.Copy()
			newLevelData.Moves -= 1
			newLevelData.OpList = newOpList

			found = self.CheckOps(newLevelData, solveOrder)

			if found:
				return True

		return False

def DoPortalMoves(currentNumber, portalFrom, portalTo):
	if portalFrom != None and portalTo != None:

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
			currentNumber += addValue
			currentNumber = DoPortalMoves(currentNumber, portalFrom, portalTo)

	return currentNumber
