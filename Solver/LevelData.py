import Solver.Operations as Operations

class LevelData:

	Version = "1"

	def __init__(self):	
		self.Level = 0
		self.Moves = 0
		self.Goal = 0
		self.StartingNum = 0
		self.OpList = []
		for loop in range(5):
			self.OpList += [Operations.MakeOperation(0)]
		return

	def DataMigrator(self, data):
		if "Version" not in data:
			data["Version"] = "1"


		return data

	def Serialize(self):
		dataDict = {}
		dataDict["Version"] = self.Version
		dataDict["Level"] = self.Level
		dataDict["Moves"] = self.Moves
		dataDict["Goal"] = self.Goal
		dataDict["StartingNumber"] = self.StartingNum

		operationsData = []
		for op in self.OpList:
			operationsData += [op.Serialize()]

		dataDict["Operations"] = operationsData

		return dataDict

	def Deserialize(self, dataDict):
		neededMigration = False

		if "Version" not in dataDict or dataDict["Version"] != self.Version:
			dataDict = self.DataMigrator(dataDict)
			neededMigration = True

		self.Level = dataDict["Level"]
		self.Moves = dataDict["Moves"]
		self.Goal = dataDict["Goal"]
		self.StartingNum = dataDict["StartingNumber"]

		self.OpList = []
		operationsData = dataDict["Operations"]
		for opData in operationsData:
			self.OpList += [Operations.OpDeserialization(opData)]
		
		return neededMigration

	def IsValid(self):
		numValidOps = 0
		for op in self.OpList:
			if op.IsValid():
				numValidOps += 1
		
		return self.Moves > 0 and self.Goal != self.StartingNum and numValidOps > 0

	def Copy(self):
		newLevelData = LevelData()
		
		dataDict = self.Serialize()
		newLevelData.Deserialize(dataDict)
		return newLevelData
