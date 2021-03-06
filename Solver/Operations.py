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

	def SetSetting(self, index, value, overrideTemp=False):
		if len(self.Setting) > index and index >= 0:
			if not self.Setting[index].IsTempValue or overrideTemp:
				self.Setting[index].SetValue(value)
			
		return
	
	def IsValid(self):
		isVaild = True
		for item in self.Setting:
			valueType = type(item.Value())

			if valueType != item.SettingType:
				isVaild = False

		return isVaild

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

	def MakeCopy(self):
		newOp = MakeOperation(self.OperationId)

		for loop in range(len(self.Setting)):
			newOp.SetSetting(loop, self.Setting[loop].Value(), True)

		return newOp

class ValueChangeOp(Operation):

	def DoActionOnValue(self, inputValue):

		return inputValue

	def IsValid(self, checkValueChange=True):
		if checkValueChange:
			number = 1234
			newNumber = self.DoActionOnValue(number)
			return number != newNumber and super().IsValid()
		else:
			return super().IsValid()

class OpListChangeOp(Operation):

	def DoActionOnOpList(self, opList, value):

		return opList

	def IsValid(self):
		opList = []
		opList += [MakeOperation(1)]
		number = 1234

		newOpList = self.DoActionOnOpList(opList, number)
		return opList[0] != newOpList[0] and super().IsValid()

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
		SwapLeftOrder,
		SwapRightOrder,
		Mirror,
		Modifier,
		Store,
		Inv10]

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
		if int(inputValue) != inputValue:
			return inputValue

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
		self.Setting += [OpSetting.OperationSetting(settingType=str)]
		self.Setting += [OpSetting.OperationSetting(settingType=str)]
		return

	def DoActionOnValue(self, inputValue):

		return int(str(inputValue).replace(str(self.Setting[0].Value()), str(self.Setting[1].Value())))
	
	def __str__(self):

		return str(self.Setting[0].Value()) + "=>" + str(self.Setting[1].Value())
	
	def IsValid(self):
		return (super().IsValid(False) and self.Setting[0].Value() != self.Setting[1].Value() and 
			len(self.Setting[0].Value()) > 0 and len(self.Setting[1].Value()) > 0)

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
		return "+/-"

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

class SwapLeftOrder(ValueChangeOp):
	BaseImage = "Button_Orange"
	
	def __init__(self, id):
		super().__init__(id)
		return

	def DoActionOnValue(self, inputValue):
		isNegtive = inputValue < 0
		if isNegtive:
			inputValue *= -1
		
		valueStr = str(inputValue)

		valueStr = valueStr[1:] + valueStr[0]

		newValue = int(valueStr)

		if isNegtive:
			newValue *= -1

		return newValue

	def __str__(self):
		return "Shift <"

class SwapRightOrder(ValueChangeOp):
	BaseImage = "Button_Orange"
	
	def __init__(self, id):
		super().__init__(id)
		return

	def DoActionOnValue(self, inputValue):
		isNegtive = inputValue < 0
		if isNegtive:
			inputValue *= -1
		
		valueStr = str(inputValue)

		valueStr = valueStr[-1] + valueStr[:-1]

		newValue = int(valueStr)

		if isNegtive:
			newValue *= -1

		return newValue

	def __str__(self):
		return "Shift >"

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
			newOp = op.MakeCopy()

			if op != self:
				newOp.ModifySettings(self.Setting[0].Value())
				
			newOpList += [newOp]

		return newOpList
		
	def __str__(self):
		return "[+] " + str(self.Setting[0].Value())

class Store(ValueChangeOp, OpListChangeOp):
	BaseImage = "Button_Store"

	def __init__(self, id):
		super().__init__(id)
		self.Setting += [OpSetting.OperationSetting(isTempValue=True)]
		self.Setting += [OpSetting.OperationSetting(value=False, settingType=bool, isTempValue=True)]
		return

	def DoActionOnValue(self, inputValue):
		if int(inputValue) != inputValue or not self.Setting[1].Value():
			return inputValue

		value = self.Setting[0].Value()

		if value < 0:
			value *= -1

		return int(str(inputValue) + str(value))

	def DoActionOnOpList(self, opList, value):
		newOpList = []
		for op in opList:
			newOp = op.MakeCopy()

			if op == self:
				newOp.SetSetting(0, value, overrideTemp=True)
				newOp.SetSetting(1, True, overrideTemp=True)
				
			newOpList += [newOp]

		return newOpList
	
	def IsValid(self):
		return True

	def __str__(self):
		if self.Setting[1].Value():
			text = str(self.Setting[0].Value())
		else:
			text = "Store"
		return text

class Inv10(ValueChangeOp):
	BaseImage = "Button_Orange"

	def DoActionOnValue(self, inputValue):
		isNegtive = inputValue < 0
		if isNegtive:
			inputValue *= -1

		valueList = map(lambda x: int(x), str(inputValue))

		newString = ""
		for item in valueList:
			if item == 0:
				newString += "0"
			else:
				newString += str(10-item)

		newValue = int(newString)

		if isNegtive:
			newValue *= -1
		return newValue
		

	def __str__(self):
		return "Inv10"