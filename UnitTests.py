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
			self.NumFailed += 1
			

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
		
		self.SetGroup("Add")
		op = Operations.MakeOperation(1)
		op.SetSetting(0, 1)
		self.Assert(op.DoActionOnValue(1), 2, "+1 DoActionOnValue()")
		self.Assert(op.ToString(), "+1", "+1 ToString()")

		op = Operations.MakeOperation(1)
		op.SetSetting(0, -1)
		self.Assert(op.DoActionOnValue(1), 0, "-1 DoActionOnValue()")
		self.Assert(op.ToString(), "-1", "-1 ToString()")

		self.SetGroup("Multiply")
		op = Operations.MakeOperation(2)
		op.SetSetting(0, 3)
		self.Assert(op.DoActionOnValue(1), 3, "3 DoActionOnValue()")
		self.Assert(op.ToString(), "X3", "3 ToString()")

		self.SetGroup("Divide")
		op = Operations.MakeOperation(3)
		op.SetSetting(0, 3)
		self.Assert(op.DoActionOnValue(9), 3, "3 DoActionOnValue()")
		self.Assert(op.ToString(), "/3", "3 ToString()")

		self.SetGroup("Shift")
		op = Operations.MakeOperation(4)
		self.Assert(op.DoActionOnValue(10), 1, "right DoActionOnValue()")
		self.Assert(op.ToString(), "<<", "right ToString()")

		self.SetGroup("Insert")
		op = Operations.MakeOperation(5)
		op.SetSetting(0, 12)
		self.Assert(op.DoActionOnValue(1), 112, "DoActionOnValue()")
		self.Assert(op.ToString(), "12", "ToString()")

		self.SetGroup("Translate")
		op = Operations.MakeOperation(6)
		op.SetSetting(0, 1)
		op.SetSetting(1, 2)
		self.Assert(op.DoActionOnValue(121), 222, "DoActionOnValue()")
		self.Assert(op.ToString(), "1=>2", "ToString()")

		self.SetGroup("Pow")
		op = Operations.MakeOperation(7)
		op.SetSetting(0, 2)
		self.Assert(op.DoActionOnValue(4), 16, "DoActionOnValue()")
		self.Assert(op.ToString(), "Pow 2", "ToString()")

		op = Operations.MakeOperation(7)
		op.SetSetting(0, 3)
		self.Assert(op.DoActionOnValue(4), 64, "DoActionOnValue()")
		self.Assert(op.ToString(), "Pow 3", "ToString()")

		self.SetGroup("Flip")
		op = Operations.MakeOperation(8)
		self.Assert(op.DoActionOnValue(1), -1, "DoActionOnValue()")
		self.Assert(op.ToString(), "+/- ", "ToString()")

		self.SetGroup("Reverse")
		op = Operations.MakeOperation(9)
		self.Assert(op.DoActionOnValue(1234), 4321, "DoActionOnValue()")
		self.Assert(op.ToString(), "Reverse", "ToString()")

		self.SetGroup("Sum")
		op = Operations.MakeOperation(10)
		self.Assert(op.DoActionOnValue(1234), 10, "DoActionOnValue()")
		self.Assert(op.ToString(), "Sum", "ToString()")

		self.SetGroup("SwapOrder")
		op = Operations.MakeOperation(11)
		op.SetSetting(0, True)
		self.Assert(op.DoActionOnValue(122), 221, "DoActionOnValue()")
		self.Assert(op.ToString(), "Shift <", "ToString()")

		op = Operations.MakeOperation(11)
		op.SetSetting(0, False)
		self.Assert(op.DoActionOnValue(122), 212, "DoActionOnValue()")
		self.Assert(op.ToString(), "Shift >", "ToString()")

		self.SetGroup("Mirror")
		op = Operations.MakeOperation(12)
		self.Assert(op.DoActionOnValue(12), 1221, "DoActionOnValue()")
		self.Assert(op.ToString(), "Mirror", "ToString()")
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
		for opData in operationsData:
			operationsList += [Operations.OpDeserialization(opData)]

		found, solveOrder = GameSolver.Solve(moves, operationsList, startingNum, goal)
		self.Assert(found, True, "Found Solve")
		self.Assert(len(solveOrder) <= moves, True, "number of moves are valid")
		self.Assert(key == str(levelData["Level"]), True, "key == level")
		return

if __name__ == "__main__":
	UnitTests()
