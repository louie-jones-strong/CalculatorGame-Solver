class Operation:
	BaseImage = ""
	NumberOfSetting = 0
	Setting = []
	OperationId = 0

	def __init__(self, Id):
		self.OperationId = Id
		self.Setting = []
		for loop in range(self.NumberOfSetting):
			self.Setting += [0]
		return

	def Setup(self):

		return

	def DoAction(self, inputValue):

		return inputValue

	def ToString(self):

		return "?"

	def GetSetting(self, index):
		if len(self.Setting) > index and index >= 0:
			return self.Setting[index]
		return 0

	def SetSetting(self, index, value):
		if len(self.Setting) > index and index >= 0:
			self.Setting[index] = value
			
		return

	def IsValid(self):
		number = 1234
		newNumber = self.DoAction(number)
		return number != newNumber

	def Serialize(self):
		return {"OpType":self.OperationId, "Settings": self.Setting}

def MakeOperation(opType=None):
	#do not change the order of this list
	opList = [
		Operation, 
		Add,
		Multiply,
		Divide,
		ShiftRight,
		ShiftLeft,
		Insert,
		Translate,
		Pow,
		Flip,
		Reverse,
		Sum]

	if opType == None:
		text = "Type none [0]"

		for loop in range(1, len(opList)):
			op = opList[loop](loop)
			text += " " + str(type(op).__name__) + "["+str(loop)+"]"
		text += ": "
		opType = int(input(text))

	if opType >= 0 and opType < len(opList):
		return opList[opType](opType)

	return None

class Add(Operation):
	BaseImage = "Button_Black"
	NumberOfSetting = 1

	def Setup(self, addAmount=None):
		if addAmount == None:
			addAmount = int(input("Add Value: "))

		self.Setting[0] = addAmount
		return

	def DoAction(self, inputValue):

		return inputValue + self.Setting[0]

	def ToString(self):
		if self.Setting[0] >= 0:
			return "+"+str(self.Setting[0])
		else:
			return str(self.Setting[0])

class Multiply(Operation):
	BaseImage = "Button_Black"
	NumberOfSetting = 1

	def Setup(self, multiplyAmount=None):

		if multiplyAmount == None:
			multiplyAmount = int(input("multiply Value: "))

		self.Setting[0] = multiplyAmount
		return

	def DoAction(self, inputValue):

		return inputValue * self.Setting[0]

	def ToString(self):

		return "X"+str(self.Setting[0])

	def IsValid(self):
		return self.Setting[0] != 0 and super().IsValid()

class Divide(Operation):
	BaseImage = "Button_Black"
	NumberOfSetting = 1

	def Setup(self, divideAmount=None):
		if divideAmount == None:
			divideAmount = int(input("Divide Value: "))

		self.Setting[0] = divideAmount
		return

	def DoAction(self, inputValue):
		output = inputValue / self.Setting[0]
		if int(output) == output:
			return int(output)
		return output

	def ToString(self):

		return "/"+str(self.Setting[0])

	def IsValid(self):
		return self.Setting[0] != 0 and super().IsValid()

class ShiftRight(Operation):
	BaseImage = "Button_Orange"

	def Setup(self):
		return

	def DoAction(self, inputValue):
		return int(inputValue / 10)

	def ToString(self):
		return "<<"

class ShiftLeft(Operation):
	BaseImage = "Button_Orange"

	def Setup(self):
		return

	def DoAction(self, inputValue):
		return inputValue * 10

	def ToString(self):
		return ">>"

class Insert(Operation):
	BaseImage = "Button_Purple"
	NumberOfSetting = 1

	def Setup(self, insertNumber=None):
		if insertNumber == None:
			insertNumber = int(input("Insert Number: "))
		self.Setting[0] = insertNumber
		return

	def DoAction(self, inputValue):
		return int(str(inputValue) + str(self.Setting[0]))

	def ToString(self):
		return "Insert "+str(self.Setting[0])

class Translate(Operation):
	BaseImage = "Button_Orange"
	NumberOfSetting = 2

	def Setup(self, fromNum=None, toNum=None):

		if fromNum == None:
			fromNum = int(input("From: "))

		if toNum == None:
			toNum = int(input("To: "))

		self.Setting[0] = fromNum
		self.Setting[1] = toNum
		return

	def DoAction(self, inputValue):

		return int(str(inputValue).replace(str(self.Setting[0]), str(self.Setting[1])))
	
	def ToString(self):

		return str(self.Setting[0]) + "=>" + str(self.Setting[1])
	
	def IsValid(self):
		return self.Setting[0] != self.Setting[1]

class Pow(Operation):
	BaseImage = "Button_Orange"

	def DoAction(self, inputValue):
		return inputValue ** 2

	def ToString(self):
		return "Pow "+str(2)

class Flip(Operation):
	BaseImage = "Button_Orange"

	def DoAction(self, inputValue):
		return inputValue * -1

	def ToString(self):
		return "+/- "

class Reverse(Operation):
	BaseImage = "Button_Orange"

	def DoAction(self, inputValue):
		if inputValue > 0:
			return int(str(inputValue)[::-1])
		else:
			return int(str(inputValue*-1)[::-1])*-1

	def ToString(self):
		return "Reverse"

class Sum(Operation):
	BaseImage = "Button_Orange"

	def DoAction(self, inputValue):

		return sum( map(lambda x: int(x), str(inputValue)))
		

	def ToString(self):
		return "Sum"
