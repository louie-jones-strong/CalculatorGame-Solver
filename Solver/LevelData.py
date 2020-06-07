import Solver.Operations as Operations

class LevelData:

	Version = "1.2"

	def __init__(self):	
		self.Level = 0
		self.Moves = 0
		self.Goal = 0
		self.StartingNum = 0
		self.PortalFrom = None
		self.PortalTo = None
		self.OpList = []
		for loop in range(5):
			self.OpList += [Operations.MakeOperation(0)]
		return

	def DataMigrator(self, data):

		if "Version" not in data:
			data["Version"] = "1"

		if data["Version"] == "1":
			data["PortalFrom"] = None
			data["PortalTo"] = None
			data["Version"] = "1.1"

		if data["Version"] == "1.1":
			for op in data["Operations"]:
				if op["OpType"] == 11:
					if op["Settings"][0] == True:
						op["Settings"] = []
					else:
						op["OpType"] = 12
						op["Settings"] = []

				elif op["OpType"] > 11:
					op["OpType"] += 1

			data["Version"] = "1.2"

		return data

	def Serialize(self):
		dataDict = {}
		dataDict["Version"] = self.Version
		dataDict["Level"] = self.Level
		dataDict["Moves"] = self.Moves
		dataDict["Goal"] = self.Goal
		dataDict["StartingNumber"] = self.StartingNum
		dataDict["PortalFrom"] = self.PortalFrom
		dataDict["PortalTo"] = self.PortalTo

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
		self.PortalFrom = dataDict["PortalFrom"]
		self.PortalTo = dataDict["PortalTo"]
		
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
		
		return (self.Moves > 0 and 
			self.Goal != self.StartingNum and 
			numValidOps > 0 and
			((self.PortalFrom == None and self.PortalTo == None) or 
			self.PortalFrom > self.PortalTo))

	def Copy(self):
		newLevelData = LevelData()
		
		newLevelData.Level = self.Level
		newLevelData.Moves = self.Moves 
		newLevelData.Goal = self.Goal
		newLevelData.StartingNum = self.StartingNum
		newLevelData.PortalFrom = self.PortalFrom
		newLevelData.PortalTo = self.PortalTo

		newLevelData.OpList = []
		for op in self.OpList:
			newLevelData.OpList += [op.MakeCopy()]

		return newLevelData
