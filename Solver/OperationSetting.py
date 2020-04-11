class OperationSetting:

	def __init__(self, value=None, canModify=True, settingType=int):
		self.SettingType = settingType

		if value == None:
			self.SettingValue = 0

			if self.SettingType == int:
				self.SettingValue = 0

			elif self.SettingType == bool:
				self.SettingValue = False

			elif self.SettingType == str:
				self.SettingValue = ""
		else:
			self.SettingValue = value

			if self.SettingType == str:
				self.SettingValue = str(self.SettingValue)

		self.CanModify = canModify
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
