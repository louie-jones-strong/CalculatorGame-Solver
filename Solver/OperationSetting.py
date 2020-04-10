class OperationSetting:

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
			if self.SettingValue < 0:
				self.SettingValue -= value
			else:
				self.SettingValue += value
		return
