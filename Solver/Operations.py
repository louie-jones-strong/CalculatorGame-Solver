class Operation:
	BaseImage = ""
	NumberOfSetting = 0
	Setting = []

	def __init__(self):
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

def MakeOperation(opType=None):
	if opType == None:
		opType = int(input("Type none [0] +[1] *[2] /[3] <<[4] >>[5] Insert[6] =>[7] pow[8] +/-[9] Reverse[10] Sum[11]: "))
	
	if opType == 0:
		return Operation()

	elif opType == 1:
		return Add()

	elif  opType == 2:
		return Multiply()

	elif opType == 3:
		return Divide()

	elif opType == 4:
		return ShiftRight()

	elif opType == 5:
		return ShiftLeft()

	elif opType == 6:
		return Insert()
	
	elif opType == 7:
		return Translate()

	elif opType == 8:
		return Pow()

	elif opType == 9:
		return Flip()

	elif opType == 10:
		return Reverse()

	elif opType == 11:
		return Sum()

	return None

class Add(Operation):#1
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

class Multiply(Operation):#2
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

class Divide(Operation):#3
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


class ShiftRight(Operation):  # 4
	BaseImage = "Button_Orange"

	def Setup(self):
		return

	def DoAction(self, inputValue):
		return int(inputValue / 10)

	def ToString(self):
		return "<<"

class ShiftLeft(Operation):  # 5
	BaseImage = "Button_Orange"

	def Setup(self):
		return

	def DoAction(self, inputValue):
		return inputValue * 10

	def ToString(self):
		return ">>"

class Insert(Operation):#6
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

class Translate(Operation):#7
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

class Pow(Operation):#8
	BaseImage = "Button_Orange"

	def DoAction(self, inputValue):
		return inputValue ** 2

	def ToString(self):
		return "Pow "+str(2)

class Flip(Operation):#9
	BaseImage = "Button_Orange"

	def DoAction(self, inputValue):
		return inputValue * -1

	def ToString(self):
		return "+/- "

class Reverse(Operation):#10
	BaseImage = "Button_Orange"

	def DoAction(self, inputValue):
		if inputValue > 0:
			return int(str(inputValue)[::-1])
		else:
			return int(str(inputValue*-1)[::-1])*-1

	def ToString(self):
		return "Reverse"

class Sum(Operation):#11
	BaseImage = "Button_Orange"

	def DoAction(self, inputValue):

		return sum( map(lambda x: int(x), str(inputValue)))
		

	def ToString(self):
		return "Sum"
