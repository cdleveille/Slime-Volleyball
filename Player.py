## Chris Leveille
## April 2019

import pygame
import math

class Player():

	# Create a new player
	def __init__(self, name, radius, speed, jump, color, inputs, message):
		
		self.x = 0
		self.y = 0
		self.xv = 0
		self.yv = 0
		self.color = color
		self.name = name
		self.radius = radius
		self.speed = speed
		self.jump = jump
		self.inputs = inputs
		self.jumpEnabled = True
		self.eyeX = self.radius / 2
		self.eyeY = self.radius * (3 / 5)
		self.pupilOffsetRatio = self.radius / 10
		self.message = message
		self.messageFont = pygame.font.Font(None, 24)

	# Update movement properties based on the keys currently being pressed
	def handleInput(self, keys):
		
		jump = self.inputs[0]
		left = self.inputs[1]
		right = self.inputs[2]

		if keys[left] and keys[right]:
			self.xv = 0
		elif keys[left]:
			self.xv = -self.speed
		elif keys[right]:
			self.xv = self.speed
		else:
			self.xv = 0
		if (self.jumpEnabled == True):
			if keys[jump]:
				self.yv = -self.jump
				self.jumpEnabled = False

	def getPupilOffset(self, ball, pupilX):
		
		(pupilShiftX, pupilShiftY) = (0, 0)
		XDiff = -(ball.x - (self.x + pupilX))
		YDiff = -(ball.y - (self.y - self.radius / 2))
		if XDiff > 0:
			if YDiff > 0:
				Angle = math.degrees(math.atan(YDiff / XDiff))
				pupilShiftX = -self.pupilOffsetRatio * math.cos(math.radians(Angle))
				pupilShiftY = -self.pupilOffsetRatio * math.sin(math.radians(Angle))
			elif YDiff < 0:
				Angle = math.degrees(math.atan(YDiff / XDiff))
				pupilShiftX = -self.pupilOffsetRatio * math.cos(math.radians(Angle))
				pupilShiftY = -self.pupilOffsetRatio * math.sin(math.radians(Angle))
		elif XDiff < 0:
			if YDiff > 0:
				Angle = 180 + math.degrees(math.atan(YDiff / XDiff))
				pupilShiftX = -self.pupilOffsetRatio * math.cos(math.radians(Angle))
				pupilShiftY = -self.pupilOffsetRatio * math.sin(math.radians(Angle))
			elif YDiff < 0:
				Angle = -180 + math.degrees(math.atan(YDiff / XDiff))
				pupilShiftX = -self.pupilOffsetRatio * math.cos(math.radians(Angle))
				pupilShiftY = -self.pupilOffsetRatio * math.sin(math.radians(Angle))
		elif XDiff == 0:
			if YDiff > 0:
				Angle = -90
			else:
				Angle = 90
			pupilShiftX = self.pupilOffsetRatio * math.cos(math.radians(Angle))
			pupilShiftY = self.pupilOffsetRatio * math.sin(math.radians(Angle))
		elif YDiff == 0:
			if XDiff < 0:
				Angle = 0
			else:
				Angle = 180
			pupilShiftX = self.pupilOffsetRatio * math.cos(math.radians(Angle))
			pupilShiftY = self.pupilOffsetRatio * math.sin(math.radians(Angle))
		return (pupilShiftX, pupilShiftY)

	# Update position properties based on a given gravity value
	def updatePosition(self, gravity):
		
		self.yv += gravity
		self.x += self.xv
		self.y += self.yv

	def draw(self, gameWin, backgroundColor, ball):
		
		self.drawBody(gameWin, backgroundColor)
		self.drawEye(gameWin, ball)
		self.drawMessage(gameWin)

	def drawBody(self, gameWin, backgroundColor):
		
		self.drawAACircle(gameWin, int(self.x), int(self.y), int(self.radius), self.color)
		pygame.draw.rect(gameWin, backgroundColor, (self.x - self.radius, self.y, self.radius * 2 + 1, self.radius + 1))
		pygame.gfxdraw.line(gameWin, int(self.x - self.radius), int(self.y), int(self.x + self.radius), int(self.y), pygame.color.Color("black"))

	def drawEye(self, gameWin, ball):
		
		# If the ball contacts the ground on this player's side, widen the white of his eye
		if ball.y + ball.radius >= pygame.display.get_surface().get_height():
			if self.x < pygame.display.get_surface().get_width() / 2 and ball.x < pygame.display.get_surface().get_width() / 2:
				eyeRadius = self.radius / 3
			elif self.x > pygame.display.get_surface().get_width() / 2 and ball.x > pygame.display.get_surface().get_width() / 2:
				eyeRadius = self.radius / 3
			else:
				eyeRadius = self.radius / 4
		else:
			eyeRadius = self.radius / 4

		if (self.x < pygame.display.get_surface().get_width() / 2):
			self.drawAACircle(gameWin, int(self.x + self.eyeX), int(self.y - self.eyeY), int(eyeRadius), pygame.color.Color("lightgray"))
		else:
			self.drawAACircle(gameWin, int(self.x - self.eyeX), int(self.y - self.eyeY), int(eyeRadius), pygame.color.Color("lightgray"))
		
		self.drawPupil(gameWin, ball)

	def drawPupil(self, gameWin, ball):
		
		# Draw the pupil so it is tracking the ball's location
		if self.x < pygame.display.get_surface().get_width() / 2:
			(pupilOffsetX, pupilOffsetY) = self.getPupilOffset(ball, self.eyeX)
		else:
			(pupilOffsetX, pupilOffsetY) = self.getPupilOffset(ball, -self.eyeX)

		if (self.x < pygame.display.get_surface().get_width() / 2):
			self.drawAACircle(gameWin, int(self.x + self.eyeX + pupilOffsetX), int(self.y - self.eyeY + pupilOffsetY), int(self.radius / 8), pygame.color.Color("black"))
		else:
			self.drawAACircle(gameWin, int(self.x - self.eyeX + pupilOffsetX), int(self.y - self.eyeY + pupilOffsetY), int(self.radius / 8), pygame.color.Color("black"))

	def drawMessage(self, gameWin):
		
		messageLabel = self.messageFont.render(self.message, True, pygame.color.Color("black"))
		messageLabelRect = messageLabel.get_rect(center = (self.x, self.y - self.radius - 20))
		gameWin.blit(messageLabel, messageLabelRect)

	# Draw a circle with smooth edges using anti-aliasing
	def drawAACircle(self, gameWin, x, y, r, color):
		
		pygame.gfxdraw.filled_circle(gameWin, int(x), int(y), int(r), color)
		pygame.gfxdraw.aacircle(gameWin, int(x), int(y), int(r), pygame.color.Color("black"))