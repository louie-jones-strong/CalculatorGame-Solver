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
			self.Assert(False, True, "working code")
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

	def Assert(self, value, expectedValue, testName=""):
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
		self.Assert(type(op), Operations.Operation, "op Type Check")
		self.Assert(op.OperationId, 0, "ID Check")

		self.SetGroup("Add")
		op = Operations.MakeOperation(1)
		self.Assert(type(op), Operations.Add, "op Type Check")
		self.Assert(op.OperationId, 1, "ID Check")
		op.SetSetting(0, 1)
		self.Assert(op.DoActionOnValue(1), 2, "+1 DoActionOnValue()")
		self.Assert(op.ToString(), "+1", "+1 ToString()")
		self.Assert(op.IsValid(), True, "IsVaild()")

		op = Operations.MakeOperation(1)
		op.SetSetting(0, -1)
		self.Assert(op.DoActionOnValue(1), 0, "-1 DoActionOnValue()")
		self.Assert(op.ToString(), "-1", "-1 ToString()")
		self.Assert(op.IsValid(), True, "IsVaild()")

		self.SetGroup("Multiply")
		op = Operations.MakeOperation(2)
		self.Assert(type(op), Operations.Multiply, "op Type Check")
		self.Assert(op.OperationId, 2, "ID Check")
		op.SetSetting(0, 3)
		self.Assert(op.DoActionOnValue(1), 3, "3 DoActionOnValue()")
		self.Assert(op.ToString(), "X3", "3 ToString()")
		self.Assert(op.IsValid(), True, "IsVaild()")

		self.SetGroup("Divide")
		op = Operations.MakeOperation(3)
		self.Assert(type(op), Operations.Divide, "op Type Check")
		self.Assert(op.OperationId, 3, "ID Check")
		op.SetSetting(0, 3)
		self.Assert(op.DoActionOnValue(9), 3, "3 DoActionOnValue()")
		self.Assert(op.ToString(), "/3", "3 ToString()")
		self.Assert(op.IsValid(), True, "IsVaild()")

		self.SetGroup("Shift")
		op = Operations.MakeOperation(4)
		self.Assert(type(op), Operations.BitShiftRight, "op Type Check")
		self.Assert(op.OperationId, 4, "ID Check")
		self.Assert(op.DoActionOnValue(10), 1, "right DoActionOnValue()")
		self.Assert(op.ToString(), "<<", "right ToString()")
		self.Assert(op.IsValid(), True, "IsVaild()")

		self.SetGroup("Insert")
		op = Operations.MakeOperation(5)
		self.Assert(type(op), Operations.Insert, "op Type Check")
		self.Assert(op.OperationId, 5, "ID Check")
		op.SetSetting(0, 12)
		self.Assert(op.DoActionOnValue(1), 112, "DoActionOnValue()")
		self.Assert(op.ToString(), "12", "ToString()")
		self.Assert(op.IsValid(), True, "IsVaild()")

		self.SetGroup("Translate")
		op = Operations.MakeOperation(6)
		self.Assert(type(op), Operations.Translate, "op Type Check")
		self.Assert(op.OperationId, 6, "ID Check")
		op.SetSetting(0, 1)
		op.SetSetting(1, 2)
		self.Assert(op.DoActionOnValue(121), 222, "DoActionOnValue()")
		self.Assert(op.ToString(), "1=>2", "ToString()")
		self.Assert(op.IsValid(), True, "IsVaild()")

		self.SetGroup("Pow")
		op = Operations.MakeOperation(7)
		self.Assert(type(op), Operations.Pow, "op Type Check")
		self.Assert(op.OperationId, 7, "ID Check")
		op.SetSetting(0, 2)
		self.Assert(op.DoActionOnValue(4), 16, "DoActionOnValue()")
		self.Assert(op.ToString(), "Pow 2", "ToString()")
		self.Assert(op.IsValid(), True, "IsVaild()")

		op = Operations.MakeOperation(7)
		op.SetSetting(0, 3)
		self.Assert(op.DoActionOnValue(4), 64, "DoActionOnValue()")
		self.Assert(op.ToString(), "Pow 3", "ToString()")
		self.Assert(op.IsValid(), True, "IsVaild()")

		self.SetGroup("Flip")
		op = Operations.MakeOperation(8)
		self.Assert(type(op), Operations.Flip, "op Type Check")
		self.Assert(op.OperationId, 8, "ID Check")
		self.Assert(op.DoActionOnValue(1), -1, "DoActionOnValue()")
		self.Assert(op.ToString(), "+/- ", "ToString()")
		self.Assert(op.IsValid(), True, "IsVaild()")

		self.SetGroup("Reverse")
		op = Operations.MakeOperation(9)
		self.Assert(type(op), Operations.Reverse, "op Type Check")
		self.Assert(op.OperationId, 9, "ID Check")
		self.Assert(op.DoActionOnValue(1234), 4321, "DoActionOnValue()")
		self.Assert(op.ToString(), "Reverse", "ToString()")
		self.Assert(op.IsValid(), True, "IsVaild()")

		self.SetGroup("Sum")
		op = Operations.MakeOperation(10)
		self.Assert(type(op), Operations.Sum, "op Type Check")
		self.Assert(op.OperationId, 10, "ID Check")
		self.Assert(op.DoActionOnValue(1234), 10, "DoActionOnValue()")
		self.Assert(op.ToString(), "Sum", "ToString()")
		self.Assert(op.IsValid(), True, "IsVaild()")

		self.SetGroup("SwapOrder")
		op = Operations.MakeOperation(11)
		self.Assert(type(op), Operations.SwapOrder, "op Type Check")
		self.Assert(op.OperationId, 11, "ID Check")
		op.SetSetting(0, True)
		self.Assert(op.DoActionOnValue(122), 221, "DoActionOnValue()")
		self.Assert(op.ToString(), "Shift <", "ToString()")
		self.Assert(op.IsValid(), True, "IsVaild()")

		op = Operations.MakeOperation(11)
		op.SetSetting(0, False)
		self.Assert(op.DoActionOnValue(122), 212, "DoActionOnValue()")
		self.Assert(op.ToString(), "Shift >", "ToString()")
		self.Assert(op.IsValid(), True, "IsVaild()")

		self.SetGroup("Mirror")
		op = Operations.MakeOperation(12)
		self.Assert(type(op), Operations.Mirror, "op Type Check")
		self.Assert(op.OperationId, 12, "ID Check")
		self.Assert(op.DoActionOnValue(12), 1221, "DoActionOnValue()")
		self.Assert(op.ToString(), "Mirror", "ToString()")
		self.Assert(op.IsValid(), True, "IsVaild()")

		self.SetGroup("Modifier")
		op = Operations.MakeOperation(13)
		self.Assert(type(op), Operations.Modifier, "op Type Check")
		self.Assert(op.OperationId, 13, "ID Check")
		op.SetSetting(0, 1)
		self.Assert(op.DoActionOnValue(12), 12, "DoActionOnValue()")
		self.Assert(op.ToString(), "[+] 1", "ToString()")
		self.Assert(op.IsValid(), True, "IsVaild()")
		return

	def TestSolves(self):
		
		self.SetGroup("Loading Level Data")

		path = os.getcwd()
		path = os.path.join(path, "Assets", "Data")
		levelDataPath = os.path.join(path, "LevelData.json")
		file = open(levelDataPath, "r")
		levelDataDict = json.load(file)
		file.close()

		for key, value in levelDataDict.items():
			self.CheckLevelData(value, key)
		return

	def CheckLevelData(self, levelData, key):
		level = levelData["Level"]

		self.SetGroup("Regression Testing Level: "+str(level))

		level = levelData["Level"] 
		startingNum = levelData["StartingNumber"] 
		goal = levelData["Goal"] 
		moves = levelData["Moves"]

		operationsData = levelData["Operations"]

		operationsList = []
		loop = 0
		for opData in operationsData:
			op = Operations.OpDeserialization(opData)
			if type(op) != Operations.Operation:
				self.Assert(op.IsValid(), True, "op[" + str(loop) + "] isVaild")
			operationsList += [op]
			loop += 1

		found, solveOrder = GameSolver.Solve(moves, operationsList, startingNum, goal)
		self.Assert(found, True, "Found Solve")
		self.Assert(len(solveOrder) <= moves, True, "number of moves are valid")
		self.Assert(key == str(levelData["Level"]), True, "key == level")
		return

if __name__ == "__main__":
	UnitTests()
