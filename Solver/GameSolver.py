def Solve(movesLeft, operations, currentNumber, targetNumber):

	for loop in range(len(operations)):
		operation = operations[loop]

		newCurrentNumber = operation.DoActionOnValue(currentNumber)
		newoperationsList = operation.DoActionOnOpList(operations)
		
		if targetNumber == newCurrentNumber:
			return True, [loop]

		elif len(str(newCurrentNumber)) > 6:
			continue

		elif newCurrentNumber == currentNumber and operations == newoperationsList:
			continue
		
		elif int(newCurrentNumber) != newCurrentNumber:
			continue

		elif movesLeft > 1:
			found, operationList = Solve(
				movesLeft-1, newoperationsList, newCurrentNumber, targetNumber)

			if found:
				return True, [loop] + operationList

	return False, []