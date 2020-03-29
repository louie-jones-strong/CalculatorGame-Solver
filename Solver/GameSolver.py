def Solve(movesLeft, operations, currentNumber, targetNumber):

	for operation in operations:
		newCurrentNumber = operation.DoAction(currentNumber)
		
		if targetNumber == newCurrentNumber:
			return True, [operation]

		elif len(str(newCurrentNumber)) > 6:
			continue

		elif newCurrentNumber == currentNumber:
			continue
		
		elif int(newCurrentNumber) != newCurrentNumber:
			continue

		elif movesLeft > 1:
			found, operationList = Solve(
				movesLeft-1, operations, newCurrentNumber, targetNumber)

			if found:
				return True, [operation] + operationList

	return False, []

def Main():
	while True:
		print("===================")
		print("")
		startNumber = int(input("Starting Number: "))
		targetNumber = int(input("Target Number: "))

		moves = int(input("Moves: "))

		operations = []

		while True:
			operation = Operations.MakeOperation()
			operation.Setup()
			if type(operation) == type(Operations.Operation()):
				break
			
			operations += [operation]

		found, operationList = Solve(moves, operations, startNumber, targetNumber)

		print("===================")
		print("")
		print("Found: "+str(found))
		print("")
		print("")

		for operation in operationList:
			print(operation.ToString())
	return


if __name__ == "__main__":
	import Operations
	Main()
