import Operations

def Solve(movesLeft, operations, currentNumber, targetNumber):

	for operation in operations:
		newCurrentNumber = operation.DoAction(currentNumber)
		
		if targetNumber == newCurrentNumber:
			return True, [operation]

		elif int(newCurrentNumber) != newCurrentNumber:
			continue

		elif movesLeft > 1:
			found, operationList = Solve(
				movesLeft-1, operations, newCurrentNumber, targetNumber)

			if found:
				return True, [operation] + operationList

	return False, []

def MakeOperation():
	opType = int(input("Type none [0] +[1] *[2] /[3] <<[4] Insert[5] =>[6] pow[7] +/-[8] Reverse[9] Sum[10]: "))

	if opType == 1:
		return Operations.Add()

	elif  opType == 2:
		return Operations.Multiply()

	elif opType == 3:
		return Operations.Divide()

	elif opType == 4:
		return Operations.Shift()

	elif opType == 5:
		return Operations.Insert()
	
	elif opType == 6:
		return Operations.Translate()

	elif opType == 7:
		return Operations.Pow()

	elif opType == 8:
		return Operations.Flip()

	elif opType == 9:
		return Operations.Reverse()

	elif opType == 10:
		return Operations.Sum()

	return None

def Main():
	while True:
		print("===================")
		print("")
		startNumber = int(input("Starting Number: "))
		targetNumber = int(input("Target Number: "))

		moves = int(input("Moves: "))

		operations = []

		while True:
			operation = MakeOperation()

			if operation == None:
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
	Main()
