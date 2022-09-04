import unittest

import Solver.GameSolver as GameSolver
import Solver.Operations as Operations
import Solver.LevelData as LevelData
import json
import os
import traceback

class UnitTests(unittest.TestCase):

	# def __init__(self):
	# 	self.Sovler = GameSolver.GameSolver()

	# 	return

# test each operation

	def test_Base_Operation(self):
		op = Operations.MakeOperation(0)
		self.assertEqual(type(op), Operations.Operation, "op Type Check")
		self.assertEqual(op.OperationId, 0, "ID Check")

	def test_Add(self):
		op = self.SharedOpTests(1, Operations.Add, "+1", [1])
		self.assertEqual(op.DoActionOnValue(1), 2, "+1 DoActionOnValue()")

		op = self.SharedOpTests(1, Operations.Add, "-1", [-1])
		self.assertEqual(op.DoActionOnValue(1), 0, "-1 DoActionOnValue()")

	def test_Multiply(self):
		op = self.SharedOpTests(2, Operations.Multiply, "X3", [3])
		self.assertEqual(op.DoActionOnValue(1), 3, "3 DoActionOnValue()")

	def test_Divide(self):
		op = self.SharedOpTests(3, Operations.Divide, "/3", [3])
		self.assertEqual(op.DoActionOnValue(9), 3, "3 DoActionOnValue()")

	def test_Shift(self):
		op = self.SharedOpTests(4, Operations.BitShiftRight, "<<")
		self.assertEqual(op.DoActionOnValue(10), 1, "right DoActionOnValue()")

	def test_Insert(self):
		op = self.SharedOpTests(5, Operations.Insert, "12", [12])
		self.assertEqual(op.DoActionOnValue(1), 112, "DoActionOnValue()")

	def test_Translate(self):
		op = self.SharedOpTests(6, Operations.Translate, "1=>2", ["1", "2"])
		self.assertEqual(op.DoActionOnValue(121), 222, "DoActionOnValue()")

	def test_Pow(self):
		op = self.SharedOpTests(7, Operations.Pow, "Pow 2", [2])
		self.assertEqual(op.DoActionOnValue(4), 16, "DoActionOnValue()")

		op = self.SharedOpTests(7, Operations.Pow, "Pow 3", [3])
		self.assertEqual(op.DoActionOnValue(4), 64, "DoActionOnValue()")

	def test_Flip(self):
		op = self.SharedOpTests(8, Operations.Flip, "+/-")
		self.assertEqual(op.DoActionOnValue(1), -1, "DoActionOnValue()")

	def test_Reverse(self):
		op = self.SharedOpTests(9, Operations.Reverse, "Reverse")
		self.assertEqual(op.DoActionOnValue(1234), 4321, "DoActionOnValue()")

	def test_Sum(self):
		op = self.SharedOpTests(10, Operations.Sum, "Sum")
		self.assertEqual(op.DoActionOnValue(1234), 10, "DoActionOnValue()")

	def test_SwapLeftOrder(self):
		op = self.SharedOpTests(11, Operations.SwapLeftOrder, "Shift <")
		self.assertEqual(op.DoActionOnValue(1123), 1231, "DoActionOnValue()")

	def test_SwapRightOrder(self):
		op = self.SharedOpTests(12, Operations.SwapRightOrder, "Shift >")
		self.assertEqual(op.DoActionOnValue(122), 212, "DoActionOnValue()")

	def test_Mirror(self):
		op = self.SharedOpTests(13, Operations.Mirror, "Mirror")
		self.assertEqual(op.DoActionOnValue(12), 1221, "DoActionOnValue()")

	def test_Modifier(self):
		op = self.SharedOpTests(14, Operations.Modifier, "[+] 1", [1])
		testOpList = [op]
		exceptedOpList = [op]

		addOp = Operations.MakeOperation(1)
		testOpList += [addOp]

		addOp = Operations.MakeOperation(1)
		addOp.SetSetting(0, 1)
		exceptedOpList += [addOp]

		newOpList = op.DoActionOnOpList(testOpList, 123)
		self.assertEqual(newOpList, exceptedOpList, "DoActionOnOpList()")

	def test_Store(self):
		op = self.SharedOpTests(15, Operations.Store, "Store")

		testOpList = [op]
		storeOp = Operations.MakeOperation(15)
		storeOp.SetSetting(0, 123, overrideTemp=True)
		storeOp.SetSetting(1, True, overrideTemp=True)
		exceptedOpList = [storeOp]


		addOp = Operations.MakeOperation(1)
		testOpList += [addOp]
		exceptedOpList += [addOp]

		newOpList = op.DoActionOnOpList(testOpList, 123)
		self.assertEqual(newOpList, exceptedOpList, "DoActionOnOpList()")

	def test_Inv10(self):
		op = self.SharedOpTests(16, Operations.Inv10, "Inv10")
		self.assertEqual(op.DoActionOnValue(1234567890), 9876543210, "DoActionOnValue()")

	def test_Portals(self):
		newNum = GameSolver.DoPortalMoves(100, None, None)
		self.assertEqual(newNum, 100, "DoPortalMoves(100, None, None)")

		newNum = GameSolver.DoPortalMoves(10, 1, 0)
		self.assertEqual(newNum, 1, "DoPortalMoves(10, 1, 0)")

		newNum = GameSolver.DoPortalMoves(199, 2, 0)
		self.assertEqual(newNum, 1, "DoPortalMoves(199, 2, 0)")

		newNum = GameSolver.DoPortalMoves(991, 2, 0)
		self.assertEqual(newNum, 1, "DoPortalMoves(991, 2, 0)")

		newNum = GameSolver.DoPortalMoves(946, 2, 1)
		self.assertEqual(newNum, 46, "DoPortalMoves(946, 2, 1)")

		newNum = GameSolver.DoPortalMoves(150, 2, 1)
		self.assertEqual(newNum, 60, "DoPortalMoves(150, 2, 1)")

		newNum = GameSolver.DoPortalMoves(964, 2, 1)
		self.assertEqual(newNum, 64, "DoPortalMoves(964, 2, 1)")

		newNum = GameSolver.DoPortalMoves(96, 2, 1)
		self.assertEqual(newNum, 96, "DoPortalMoves(96, 2, 1)")
		return


