import Solver.OperationSetting as OpSetting
class Operation:
	BaseImage = ""

	def __init__(self, id):
		self.OperationId = id
		self.Setting = []
		return

	def __str__(self):
		return "?"

	def GetSetting(self, index):
		if len(self.Setting) > index and index >= 0:
			return self.Setting[index].Value()
		return 0

	def SetSetting(self, index, value):
		if len(self.Setting) > index and index >= 0:
			self.Setting[index].SetValue(value)
			
		return
	
	def IsValid(self):
		return False

	def Serialize(self):
		settingList = []
		for item in self.Setting:
			settingList += [item.Serialize()]

		return {"OpType":self.OperationId, "Settings": settingList}

	def ModifySettings(self, delta):
		for setting in self.Setting:
			setting.ChangeModifyValue(delta)
		return

	def __eq__(self, other):
		return type(other) == type(self) and self.Serialize() == other.Serialize()

class ValueChangeOp(Operation):

	def DoActionOnValue(self, inputValue):

		return inputValue

	def IsValid(self):
		number = 1234
		newNumber = self.DoActionOnValue(number)
		return number != newNumber

class OpListChangeOp(Operation):

	def DoActionOnOpList(self, opList, value):

		return opList

	def IsValid(self):
		opList = []
		opList += [MakeOperation(1)]
		number = 1234

		newOpList = self.DoActionOnOpList(opList, number)
		return opList[0] != newOpList[0]

def MakeOperation(opType):
	#do not change the order of this list
	opList = [
		Operation, 
		Add,
		Multiply,
		Divide,
		BitShiftRight,
		Insert,
		Translate,
		Pow,
		Flip,
		Reverse,
		Sum,
		SwapOrder,
		Mirror,
		Modifier,
		Store]

	if opType >= 0 and opType < len(opList):
		return opList[opType](opType)

	return None

def OpDeserialization(opData):
	op = MakeOperation(opData["OpType"])
	
	settingList = opData["Settings"]
	for loop in range(len(settingList)):
		op.SetSetting(loop, settingList[loop])
		
	return op

class Add(ValueChangeOp):
	BaseImage = "Button_Black"

	def __init__(self, id):
		super().__init__(id)
		self.Setting += [OpSetting.OperationSetting()]
		return

	def DoActionOnValue(self, inputValue):

		return inputValue + self.Setting[0].Value()

	def __str__(self):
		if self.Setting[0].Value() >= 0:
			return "+"+str(self.Setting[0].Value())
		else:
			return str(self.Setting[0].Value())

class Multiply(ValueChangeOp):
	BaseImage = "Button_Black"
	
	def __init__(self, id):
		super().__init__(id)
		self.Setting += [OpSetting.OperationSetting()]
		return

	def DoActionOnValue(self, inputValue):

		return inputValue * self.Setting[0].Value()

	def __str__(self):

		return "X"+str(self.Setting[0].Value())

	def IsValid(self):
		return self.Setting[0].Value() != 0 and super().IsValid()

class Divide(ValueChangeOp):
	BaseImage = "Button_Black"
	
	def __init__(self, id):
		super().__init__(id)
		self.Setting += [OpSetting.OperationSetting()]
		return

	def DoActionOnValue(self, inputValue):
		output = inputValue / self.Setting[0].Value()
		if int(output) == output:
			return int(output)
		return output

	def __str__(self):

		return "/"+str(self.Setting[0].Value())

	def IsValid(self):
		return self.Setting[0].Value() != 0 and super().IsValid()

class BitShiftRight(ValueChangeOp):
	BaseImage = "Button_Orange"

	def DoActionOnValue(self, inputValue):
		return int(inputValue / 10)

	def __str__(self):
		return "<<"

class Insert(ValueChangeOp):
	BaseImage = "Button_Purple"
	
	def __init__(self, id):
		super().__init__(id)
		self.Setting += [OpSetting.OperationSetting()]
		return

	def DoActionOnValue(self, inputValue):
		value = self.Setting[0].Value()

		if value < 0:
			value *= -1

		return int(str(inputValue) + str(value))

	def __str__(self):
		return ""+str(self.Setting[0].Value())

