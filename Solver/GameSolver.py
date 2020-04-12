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
	
	if levelData.Goal == newCurrentNumber:
		return True, [opIndex]

	elif len(str(newCurrentNumber)) > 6:
		return False, []

	elif newCurrentNumber == levelData.StartingNum:
		return False, []
	
	elif int(newCurrentNumber) != newCurrentNumber:
		return False, []

	elif levelData.Moves > 1:
		levelData = levelData.Copy()
		levelData.Moves -= 1
		levelData.StartingNum = newCurrentNumber

		found, solveOrder = Solve(levelData)

		if found:
			return True, [opIndex] + solveOrder

	return False, []

def CheckOpListChangeOp(opIndex, levelData):
	newOpList = levelData.OpList[opIndex].DoActionOnOpList(levelData.OpList, levelData.StartingNum)

	if levelData.OpList == newOpList:
		return False, []
	
	elif levelData.Moves > 1:
		levelData = levelData.Copy()
		levelData.Moves -= 1
		levelData.OpList = newOpList

		found, solveOrder = Solve(levelData)

		if found:
			return True, [opIndex] + solveOrder

	return False, []