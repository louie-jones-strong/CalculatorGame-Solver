import os
import pygame

class ImageDrawer:
	RawImageCache = {}
	SizedImageCache = {}
	
	def __init__(self, imageAssetFolder):
		self.ImageAssetFolder = imageAssetFolder

		self.RawImageCache = {}
		self.SizedImageCache = {}
		return

	def GetSizedImage(self, imageName, size):
		
		sizedKey = imageName + str(size[0])+","+str(size[1])

		if sizedKey not in self.SizedImageCache:

			image = self.GetRawImage(imageName)

			x, y = image.get_size()

			if x != size[0] or y != size[1]:
				image = pygame.transform.scale(image, size)

			self.SizedImageCache[sizedKey] = image
		return self.SizedImageCache[sizedKey]

	def GetRawImage(self, imageName):
		if imageName not in self.RawImageCache:
			path = os.path.join(self.ImageAssetFolder, str(imageName) + ".png")

			if os.path.isfile(path):
				image = pygame.image.load(path)
			else:
				image = pygame.Surface((1, 1))
				image.fill([0,0,0,0])
				image.set_alpha(0)

			self.RawImageCache[imageName] = image

		return self.RawImageCache[imageName]
	
	def DrawImage(self, surface, imageName, pos, size):
		
		if imageName == None:
			return False

		sizedImage = self.GetSizedImage(imageName, size)

		surface.blit(sizedImage, pos)

		return True
