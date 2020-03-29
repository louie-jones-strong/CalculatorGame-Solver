def Solve(movesLeft, operations, currentNumber, targetNumber):

	for operation in operations:
		newCurrentNumber = operation.DoActionOnValue(currentNumber)
		newoperationsList = operation.DoActionOnOpList(operations)
		
		if targetNumber == newCurrentNumber:
			return True, [operation]

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
				return True, [operation] + operationList

	return False, []