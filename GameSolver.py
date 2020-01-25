class Operation:
	def DoAction(self, inputValue):

		return inputValue

	def ToString(self):

		return

class Add(Operation):
	def __init__(self):
		self.AddAmount = int(input("Add Value: "))
		return

	def DoAction(self, inputValue):

		return inputValue + self.AddAmount

	def ToString(self):
		if self.AddAmount >= 0:
			return "+"+str(self.AddAmount)
		else:
			return str(self.AddAmount)

class Multiply(Operation):
	def __init__(self):
		self.MultiplyAmount = int(input("multiply Value: "))
		return

	def DoAction(self, inputValue):

		return inputValue * self.MultiplyAmount

	def ToString(self):

		return "X"+str(self.MultiplyAmount)

class Divide(Operation):
	def __init__(self):
		self.DivideAmount = int(input("Divide Value: "))
		return

	def DoAction(self, inputValue):
		output = inputValue / self.DivideAmount
		if int(output) == output:
			return int(output)
		return output

	def ToString(self):

		return "/"+str(self.DivideAmount)

class Shift(Operation):
	def __init__(self):
		self.RightShift = int(input("<<[1] >>[2]: ")) == 1
		return

	def DoAction(self, inputValue):
		if self.RightShift:
			return int(inputValue / 10)
		else:
			return inputValue * 10

	def ToString(self):
		if self.RightShift:
			return "<<"
		else:
			return ">>"

class Insert(Operation):
	def __init__(self):
		self.InsertNumber = int(input("Insert Number: "))
		return

	def DoAction(self, inputValue):
		return int(str(inputValue) + str(self.InsertNumber))

	def ToString(self):
		return "Insert "+str(self.InsertNumber)

class Translate(Operation):

	def __init__(self):
		self.From = int(input("From: "))
		self.To = int(input("To: "))
		return

	def DoAction(self, inputValue):

		return int(str(inputValue).replace(str(self.From), str(self.To)))
	
	def ToString(self):

		return str(self.From) + "=>" + str(self.To)

class Pow(Operation):
	def __init__(self):
		self.PowNumber = 2#int(input("pow Number: "))
		return

	def DoAction(self, inputValue):
		return inputValue ** self.PowNumber

	def ToString(self):
		return "Pow "+str(self.PowNumber)

class Flip(Operation):
	def __init__(self):
		return

	def DoAction(self, inputValue):
		return inputValue * -1

	def ToString(self):
		return "+/- "

class Reverse(Operation):
	def __init__(self):
		return

	def DoAction(self, inputValue):
		if inputValue > 0:
			return int(str(inputValue)[::-1])
		else:
			return int(str(inputValue*-1)[::-1])*-1

	def ToString(self):
		return "Reverse"

class Sum(Operation):
	def __init__(self):
		return

	def DoAction(self, inputValue):

		return sum( map(lambda x: int(x), str(inputValue)))
		

	def ToString(self):
		return "Sum"

def TryMove(movesLeft, operations, currentNumber, targetNumber):

	for operation in operations:
		newCurrentNumber = operation.DoAction(currentNumber)
		
		if targetNumber == newCurrentNumber:
			return True, [operation]

		elif int(newCurrentNumber) != newCurrentNumber:
			continue

		elif movesLeft > 1:
			found, operationList = TryMove(movesLeft-1, operations, newCurrentNumber, targetNumber)

			if found:
				return True, [operation] + operationList

	return False, []

def MakeOperation():
	opType = int(input("Type none [0] +[1] *[2] /[3] <<[4] Insert[5] =>[6] pow[7] +/-[8] Reverse[9] Sum[10]: "))

	if opType == 1:
		return Add()

	elif  opType == 2:
		return Multiply()

	elif opType == 3:
		return Divide()

	elif opType == 4:
		return Shift()

	elif opType == 5:
		return Insert()
	
	elif opType == 6:
		return Translate()

	elif opType == 7:
		return Pow()

	elif opType == 8:
		return Flip()

	elif opType == 9:
		return Reverse()

	elif opType == 10:
		return Sum()

	return None


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


	found, operationList = TryMove(moves, operations, startNumber, targetNumber)

	print("===================")
	print("")
	print("Found: "+str(found))
	print("")
	print("")

	for operation in operationList:
		print(operation.ToString())