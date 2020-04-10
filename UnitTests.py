import Solver.GameSolver as GameSolver
import Solver.Operations as Operations
import json
import os
import traceback

class UnitTests:

	def __init__(self):
		self.NumFailed = 0
		self.TestNumber = 1
		self.GroupText = ""
		self.GroupStart = 1
		self.GroupPassed = True
		self.GroupName = ""

		try:
			self.TestOperations()
			self.TestSolves()

		except Exception as e:
			self.AssertEqual(False, True, "working code")
			self.SetGroup("test: "+str(self.TestNumber)+")")
			
			strTrace = traceback.format_exc()

			print(strTrace)
			

		self.SetGroup("Done")

		print("")
		print("Number Of Tests Failed: "+str(self.NumFailed))
		if self.NumFailed > 0:
			exit(code=1)
		return

	def SetGroup(self, groupName):

		if len(self.GroupText) > 0:
			text = str(self.GroupStart)+"-"+str(self.TestNumber-1)+") "

			if self.GroupPassed:
				text += "Passed "+str(self.GroupName)
				print(text)
			else:
				text += "Failed "+str(self.GroupName)
				print(text)
				print(self.GroupText)


		self.GroupText = ""
		self.GroupStart = self.TestNumber
		self.GroupName = groupName
		self.GroupPassed = True
		return

	def AssertEqual(self, value, expectedValue, testName=""):
		self.GroupText += "\t"+str(self.TestNumber) + ") "

		if value == expectedValue:
			self.GroupText += "Passed " + str(testName) + "\n"
		else:
			self.GroupPassed = False
			self.NumFailed += 1
			self.GroupText += "Failed " + str(testName) + "\n"
			self.GroupText += "\t\texpected: " + str(expectedValue) + " but got " + str(value) + "\n"

		self.TestNumber += 1
		return value == expectedValue

	def TestOperations(self):
		self.SetGroup("Base Operation")
		op = Operations.MakeOperation(0)
		self.AssertEqual(type(op), Operations.Operation, "op Type Check")
		self.AssertEqual(op.OperationId, 0, "ID Check")

		self.SetGroup("Add")
		op = self.SharedOpTests(1, Operations.Add, "+1", [1])
		self.AssertEqual(op.DoActionOnValue(1), 2, "+1 DoActionOnValue()")

		op = self.SharedOpTests(1, Operations.Add, "-1", [-1])
		self.AssertEqual(op.DoActionOnValue(1), 0, "-1 DoActionOnValue()")

		self.SetGroup("Multiply")
		op = self.SharedOpTests(2, Operations.Multiply, "X3", [3])
		self.AssertEqual(op.DoActionOnValue(1), 3, "3 DoActionOnValue()")

		self.SetGroup("Divide")
		op = self.SharedOpTests(3, Operations.Divide, "/3", [3])
		self.AssertEqual(op.DoActionOnValue(9), 3, "3 DoActionOnValue()")

		self.SetGroup("Shift")
		op = self.SharedOpTests(4, Operations.BitShiftRight, "<<")
		self.AssertEqual(op.DoActionOnValue(10), 1, "right DoActionOnValue()")

		self.SetGroup("Insert")
		op = self.SharedOpTests(5, Operations.Insert, "12", [12])
		self.AssertEqual(op.DoActionOnValue(1), 112, "DoActionOnValue()")

		self.SetGroup("Translate")
		op = self.SharedOpTests(6, Operations.Translate, "1=>2", [1, 2])
		self.AssertEqual(op.DoActionOnValue(121), 222, "DoActionOnValue()")

		self.SetGroup("Pow")
		op = self.SharedOpTests(7, Operations.Pow, "Pow 2", [2])
		self.AssertEqual(op.DoActionOnValue(4), 16, "DoActionOnValue()")

		op = self.SharedOpTests(7, Operations.Pow, "Pow 3", [3])
		self.AssertEqual(op.DoActionOnValue(4), 64, "DoActionOnValue()")

		self.SetGroup("Flip")
		op = self.SharedOpTests(8, Operations.Flip, "+/-")
		self.AssertEqual(op.DoActionOnValue(1), -1, "DoActionOnValue()")


		self.SetGroup("Reverse")
		op = self.SharedOpTests(9, Operations.Reverse, "Reverse")
		self.AssertEqual(op.DoActionOnValue(1234), 4321, "DoActionOnValue()")
		
		self.SetGroup("Sum")
		op = self.SharedOpTests(10, Operations.Sum, "Sum")
		self.AssertEqual(op.DoActionOnValue(1234), 10, "DoActionOnValue()")

		self.SetGroup("SwapOrder")
		op = self.SharedOpTests(11, Operations.SwapOrder, "Shift <", [True])
		self.AssertEqual(op.DoActionOnValue(122), 221, "DoActionOnValue()")
		op = self.SharedOpTests(11, Operations.SwapOrder, "Shift >", [False])
		self.AssertEqual(op.DoActionOnValue(122), 212, "DoActionOnValue()")

		self.SetGroup("Mirror")
		op = self.SharedOpTests(12, Operations.Mirror, "Mirror")
		self.AssertEqual(op.DoActionOnValue(12), 1221, "DoActionOnValue()")

		self.SetGroup("Modifier")
		op = self.SharedOpTests(13, Operations.Modifier, "[+] 1", [1])
		testOpList = [op]
		exceptedOpList = [op]

		addOp = Operations.MakeOperation(1)
		testOpList += [addOp]

		addOp = Operations.MakeOperation(1)
		addOp.SetSetting(0, 1)
		exceptedOpList += [addOp]

		newOpList = op.DoActionOnOpList(testOpList, 123)
		self.AssertEqual(newOpList, exceptedOpList, "DoActionOnOpList()")

		self.SetGroup("Store")
		op = self.SharedOpTests(14, Operations.Store, "Store")

		testOpList = [op]
		storeOp = Operations.MakeOperation(14)
		storeOp.SetSetting(0, 123)
		exceptedOpList = [storeOp]


		addOp = Operations.MakeOperation(1)
		testOpList += [addOp]
		exceptedOpList += [addOp]

		newOpList = op.DoActionOnOpList(testOpList, 123)
		self.AssertEqual(newOpList, exceptedOpList, "DoActionOnOpList()")
		self.AssertEqual(str(storeOp), "123", "ToString()")
		return

	def SharedOpTests(self, opId, exceptedType, exceptedString, settingList=None):
		op = Operations.MakeOperation(opId)
		self.AssertEqual(type(op), exceptedType, "op Type Check")
		self.AssertEqual(op.OperationId, opId, "ID Check")

		if settingList != None:
			for index in range(len(settingList)):
				op.SetSetting(index, settingList[index])

		self.AssertEqual(op.IsValid(), True, "IsVaild()")
		self.AssertEqual(str(op), exceptedString, "str()")

		return op

	def TestSolves(self):
		
		self.SetGroup("Loading Level Data")

		path = os.getcwd()
		path = os.path.join(path, "Assets", "Data")
		levelDataPath = os.path.join(path, "LevelData.json")
		file = open(levelDataPath, "r")
		levelDataDict = json.load(file)
		file.close()

		self.AssertEqual(0 in levelDataDict, False, "level 0 should not be in level data")

		for loop in range(1, len(levelDataDict)+1):

			key = str(loop)

			self.SetGroup("Regression Testing Level: "+str(key))
			if self.AssertEqual(key in levelDataDict, True, "level key in level data"):
				value = levelDataDict[key]
				self.CheckLevelData(key, value)
		return

	def CheckLevelData(self, key, levelData):
		level = levelData["Level"]
		startingNum = levelData["StartingNumber"] 
		goal = levelData["Goal"] 
		moves = levelData["Moves"]

		operationsData = levelData["Operations"]

		self.AssertEqual(key == str(levelData["Level"]), True, "key == level")

		operationsList = []
		loop = 0
		for opData in operationsData:
			op = Operations.OpDeserialization(opData)

			if type(op) != Operations.Operation:
				self.AssertEqual(op.IsValid(), True, "op[" + str(loop) + "] isVaild")

			operationsList += [op]
			loop += 1

		self.AssertEqual(len(operationsList) <= 5, True, "length of operationsList is smaller or equal to 5")

		found, solveOrder = GameSolver.Solve(moves, operationsList, startingNum, goal)
		self.AssertEqual(found, True, "Found Solve")
		self.AssertEqual(len(solveOrder) <= moves, True, "number of moves are valid")
		return

if __name__ == "__main__":
	UnitTests()
