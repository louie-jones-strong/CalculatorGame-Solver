import Solver.Operations as Operations

def Solve(levelData):

	for opIndex in range(len(levelData.OpList)):
		operation = levelData.OpList[opIndex]

		if issubclass(type(operation), Operations.ValueChangeOp):
			found, solveOrder = CheckValueChangeOp(opIndex, levelData)
			if found:
				return True, solveOrder

		if issubclass(type(operation), Operations.OpListChangeOp):
			found, solveOrder = CheckOpListChangeOp(opIndex, levelData)
			if found:
				return True, solveOrder
		
	return False, []

def CheckValueChangeOp(opIndex, levelData):
	newCurrentNumber = levelData.OpList[opIndex].DoActionOnValue(levelData.StartingNum)
	
	newCurrentNumber = DoPortalMoves(newCurrentNumber, levelData.PortalFrom, levelData.PortalTo)
	
	if levelData.Goal == newCurrentNumber:
		return True, [opIndex]

	elif len(str(newCurrentNumber)) > 6:
		return False, []

	elif newCurrentNumber == levelData.StartingNum:
		return False, []
	
	elif int(newCurrentNumber) != newCurrentNumber:
		return False, []

	elif levelData.Moves > 1:
		newLevelData = levelData.Copy()
		newLevelData.Moves -= 1
		newLevelData.StartingNum = newCurrentNumber

		found, solveOrder = Solve(newLevelData)

		if found:
			return True, [opIndex] + solveOrder

	return False, []

def CheckOpListChangeOp(opIndex, levelData):
	newOpList = levelData.OpList[opIndex].DoActionOnOpList(levelData.OpList, levelData.StartingNum)

	if levelData.OpList == newOpList:
		return False, []
	
	elif levelData.Moves > 1:
		newLevelData = levelData.Copy()
		newLevelData.Moves -= 1
		newLevelData.OpList = newOpList

		found, solveOrder = Solve(newLevelData)

		if found:
			return True, [opIndex] + solveOrder

	return False, []

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