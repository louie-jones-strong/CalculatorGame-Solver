class Operation:
	def DoAction(self, inputValue):

		return inputValue

	def ToString(self):

		return

class Add(Operation):
	def __init__(self, addAmount=None):
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

class Multiply(Operation):
	def __init__(self, multiplyAmount=None):

		if multiplyAmount == None:
			multiplyAmount = int(input("multiply Value: "))

		self.MultiplyAmount = multiplyAmount
		return

	def DoAction(self, inputValue):

		return inputValue * self.MultiplyAmount

	def ToString(self):

		return "X"+str(self.MultiplyAmount)

class Divide(Operation):
	def __init__(self, divideAmount=None):
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

class Shift(Operation):
	def __init__(self, isRightShift=None):
		if isRightShift == None:
			isRightShift = int(input("<<[1] >>[2]: ")) == 1
		self.IsRightShift = isRightShift
		return

	def DoAction(self, inputValue):
		if self.IsRightShift:
			return int(inputValue / 10)
		else:
			return inputValue * 10

	def ToString(self):
		if self.IsRightShift:
			return "<<"
		else:
			return ">>"

class Insert(Operation):
	def __init__(self, insertNumber=None):
		if insertNumber == None:
			insertNumber = int(input("Insert Number: "))
		self.InsertNumber = insertNumber
		return

	def DoAction(self, inputValue):
		return int(str(inputValue) + str(self.InsertNumber))

	def ToString(self):
		return "Insert "+str(self.InsertNumber)

class Translate(Operation):

	def __init__(self, fromNum=None, toNum=None):

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