# checking level data
	def test_Loading_Level_Data(self):

		path = os.getcwd()
		path = os.path.join(path, "Assets", "Data")
		levelDataPath = os.path.join(path, "LevelData.json")
		file = open(levelDataPath, "r")
		levelsDataDict = json.load(file)
		file.close()

		self.assertEqual(0 in levelsDataDict, False, "level 0 should not be in level data")

		for loop in range(1, len(levelsDataDict)+1):

			key = str(loop)


			if self.assertEqual(key in levelsDataDict, True, "level key in level data"):

				levelDataDict = levelsDataDict[key]
				self.CheckLevelData(key, levelDataDict)
		return


# helpers
	def SharedOpTests(self, opId, exceptedType, exceptedString, settingList=None):
		op = Operations.MakeOperation(opId)
		self.assertEqual(type(op), exceptedType, "op Type Check")
		self.assertEqual(op.OperationId, opId, "ID Check")

		if settingList != None:
			for index in range(len(settingList)):
				op.SetSetting(index, settingList[index])

		self.assertEqual(op.IsValid(), True, "IsVaild()")
		self.assertEqual(str(op), exceptedString, "str()")

		self.TestOpSetting(op)

		return op

	def TestOpSetting(self, op):
		for loop in range(len(op.Setting)):
			item = op.Setting[loop]

			valueType = type(item.Value())
			self.assertEqual(valueType, item.SettingType, "Setting["+str(loop)+"] value type Check")
		return

	def OpListToText(self, opList):
		text = "[ "

		text += str(opList[0])

		for index in range(1, len(opList)):

			text += ", " + str(opList[index])

		text += " ]"
		return text

	def CheckLevelData(self, key, levelDataDict):
		levelData = LevelData.LevelData()
		neededMigration = levelData.Deserialize(levelDataDict)

		self.assertEqual(neededMigration, False, "LevelData Version Check")

		self.assertEqual(key == str(levelData.Level), True, "key == level")

		operationsList = []
		loop = 0
		for op in levelData.OpList:

			opType = type(op)
			if opType != Operations.Operation:
				self.TestOpSetting(op)
				self.assertEqual(op.IsValid(), True, "op[" + str(loop) + "] ("+str(opType.__name__)+") isVaild")


			operationsList += [op]
			loop += 1

		self.assertEqual(len(operationsList) <= 5, True, "length of operationsList is smaller or equal to 5")

		if levelData.PortalFrom == None or levelData.PortalTo == None:
			self.assertEqual(levelData.PortalFrom == levelData.PortalTo, True, "portals both none data Check")
		else:
			self.assertEqual(levelData.PortalFrom > levelData.PortalTo, True, "PortalFrom > PortalTo")
			self.assertEqual(levelData.PortalFrom > 0, True, "PortalFrom > 0")
			self.assertEqual(levelData.PortalFrom <= 5, True, "PortalFrom <= 5")
			self.assertEqual(levelData.PortalTo >= 0, True, "PortalTo >= 0")
			self.assertEqual(levelData.PortalTo <= 4, True, "PortalTo <= 4")

		found, solveOrder = self.Sovler.Solve(levelData)
		self.assertEqual(found, True, "Found Solve "+ self.OpListToText(operationsList))
		if found:
			self.assertEqual(len(solveOrder) > 0, True, "number of min moves")
			self.assertEqual(len(solveOrder) <= levelData.Moves, True, "number of moves are valid")
		return



if __name__ == "__main__":
	unittest.main()
