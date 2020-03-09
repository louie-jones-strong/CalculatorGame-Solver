class Operation:
	BaseImage = ""

	def __init__(self):

		return

	def Setup(self):

		return

	def DoAction(self, inputValue):

		return inputValue

	def ToString(self):

		return "?"

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

	def __init__(self):
		self.AddAmount = 1
		return

	def Setup(self, addAmount=None):
		if addAmount == None:
			addAmount = int(input("Add Value: "))

		self.AddAmount = addAmount
		return

	def DoAction(self, inputValue):

		return inputValue + self.AddAmount

	def ToString(self):
		if self.AddAmount >= 0:
			return "+"+str(self.AddAmount)
		else:
			return str(self.AddAmount)

class Multiply(Operation):#2
	BaseImage = "Button_Black"
	
	def __init__(self):
		self.MultiplyAmount = 1
		return

	def Setup(self, multiplyAmount=None):

		if multiplyAmount == None:
			multiplyAmount = int(input("multiply Value: "))

		self.MultiplyAmount = multiplyAmount
		return

	def DoAction(self, inputValue):

		return inputValue * self.MultiplyAmount

	def ToString(self):

		return "X"+str(self.MultiplyAmount)

class Divide(Operation):#3
	BaseImage = "Button_Black"

	def __init__(self):
		self.DivideAmount = 1
		return

	def Setup(self, divideAmount=None):
		if divideAmount == None:
			divideAmount = int(input("Divide Value: "))

		self.DivideAmount = divideAmount
		return

	def DoAction(self, inputValue):
		output = inputValue / self.DivideAmount
		if int(output) == output:
			return int(output)
		return output

	def ToString(self):

		return "/"+str(self.DivideAmount)


class ShiftRight(Operation):  # 4
	BaseImage = "Button_Orange"

	def __init__(self):
		return

	def Setup(self):
		return

	def DoAction(self, inputValue):
		return int(inputValue / 10)

	def ToString(self):
		return "<<"

class ShiftLeft(Operation):  # 5
	BaseImage = "Button_Orange"

	def __init__(self):
		return

	def Setup(self):
		return

	def DoAction(self, inputValue):
		return inputValue * 10

	def ToString(self):
		return ">>"

class Insert(Operation):#6
	BaseImage = "Button_Purple"

	def __init__(self):
		self.InsertNumber = 1
		return

	def Setup(self, insertNumber=None):
		if insertNumber == None:
			insertNumber = int(input("Insert Number: "))
		self.InsertNumber = insertNumber
		return

	def DoAction(self, inputValue):
		return int(str(inputValue) + str(self.InsertNumber))

	def ToString(self):
		return "Insert "+str(self.InsertNumber)

class Translate(Operation):#7
	BaseImage = "Button_Orange"

	def __init__(self):
		self.From = 1
		self.To = 1
		return

	def Setup(self, fromNum=None, toNum=None):

		if fromNum == None:
			fromNum = int(input("From: "))

		if toNum == None:
			toNum = int(input("To: "))

		self.From = fromNum
		self.To = toNum
		return

	def DoAction(self, inputValue):

		return int(str(inputValue).replace(str(self.From), str(self.To)))
	
	def ToString(self):

		return str(self.From) + "=>" + str(self.To)

class Pow(Operation):#8
	BaseImage = "Button_Orange"

	def __init__(self):
		self.PowNumber = 2
		return

	def Setup(self):
		self.PowNumber = 2#int(input("pow Number: "))
		return

	def DoAction(self, inputValue):
		return inputValue ** self.PowNumber

	def ToString(self):
		return "Pow "+str(self.PowNumber)

class Flip(Operation):#9
	BaseImage = "Button_Orange"

	def Setup(self):
		return

	def DoAction(self, inputValue):
		return inputValue * -1

	def ToString(self):
		return "+/- "

class Reverse(Operation):#10
	BaseImage = "Button_Orange"

	def Setup(self):
		return

	def DoAction(self, inputValue):
		if inputValue > 0:
			return int(str(inputValue)[::-1])
		else:
			return int(str(inputValue*-1)[::-1])*-1

	def ToString(self):
		return "Reverse"

class Sum(Operation):#11
	BaseImage = "Button_Orange"
	
	def Setup(self):
		return

	def DoAction(self, inputValue):

		return sum( map(lambda x: int(x), str(inputValue)))
		

	def ToString(self):
		return "Sum"
