import Solver.Operations as Operations

def Solve(movesLeft, opList, currentNumber, targetNumber):

	for opIndex in range(len(opList)):
		operation = opList[opIndex]

		if issubclass(type(operation), Operations.ValueChangeOp):
			found, solveOrder = CheckValueChangeOp(opIndex, movesLeft, opList, currentNumber, targetNumber)
			if found:
				return True, solveOrder

		if issubclass(type(operation), Operations.OpListChangeOp):
			found, solveOrder = CheckOpListChangeOp(opIndex, movesLeft, opList, currentNumber, targetNumber)
			if found:
				return True, solveOrder
		
	return False, []

def CheckValueChangeOp(opIndex, movesLeft, opList, currentNumber, targetNumber):
	newCurrentNumber = opList[opIndex].DoActionOnValue(currentNumber)
	
	if targetNumber == newCurrentNumber:
		return True, [opIndex]

	elif len(str(newCurrentNumber)) > 6:
		return False, []

	elif newCurrentNumber == currentNumber:
		return False, []
	
	elif int(newCurrentNumber) != newCurrentNumber:
		return False, []

	elif movesLeft > 1:
		found, solveOrder = Solve(movesLeft-1, opList, newCurrentNumber, targetNumber)

		if found:
			return True, [opIndex] + solveOrder

	return False, []

def CheckOpListChangeOp(opIndex, movesLeft, opList, currentNumber, targetNumber):
	newOpList = opList[opIndex].DoActionOnOpList(opList)

	if opList == newOpList:
		return False, []
	
	elif movesLeft > 1:
		found, solveOrder = Solve(movesLeft-1, newOpList, currentNumber, targetNumber)

		if found:
			return True, [opIndex] + solveOrder

	return False, []