class Translate(ValueChangeOp):
	BaseImage = "Button_Orange"
	
	def __init__(self, id):
		super().__init__(id)
		self.Setting += [OpSetting.OperationSetting()]
		self.Setting += [OpSetting.OperationSetting()]
		return

	def DoActionOnValue(self, inputValue):

		return int(str(inputValue).replace(str(self.Setting[0].Value()), str(self.Setting[1].Value())))
	
	def __str__(self):

		return str(self.Setting[0].Value()) + "=>" + str(self.Setting[1].Value())
	
	def IsValid(self):
		return self.Setting[0].Value() != self.Setting[1].Value()

class Pow(ValueChangeOp):
	BaseImage = "Button_Orange"
	
	def __init__(self, id):
		super().__init__(id)
		self.Setting += [OpSetting.OperationSetting()]
		return

	def DoActionOnValue(self, inputValue):
		return inputValue ** self.Setting[0].Value()

	def __str__(self):
		return "Pow "+str(self.Setting[0].Value())

	def IsValid(self):
		return self.Setting[0].Value() > 1 and super().IsValid()

class Flip(ValueChangeOp):
	BaseImage = "Button_Orange"

	def DoActionOnValue(self, inputValue):
		return inputValue * -1

	def __str__(self):
		return "+/- "

class Reverse(ValueChangeOp):
	BaseImage = "Button_Orange"

	def DoActionOnValue(self, inputValue):
		if inputValue > 0:
			return int(str(inputValue)[::-1])
		else:
			return int(str(inputValue*-1)[::-1])*-1

	def __str__(self):
		return "Reverse"

class Sum(ValueChangeOp):
	BaseImage = "Button_Orange"

	def DoActionOnValue(self, inputValue):
		isNegtive = inputValue < 0
		if isNegtive:
			inputValue *= -1

		newValue = sum( map(lambda x: int(x), str(inputValue)))

		if isNegtive:
			newValue *= -1
		return newValue
		

	def __str__(self):
		return "Sum"

class SwapOrder(ValueChangeOp):
	BaseImage = "Button_Orange"
	
	def __init__(self, id):
		super().__init__(id)
		self.Setting += [OpSetting.OperationSetting(settingType=bool)]
		return

	def DoActionOnValue(self, inputValue):
		isNegtive = inputValue < 0
		if isNegtive:
			inputValue *= -1
		
		valueStr = str(inputValue)

		if self.Setting[0].Value():
			valueStr = valueStr[1:] + valueStr[0]
		else:
			valueStr = valueStr[-1] + valueStr[:-1]

		newValue = int(valueStr)

		if isNegtive:
			newValue *= -1

		return newValue

	def __str__(self):
		text = "Shift "
		if self.Setting[0].Value():
			text += "<"
		else:
			text += ">"
		return text

class Mirror(ValueChangeOp):
	BaseImage = "Button_Orange"

	def DoActionOnValue(self, inputValue):
		isNegtive = inputValue < 0
		if isNegtive:
			inputValue *= -1
		
		valueStr = str(inputValue)

		valueList = list(valueStr)
		
		newValueList = []
		for item in valueList:
			newValueList += [item]

		valueList.reverse()
		for item in valueList:
			newValueList += [item]

		valueStr = "".join(newValueList)
		newValue = int(valueStr)

		if isNegtive:
			newValue *= -1

		return newValue

	def __str__(self):
		return "Mirror"

class Modifier(OpListChangeOp):
	BaseImage = "Button_Orange"
	
	def __init__(self, id):
		super().__init__(id)
		self.Setting += [OpSetting.OperationSetting()]
		return

	def DoActionOnOpList(self, opList, value):
		newOpList = []
		for op in opList:
			opData = op.Serialize()
			newOp = OpDeserialization(opData)

			if op != self:
				newOp.ModifySettings(self.Setting[0].Value())
				
			newOpList += [newOp]

		return newOpList
		
	def __str__(self):
		return "[+] " + str(self.Setting[0].Value())

class Store(Insert, OpListChangeOp):
	BaseImage = "Button_Purple"

	def __init__(self, id):
		super().__init__(id)
		self.HasBeenSet = False
		return

	def DoActionOnOpList(self, opList, value):
		newOpList = []
		for op in opList:
			opData = op.Serialize()
			newOp = OpDeserialization(opData)

			if op == self:
				newOp.SetSetting(0, value)
				
			newOpList += [newOp]

		return newOpList

	def SetSetting(self, index, value):
		super().SetSetting(index, value)
		self.HasBeenSet = True
		return
		
	def __str__(self):
		if self.HasBeenSet:
			text = str(self.Setting[0].Value())
		else:
			text = "Store"
		return text
