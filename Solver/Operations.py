class OperationSettings:

	def __init__(self, value=None, canModify=True, settingType=int):
		if value == None:
			if settingType == int:
				self.SettingValue = 0
			elif settingType == bool:
				self.SettingValue = False
		else:
			self.SettingValue = value

		self.CanModify = canModify
		self.SettingType = settingType
		return

	def Value(self):

		return self.SettingValue

	def SetValue(self, value):
		self.SettingValue = value
		return

	def Serialize(self):
		return self.SettingValue

	def ChangeModifyValue(self, value):
		if self.CanModify:
			self.SettingValue += value
		return

class Operation:
	BaseImage = ""
	Setting = []
	OperationId = 0

	def __init__(self, id):
		self.OperationId = id
		self.Setting = []
		return

	def DoActionOnValue(self, inputValue):

		return inputValue

	def DoActionOnOpList(self, opList):

		return opList

	def ToString(self):

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
		number = 1234
		newNumber = self.DoActionOnValue(number)
		if number != newNumber:
			return True

		opList = []
		opList += [MakeOperation(1)]
		
		newOpList = self.DoActionOnOpList(opList)
		return opList[0].Setting[0].Value() != newOpList[0].Setting[0].Value()

	def Serialize(self):
		settingList = []
		for item in self.Setting:
			settingList += [item.Serialize()]

		return {"OpType":self.OperationId, "Settings": settingList}

	def ModifySettings(self, delta):
		for setting in self.Setting:
			setting.ChangeModifyValue(delta)
		return

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
		Modifier]

	if opType >= 0 and opType < len(opList):
		return opList[opType](opType)

	return None


def OpDeserialization(opData):
	op = MakeOperation(opData["OpType"])
	
	settingList = opData["Settings"]
	for loop in range(len(settingList)):
		op.SetSetting(loop, settingList[loop])
		
	return op

class Add(Operation):
	BaseImage = "Button_Black"

	def __init__(self, id):
		super().__init__(id)
		self.Setting += [OperationSettings()]
		return

	def DoActionOnValue(self, inputValue):

		return inputValue + self.Setting[0].Value()

	def ToString(self):
		if self.Setting[0].Value() >= 0:
			return "+"+str(self.Setting[0].Value())
		else:
			return str(self.Setting[0].Value())

class Multiply(Operation):
	BaseImage = "Button_Black"
	
	def __init__(self, id):
		super().__init__(id)
		self.Setting += [OperationSettings()]
		return

	def DoActionOnValue(self, inputValue):

		return inputValue * self.Setting[0].Value()

	def ToString(self):

		return "X"+str(self.Setting[0].Value())

	def IsValid(self):
		return self.Setting[0].Value() != 0 and super().IsValid()

class Divide(Operation):
	BaseImage = "Button_Black"
	
	def __init__(self, id):
		super().__init__(id)
		self.Setting += [OperationSettings()]
		return

	def DoActionOnValue(self, inputValue):
		output = inputValue / self.Setting[0].Value()
		if int(output) == output:
			return int(output)
		return output

	def ToString(self):

		return "/"+str(self.Setting[0].Value())

	def IsValid(self):
		return self.Setting[0].Value() != 0 and super().IsValid()

class BitShiftRight(Operation):
	BaseImage = "Button_Orange"

	def DoActionOnValue(self, inputValue):
		return int(inputValue / 10)

	def ToString(self):
		return "<<"

class Insert(Operation):
	BaseImage = "Button_Purple"
	
	def __init__(self, id):
		super().__init__(id)
		self.Setting += [OperationSettings()]
		return

	def DoActionOnValue(self, inputValue):
		return int(str(inputValue) + str(self.Setting[0].Value()))

	def ToString(self):
		return ""+str(self.Setting[0].Value())

class Translate(Operation):
	BaseImage = "Button_Orange"
	
	def __init__(self, id):
		super().__init__(id)
		self.Setting += [OperationSettings()]
		self.Setting += [OperationSettings()]
		return

	def DoActionOnValue(self, inputValue):

		return int(str(inputValue).replace(str(self.Setting[0].Value()), str(self.Setting[1].Value())))
	
	def ToString(self):

		return str(self.Setting[0].Value()) + "=>" + str(self.Setting[1].Value())
	
	def IsValid(self):
		return self.Setting[0].Value() != self.Setting[1].Value()

class Pow(Operation):
	BaseImage = "Button_Orange"
	
	def __init__(self, id):
		super().__init__(id)
		self.Setting += [OperationSettings()]
		return

	def DoActionOnValue(self, inputValue):
		return inputValue ** self.Setting[0].Value()

	def ToString(self):
		return "Pow "+str(self.Setting[0].Value())

	def IsValid(self):
		return self.Setting[0].Value() > 1 and super().IsValid()

class Flip(Operation):
	BaseImage = "Button_Orange"

	def DoActionOnValue(self, inputValue):
		return inputValue * -1

	def ToString(self):
		return "+/- "

class Reverse(Operation):
	BaseImage = "Button_Orange"

	def DoActionOnValue(self, inputValue):
		if inputValue > 0:
			return int(str(inputValue)[::-1])
		else:
			return int(str(inputValue*-1)[::-1])*-1

	def ToString(self):
		return "Reverse"

class Sum(Operation):
	BaseImage = "Button_Orange"

	def DoActionOnValue(self, inputValue):
		isNegtive = inputValue < 0
		if isNegtive:
			inputValue *= -1

		newValue = sum( map(lambda x: int(x), str(inputValue)))

		if isNegtive:
			newValue *= -1
		return newValue
		

	def ToString(self):
		return "Sum"

class SwapOrder(Operation):
	BaseImage = "Button_Orange"
	
	def __init__(self, id):
		super().__init__(id)
		self.Setting += [OperationSettings(settingType=bool)]
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

	def ToString(self):
		text = "Shift "
		if self.Setting[0].Value():
			text += "<"
		else:
			text += ">"
		return text

class Mirror(Operation):
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

	def ToString(self):
		return "Mirror"

class Modifier(Operation):
	BaseImage = "Button_Orange"
	
	def __init__(self, id):
		super().__init__(id)
		self.Setting += [OperationSettings()]
		return

	def DoActionOnOpList(self, opList):
		newOpList = []
		for op in opList:
			if op != self:
				opData = op.Serialize()
				newOp = OpDeserialization(opData)
				newOp.ModifySettings(self.Setting[0].Value())
				newOpList += [newOp]

		return newOpList
		
	def ToString(self):
		return "[+] " + str(self.Setting[0].Value())

