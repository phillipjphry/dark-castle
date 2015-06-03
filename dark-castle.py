#from __future__ import division
import pygame, sys, random, os
from pygame.locals import *

pygame.init()
pygame.joystick.init()
pygame.font.init()

#global counting
#counting = 0

class TileCache(object):
	"""Load the tilesets lazily in to the global cache"""

	def __init__(self, width= 32, height = None):
		self.width = width
		self.height = height or width
		self.cache = {}

	def __getitem__(self, filename):
		"""return a table of tiles, load it from disk if needed. """

		key = (filename, self.width, self.height)
		try:
			return self.cache[key]
		except KeyError:
			tile_table = self._load_tile_table(filename, self.width, self.height)
			self.cache[key] = tile_table
			return tile_table

	def _load_tile_table(self, filename, width, height):
		"""load and image and split it into tiles."""

		filename = os.path.join('data', filename)
		image = pygame.image.load(filename).convert_alpha()
		image_width, image_height = image.get_size()
		#print image_width, image_height
		tile_table = []
		for tile_x in range(0, image_width/width):
			line = []
			tile_table.append(line)
			for tile_y in range(0, image_height/height):
				rect = (tile_x*width, tile_y*height, width, height)
				line.append(image.subsurface(rect))
		return tile_table


class TextPrint:
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font("FreeSansBold.ttf", 20)

    def prints(self, DISPLAYSURF, textString):
        textBitmap = self.font.render(textString, True, BLUE)
        DISPLAYSURF.blit(textBitmap, [self.x, self.y])
        self.y += self.line_height
        
    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 25
        
    def indent(self):
        self.x += 10
        
    def unindent(self):
        self.x -= 10


class Player(object):
	
	def main(self):
		#print self.x
		#print self.y
		self.x = self.x
	def fire (self, pBullet, dx, dy):
		#ADD FIRING DIRECTIONS HERE
		#REFERENCE PROJECTfireILE CLASS
		#playing.pBullet.append(playing.pBulletnum)
		#playing.pBulletnum += 1
		playing.playerProjectiles[pBullet].shown = True
		playing.playerProjectiles[pBullet].dx = dx
		playing.playerProjectiles[pBullet].dy = dy
		playing.playerProjectiles[pBullet].objRect = Rect((self.playerRect.x, self.playerRect.y), (40, 40))


	def walk(self, dx, dy):
		#collided = False
		for frame in range(5):
			#if self.collide(dx, dy):
			#if collided == True:
			#	break
			self.playerRect.move_ip(dx, dy)
			if self.collide(dx, dy):
				self.playerRect.move_ip(-dx, -dy)
				#collided = True

			#if self.collideEnemy():
			#	self.playerRect.move_ip(5, 0)
			#	pass
			
			#if self.collide(dx, dy):
				#if self.collideEnemy():
				#	self.playerRect.move_ip(5, 0)
				#pass
				#self.playerRect.move_ip(dx, dy)
				#break
			#playing.renderAll()
			""" trying something new """
			self.counting += 1
			if self.counting >= 25:

				#for frame in range(4):
				#	print self.frames
				self.image = self.frames[self.frame][0]
				#DISPLAYSURF.blit(self.image, self.objRect)
				self.frame += 1
				if self.frame >= 4:
					self.frame = 0
				self.counting = 0
			DISPLAYSURF.blit(self.image, self.playerRect)
			""" trying something new """
			for count in playing.playerProjectiles:
				count.render(count.dx, count.dy)
			pygame.display.update()
		#collided = False


	def collideEnemy(self):
		damaged = False
		for count in range(len(playing.enemyList)):
			damaged = playing.enemyList[count].enemyRect.colliderect(playing.playerone.playerRect)
			#print damaged
			if damaged == True:
				self.health -= 1
				print self.health
				if self.health <= 0:
					pygame.quit()
					sys.exit()
				return True
			#return damaged
		return damaged
	
	def collide(self, dx, dy):
		for count in playing.walls:
			if count.blocking:
				#print "bang!"
				wallhit = self.playerRect.colliderect(count.objRect)
			else:
				wallhit = False
			if wallhit:
				self.playerRect.move_ip(-dx, -dy)

		if playing.centerWall.blocking:
			wallhit = self.playerRect.colliderect(playing.centerWall.objRect)
		else:
			wallhit = False
		if wallhit:
			self.playerRect.move_ip(-dx, -dy)

		if playing.gate.blocking:
			gatehit = self.playerRect.colliderect(playing.gate.objRect)
		else:
			gatehit = False
		exithit = self.playerRect.colliderect(playing.exit.objRect)

		if exithit:
			levelChoice.levelsDone()
			levelChoice.setLevel()
			
			playing.points += 20 
			#- (playing.time / 1000)
			playing.initTwo(playing.points)
		if self.collideEnemy():
			for count in range(7):
				self.playerRect.move_ip(dx*-7, dy*-7)
				#self.render()
				playing.renderAll()
				pygame.time.wait(15)
				pygame.display.update()


	
		if playing.bounds.objRect.contains(self.playerRect):
			return False
		else:
			return True
	def render(self):
		#draw the player
		#pygame.draw.rect(DISPLAYSURF, GREEN, self.playerRect, 0)
		DISPLAYSURF.blit(self.image, self.playerRect)

		#needed to draw while moving
		self.mouseRect = Rect((pygame.mouse.get_pos(), (20, 20)))
		pygame.draw.rect(DISPLAYSURF, GREEN, self.mouseRect, 0)

		if self.health > 0:
			for num in range(self.health):
				
				pygame.draw.rect(DISPLAYSURF, GREEN, self.healthbar[num].objRect, 0)




		if self.mouseCursor:
			self.targettopRect = ((self.mouseRect.centerx - 5, self.mouseRect.top - 40), (10, 30))
			self.targetbottomRect = ((self.mouseRect.centerx - 5, self.mouseRect.bottom + 10), (10, 30))
			self.targetrightRect = ((self.mouseRect.right + 10, self.mouseRect.centery - 5), (30, 10))
			self.targetleftRect = ((self.mouseRect.left - 40, self.mouseRect.centery - 5), (30, 10))
		#	self.targetright = ((self.x + 45, self.y + 5), (30, 10))
			pygame.draw.rect(DISPLAYSURF, BLUE, self.targettopRect, 0)
			pygame.draw.rect(DISPLAYSURF, BLUE, self.targetbottomRect, 0)
			pygame.draw.rect(DISPLAYSURF, BLUE, self.targetrightRect, 0)
			pygame.draw.rect(DISPLAYSURF, BLUE, self.targetleftRect, 0)

		#fontObj = pygame.font.SysFont('ubuntumono', 32)
		#self.textSurfaceObj = fontObj.render('Beep', True, BLUE, GREEN)
		#self.textRectObj = self.textSurfaceObj.get_rect()
		#self.textRectObj.center = (self.x, self.y)

	def __init__(self, start=(0, 0)):
		#load the player image
		#playerImg = pygame.image.load('cat.png')
		self.playerRect = Rect(start, (32, 32))
		self.frames = SPRITE_CACHE["gluer.png"]
		self.walking = 0
		self.frame = 0
		self.counting = 0
		self.mouseRect = Rect(pygame.mouse.get_pos(), (20, 20))
		self.mouseCursor = False
		self.dx = 0
		self.dy = 0
		self.direction = 0
		self.points = 0
		self.image = self.frames[self.direction][0]
		self.health = 4
		self.healthbar = [Thing(500 + count*50, 50, GREEN, False, 10, 10) for count in range(self.health)]



class Enemy(object):
	def collide(self, playerBullets):
		for count in range(len(playing.playerProjectiles)):

			if self.enemyRect.colliderect(playing.playerProjectiles[count].objRect):
				#playing.playerProjectiles[count].shown = False
				#print playing.playerProjectiles[count].shown
				self.energy -= 1
				playing.playerProjectiles[count].die(True)
				if self.energy <= 0:
					playing.playerone.points += self.points
					self.dead = True
				#self.shown = False


	def render(self):
		if self.dead == True:
			playing.enemyList.remove(self)
			#print "Poot"
		if pygame.time.get_ticks() >= self.spawnTime:
			self.dead = False
			self.shown = True
			self.spawned = True
			self.collide(playing.playerProjectiles)
		if playing.bounds.objRect.contains(self.enemyRect):
				self.shown = True
		else:

				#playing.spawnPoint.append([0, 0])
				#playing.spawnTime.append(int(playing.time) + 1000)
				playing.enemyList.append(Enemy([random.randint(0, 700), random.randint(0, 900)], int(playing.time) + 1000))
				print "poof"
				self.shown = False
				playing.enemyList.remove(self)
				print "splat"
		if self.shown == True:
			moveEnemyX = random.randint(0, 1000)
			moveEnemyY = random.randint(0, 1000)
			if moveEnemyX >= 750:
				
				if moveEnemyX % 2 == 0:
					moveEnemyX = -1
				else:
					moveEnemyX = 1
			else:
				moveEnemyX = 0
			
			if moveEnemyY >= 750:
				
			
				if moveEnemyY % 2 == 0:
					moveEnemyY = -1
				else:
					moveEnemyY = 1
			else:
				moveEnemyY = 0
			self.enemyRect.move_ip(moveEnemyX, moveEnemyY)
			
			#draw the prototype
			#pygame.draw.rect(DISPLAYSURF, BLUE, self.enemyRect, 0)
			DISPLAYSURF.blit(playing.cloud, self.enemyRect)

	def __init__(self, spawnPoint, spawnTime):
		self.enemyRect = Rect(spawnPoint, (32, 32))
		self.spawnTime = spawnTime
		self.spawned = False
		self.shown = False
		self.dead = False
		self.energy = random.randint(1, 5)
		self.points = self.energy
"""hurm"""

class Sprite(pygame.sprite.Sprite):
	
	is_player = False

	def __init__(self, pos=(0, 0), frames=None):
		super(Sprite, self).__init__()
		if frames:
			self.frames = frames
		self.animation = self.stand_animation()
		self.image = self.frames[0][0]
		self.rect = self.image.get_rect()
		self.pos = pos

	def stand_animation(self):
		while True:
			for frame in self.frames[0]:
				self.image = frame
				yield None
				yield None

	def update(self, *args):
		if self.animation is None:
			self.image = self.frames[self.direction][0]
		else:
			try:
				self.animation.next()
			except StopIteration:
				self.animation = None
		#self.animation.next()

	def _get_pos(self):
		"""check the current position of the sprite on the map"""
		return (self.rect.midbottom[0]-12)/24, (self.rect.midbottom[1]-16)/16

	def _set_pos(self, pos):
		"""set the position and depth of the sprite on the map"""

		self.rect.midbottom = pos[0]*24+12, pos[1]*16+16
		self.depth = self.rect.midbottom[1]

	pos = property(_get_pos, _set_pos)

	def move(self, dx, dy):
		"""change the position of the sprite on the screen"""

		self.rect.move_ip(dx, dy)
		self.depth = self.rect.midbottom[1]

""" hurm"""


class Thing(Sprite):


	def __init__(self, x, y, COLOR, blocking, width, height):
		self.x = x
		self.y = y
		self.color = COLOR
		self.blocking = blocking
		self.objRect = Rect((self.x, self.y), (width, height))

class Projectile(Thing):

	"""
	def walk_animation(self):
		animation for the player walking.

		#this animation is hardcoded for 4 frames and 16x24 map tiles
		for frame in range(4):
			self.image = self.frames[self.direction][frame]
			yield None
			self.move(3*self.dx[self.direction], 2*self.dy[self.direction])
			yield None
			self.move(3*self.dx[self.direction], 2*self.dy[self.direction])
			self.direction += 1
			if self.direction == 4:
				self.direction = 0
	"""

	def die(self, is_dead):
		if is_dead:
			self.shown = False
			self.objRect.center = (801, 601)
			#self.direction = (0, 0)
			#print self.shown
	def render(self, dx, dy):
		#global counting
		if playing.bounds.objRect.contains(self.objRect):
				self.shown = True
		else:
				self.shown = False
		for count in playing.enemyList:
			if count.shown == False:
				return None
			elif count.enemyRect.colliderect(self.objRect):
				self.shown = False
		if self.shown == False:
			return None
		else: #playing.playerProjectiles[pBullet].shown == True:
			if self.frameOne == True:
				self.objRect.center = (self.objRect.centerx + 8, self.objRect.centery + 8)
				self.frameOne = False

			self.objRect.move_ip(dx*1, dy*1)
			#counting += 1
			#print counting
			#DEBUG
			#print self.objRect.centerx
			#DEBUG
			#self.objRect.center = (self.objRect.centerx + 25, self.objRect.centery + 25)
			#self.objRect.left = self.objRect.left + 25
			

			#draw the prototype
			#pygame.draw.rect(DISPLAYSURF, self.color, self.objRect, self.damage)
			#draw the roller
			#DISPLAYSURF.blit(self.sprite, self.objRect)
			#self.walk_animation()
			self.counting += 1
			if self.counting >= 25:

				#for frame in range(4):
				#	print self.frames
				self.image = self.frames[self.frame][0]
				#DISPLAYSURF.blit(self.image, self.objRect)
				self.frame += 1
				if self.frame >= 4:
					self.frame = 0
				self.counting = 0
			DISPLAYSURF.blit(self.image, self.objRect)

			#yield None
			#self.move_ip(self.dx, self.dy)
			#yield None
			#self.move_ip(self.dx, self.dy)
			#yield None
			#self.direction += 1
			#if self.direction == 2:
			#	self.direction = 0
			
			#	DISPLAYSURF.blit(self.image, self.objRect)
			#pygame.display.update()
			#DISPLAYSURF.fill(WHITE)
			#playing.renderAll()
			#pygame.time.wait(1000)
		#return
	def __init__(self, x, y, COLOR, blocking, width, height, damage, direction, shown, number):
		Thing.__init__(self, x, y, COLOR, blocking, width, height)
		#playing.playerProjectiles.append(self)
		self.counting = 0
		self.frames = SPRITE_CACHE["roller.png"]
		self.objRect = Rect((self.objRect.center), (height, width))
		self.direction = direction
		self.shown = shown
		self.counting = 0
		self.frameOne = True
		self.damage = 5
		self.frame = 0
		self.dx = 0
		self.dy = 0
		self.destination = 0
		self.pBullet = number
		""" Display and animate the player character."""
		Sprite.__init__(self, (x, y))
		self.direction = 0
		self.animation = None
		self.image = self.frames[self.direction][0]


#		self.bulletRect = Rect((self.x, self.y), (10, 10))
#	def travel(self, x, y, COLOR, damage):



class Tile(Thing):

	def render(self):
		pygame.draw.rect(DISPLAYSURF, self.color, self.objRect, self.tilePressed)	

	def __init__(self, x, y, COLOR, blocking, width, height):
		Thing.__init__(self, x, y, COLOR, blocking, width, height)
		self.tilePressed = 5
		self.pushed = False

class interObject(Thing):

	def render(self):
		pygame.draw.rect(DISPLAYSURF, self.color, self.objRect, self.action)

	def __init__(self, x, y, COLOR, blocking, width, height):
		Thing.__init__(self, x, y, COLOR, blocking, width, height)
		self.action = 0

class levelPicker(object):
	def setLevel(self):
		if self.level == 1:
			self.level += 1
		elif self.level == 2:
			self.level = 2
	def levelsDone(self):
		if self.levelsComplete == 1:
			self.levelsComplete += 1
		elif self.levelsComplete == 2:
			self.levelsComplete += 1

	def __init__(self):
		self.level = 1
		self.levelsComplete = 1

class Levels():

	def renderAll(self):
		if self.paused:
			pausedRect = Rect((0, 0), (800, 600))
			pygame.draw.rect(DISPLAYSURF, PAUSED, pausedRect, 0)
		elif levelChoice.level == 1:
			self.renderOne()
		elif levelChoice.level == 2:
			self.renderTwo()

	def initOne(self):
		self.cloud = pygame.image.load(os.path.join('data', 'cloud.png'))
		self.roller = pygame.image.load(os.path.join('data', 'roller.png'))
		self.bounds = Thing(0, 0, 0, False, 800, 1000)
		self.playerone = Player()
		self.tileone = Tile(125, 400, BLUE, False, 50, 50)
		self.tiletwo = Tile(375, 450, BLUE, False, 50, 50)
		self.tilethree = Tile(625, 400, BLUE, False, 50, 50)
		self.gate = interObject(750, 50, BLUE, True, 100, 25)
		self.exit = interObject(500, 0, BLUE, True, 75, 10)
	
		self.walls = []
		wallsWidth = [325, 325, 325, 325, 325]
		wallsHeight = [50, 50, 50, 50, 50]
		wallsY = [75, 275, 475, 675, 875]
		wallsX = [250, 250, 250, 250, 250]
		#print wallsXY[0], "BLUE", True, wallsWidthHeight[0]
		self.walls = [interObject(wallsX[count], wallsY[count], BLUE, True, wallsWidth[count], wallsHeight[count]) for count in range(5)]
		self.centerWall = interObject(400, 0, BLUE, True, 50, 925)
		self.playerProjectiles = []
		self.playerProjectiles = [Projectile(801, 601, GREEN, True, 10, 10, 5, (0, 0), False, count) for count in range(100)]
		self.pBullet = []
		for count in range(10):
			self.pBullet.append(count)
		#self.enemyProjectiles = [Projectile(self.playerone.playerRect.x, self.playerone.playerRect.y, BLUE, True, 10, 10, 5, (0, 0), False, count) for count in range(1000)]
		self.spawnPoint = [(0, 100), (125, 400), (150, 475), 
		(100, 600), (455, 0)]
		self.spawnTime = [1, 1000, 2500, 500, 750]
		self.enemyList = [Enemy(self.spawnPoint[count], self.spawnTime[count]) for count in range(5)]
		self.points = 0

	def initTwo(self, points):
		self.playerone = Player((350, 550))
		self.gate = interObject(350, 50, BLUE, True, 100, 25)
		self.exit = interObject(350, 0, BLUE, True, 100, 10)
		self.playerone.points = points
		#self.points += playing.points
		self.time = 0


	def actionOne(self):
		#Check if player has moved over a pushable tile

		pushtone = False
		pushttwo = False
		pushtthree = False


		pushedone = self.playerone.playerRect.colliderect(self.tileone.objRect)
		pushedtwo = self.playerone.playerRect.colliderect(self.tiletwo.objRect)
		pushedthree = self.playerone.playerRect.colliderect(self.tilethree.objRect)

		if pushedone:
			self.tileone.tilePressed = 0
			self.tileone.pushed = True
		if pushedtwo:
			self.tiletwo.tilePressed = 0
			self.tiletwo.pushed = True
		if pushedthree:
			self.tilethree.tilePressed = 0
			self.tilethree.pushed = True
	
		#check to see if we should open the gate
		if self.tileone.pushed and self.tiletwo.pushed and self.tilethree.pushed:
			self.gate.action = 5
			self.gate.color = GREEN
			self.gate.blocking = False

	def actionTwo(self):
		pass
	def renderOne(self):
		DISPLAYSURF.fill(WHITE)
		self.exit.render()
		self.tileone.render()
		self.tiletwo.render()
		self.tilethree.render()
		self.centerWall.render()
		for count in self.walls:
			count.render()
		self.playerone.render()
		for count in self.enemyList:
			count.render()

		for count in playing.playerProjectiles:
			count.render(count.dx, count.dy)
			#count.objRect.move_ip(count.dx*1, count.dy*1)
			#DEBUG
			#print self.objRect.centerx
			#DEBUG
			#self.objRect.center = (self.objRect.centerx + 25, self.objRect.centery + 25)
			#self.objRect.left = self.objRect.left + 25
			

			#draw the prototype
			#pygame.draw.rect(DISPLAYSURF, self.color, self.objRect, self.damage)
			#draw the roller
			#DISPLAYSURF.blit(self.sprite, self.objRect)
			#self.walk_animation()
			#for frame in range(4):
			#	#print count.frames
			#	count.image = count.frames[frame][0]
			#	DISPLAYSURF.blit(count.image, count.objRect)

			#yield None
			#self.move_ip(self.dx, self.dy)
			#yield None
			#self.move_ip(self.dx, self.dy)
			#yield None
			#self.direction += 1
			#if self.direction == 2:
			#	self.direction = 0
			

#			if self.bounds.objRect.contains(playing.playerProjectiles[count].objRect):
#				playing.playerProjectiles[count].shown = True
#			else:
#				playing.playerProjectiles[count].shown = False
			#DEBUG
			#print count.objRect.x
			#print count.objRect.y
			#DEBUG
#			if playing.playerProjectiles[count].shown == True:
#				playing.playerProjectiles[count].render(playing.playerProjectiles[count].direction,
#				 playing.playerProjectiles[count].pBullet)

	def renderTwo(self):
		DISPLAYSURF.fill(WHITE)
		#TODO: FIND AND DELETE ALL INGATE REFERENCES
		self.exit.render()
		self.playerone.render()
	def __init__(self):
		self.initOne()
#		self.playerProjectiles = []
#		self.playerProjectiles.append(Projectile(self.playerone.playerRect.x, self.playerone.playerRect.y, GREEN, True, 10, 10, 5, (0, 0), False, 0))
#		self.pBullet = []
#		self.pBulletnum = 0

		self.paused = False
		#self.playerone = Player()
#		self.playerProjectiles = [Projectile(self.playerone.playerRect.x, self.playerone.playerRect.y, GREEN, True, 10, 10, 5, playing) for count in range(100)]
#		self.enemyProjectiles = [Projectile(self.playerone.playerRect.x, self.playerone.playerRect.y, BLUE, True, 10, 10, 5, playing) for count in range(1000)]
		#for x in range(100):
		#	self.projectiles.append(x)
		#print self.playerProjectiles




#set up fps clock
time = 0
FPS = 120
gameClock = pygame.time.Clock()
fpsClock = pygame.time.Clock()
SPRITE_CACHE = TileCache()

#set up window
DISPLAYSURF = pygame.display.set_mode((800, 1000), 0, 32)
pygame.display.set_caption('Dark Castle')


#set things
WHITE = (255, 255, 255)
BLUE = (0, 0, 128)
GREEN = (0, 255, 0)
PAUSED = (0, 0, 0, 128)
playing = Levels()
textPrint = TextPrint()

levelChoice = levelPicker()

pygame.mouse.set_visible(0)


#DEBUG
pBulletNumber = 0
fireup = 0
#DEBUG

while True:
	#Check if player has moved over a pushable tile
	#DISPLAYSURF.blit(playerone.textSurfaceObj, playerone.textRectObj)
	keys_pressed = pygame.key.get_pressed()
	fireup += 1

	for event in pygame.event.get():
		mouse_pressed = pygame.mouse.get_pressed()
		if mouse_pressed[2]:
			playing.playerone.mouseCursor = not playing.playerone.mouseCursor
			#pygame.time.wait(10)
		if keys_pressed[K_RETURN]:
			playing.paused = not playing.paused
			#pygame.time.wait(10)
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
	#for event in pygame.event.get(): # User did something
	#if event.type == pygame.QUIT: # If user clicked close
		#done=True # Flag that we are done so we exit this loop
	# Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
		if event.type == pygame.JOYBUTTONDOWN:
			print("Joystick button pressed.")
		if event.type == pygame.JOYBUTTONUP:
			print("Joystick button released.")


	# DRAWING STEP
	# First, clear the DISPLAYSURF to white. Don't put other drawing commands
	# above this, or they will be erased with this command.
	#DISPLAYSURF.fill(WHITE)
	#playing.renderAll()
	textPrint.reset()
	"""
	#JOYSTICK CONTROLS
	joystick_count = pygame.joystick.get_count()

	for i in range(joystick_count):
		joystic = pygame.joystick.Joystick(i)
		joystic.init()
		axes = joystic.get_numaxes()
		dx = 0
		dy = 0
		for i in range( axes ):
			moved = False
			axis = joystic.get_axis( i )
			if moved == False:
				if i == 0:
					#print axis
					position = axis * 10
					if position > 5:
						playing.playerone.dx = 1
						playing.playerone.dy = 0
						#playing.playerone.walk(playing.playerone.dx, playing.playerone.dy)
						#playing.playerone.dx = 0
						#playing.playerone.dy = 0
					if position < -5:
						playing.playerone.dx = -1
						playing.playerone.dy = 0
						#playing.playerone.walk(playing.playerone.dx, playing.playerone.dy)
				if i == 1:
					position = axis * 10
					if position > 5:
						playing.playerone.dx = 0
						playing.playerone.dy = 1
						#playing.playerone.walk(playing.playerone.dx, playing.playerone.dy)
					if position < -5:
						playing.playerone.dx = 0
						playing.playerone.dy = -1
						#playing.playerone.walk(playing.playerone.dx, playing.playerone.dy)
						#playing.playerone.dx = 0
						#playing.playerone.dy = 0
				playing.playerone.walk(playing.playerone.dx, playing.playerone.dy)
				playing.playerone.dx = 0
				playing.playerone.dy = 0
				moved = True
			fired = False

			if fired == False:
				if i == 2:
					position = axis * 10
					if fireup % 10 == 0:
						if fireup / 10 > 99:
							fireup = 0
						pBulletNumber = fireup / 10
						playing.playerProjectiles[pBulletNumber].frameOne = True
						if position > 5:
							dx = 1
						if position < -5:
							dx = -1
				if i == 3:
					position = axis * 10
					if fireup % 10 == 0:
						if fireup / 10 > 99:
							fireup = 0
						pBulletNumber = fireup / 10
						playing.playerProjectiles[pBulletNumber].frameOne = True
						if position > 5:
							dy = 1
						if position < -5:
							dy = -1
				if dx != 0 or dy != 0 or dx == 1 and dy == 1 or dx == -1 and dy == -1:
					playing.playerone.fire(playing.pBullet[pBulletNumber], dx, dy)		
					fired = True
					#elif keys_pressed[K_d]:
					#	playing.playerone.fire(playing.pBullet[pBulletNumber], 1, -1)
					#else:
					#	playing.playerone.fire(playing.pBullet[pBulletNumber], 0, -1)
			
			#playing.playerProjectiles[pBulletNumber].dx = 0
			#playing.playerProjectiles[pBulletNumber].dy = 0
	
	"""		
	#JOYSTICK CONTROLS
	
	"""
	# Get count of joysticks
	joystick_count = pygame.joystick.get_count()

	textPrint.prints(DISPLAYSURF, "Number of joysticks: {}".format(joystick_count) )
	textPrint.indent()
	
	# For each joystick:
	for i in range(joystick_count):
		joystick = pygame.joystick.Joystick(i)
		joystick.init()
	
		textPrint.prints(DISPLAYSURF, "Joystick {}".format(i) )
		textPrint.indent()
	
		# Get the name from the OS for the controller/joystick
		name = joystick.get_name()
		textPrint.prints(DISPLAYSURF, "Joystick name: {}".format(name) )
		
		# Usually axis run in pairs, up/down for one, and left/right for
		# the other.
		axes = joystick.get_numaxes()
		textPrint.prints(DISPLAYSURF, "Number of axes: {}".format(axes) )
		textPrint.indent()
		
		for i in range( axes ):
			axis = joystick.get_axis( i )
			textPrint.prints(DISPLAYSURF, "Axis {} value: {:>6.3f}".format(i, axis) )
		textPrint.unindent()
			
		buttons = joystick.get_numbuttons()
		textPrint.prints(DISPLAYSURF, "Number of buttons: {}".format(buttons) )
		textPrint.indent()

		for i in range( buttons ):
			button = joystick.get_button( i )
			textPrint.prints(DISPLAYSURF, "Button {:>2} value: {}".format(i,button) )
		textPrint.unindent()
			
		# Hat switch. All or nothing for direction, not like joysticks.
		# Value comes back in an array.
		hats = joystick.get_numhats()
		textPrint.prints(DISPLAYSURF, "Number of hats: {}".format(hats) )
		textPrint.indent()

		for i in range( hats ):
			hat = joystick.get_hat( i )
			textPrint.prints(DISPLAYSURF, "Hat {} value: {}".format(i, str(hat)) )
		textPrint.unindent()
		
		textPrint.unindent()
	"""

	if levelChoice.level == 1:
		playing.actionOne()
	if levelChoice.level == 2:
		playing.actionTwo()

	#controls
	#keys_pressed = pygame.key.get_pressed()
	#if keys_pressed[K_RETURN]:
	#	playing.paused = False
	#	print "Pee"
	#	fpsClock.tick(FPS)

	

	#FIRE KEYS
	
	#DEBUG
	#print fireup / 10
	#DEBUG
	if playing.paused == False:
		if keys_pressed[K_w]:
			if fireup % 2 == 0:
				if fireup % 2 >= 9:
					fireup = 0
				else:
					fireup = fireup % 2
				pBulletNumber = fireup
				print pBulletNumber
				playing.playerProjectiles[pBulletNumber].frameOne = True
				if keys_pressed[K_a]:
					playing.playerone.fire(playing.pBullet[pBulletNumber], -1, -1)
				elif keys_pressed[K_d]:
					playing.playerone.fire(playing.pBullet[pBulletNumber], 1, -1)
				else:
					playing.playerone.fire(playing.pBullet[pBulletNumber], 0, -1)
		elif keys_pressed[K_a]:
			if fireup % 2 == 0:
				if fireup % 2 >= 9:
					fireup = 0
				else:
					fireup = fireup % 2
				pBulletNumber = fireup
				print pBulletNumber
				playing.playerProjectiles[pBulletNumber].frameOne = True
				if keys_pressed[K_w]:
					playing.playerone.fire(playing.pBullet[pBulletNumber], -1, -1)
				elif keys_pressed[K_s]:
					playing.playerone.fire(playing.pBullet[pBulletNumber], -1, 1)
				else:
					playing.playerone.fire(playing.pBullet[pBulletNumber], -1, 0)
		elif keys_pressed[K_s]:
			if fireup % 2 == 0:
				if fireup % 2 >= 9:
					fireup = 0
				else:
					fireup = fireup % 2
				pBulletNumber = fireup
				print pBulletNumber
				playing.playerProjectiles[pBulletNumber].frameOne = True
				if keys_pressed[K_a]:
					playing.playerone.fire[playing.pBullet[pBulletNumber], -1, 1]
				elif keys_pressed[K_d]:
					playing.playerone.fire(playing.pBullet[pBulletNumber], 1, 1)
				else:
					playing.playerone.fire(playing.pBullet[pBulletNumber], 0, 1)
		elif keys_pressed[K_d]:
			if fireup % 2 == 0:
				if fireup % 2 >= 9:
					fireup = 0
				else:
					fireup = fireup % 2
				pBulletNumber = fireup
				print pBulletNumber
				playing.playerProjectiles[pBulletNumber].frameOne = True
				if keys_pressed[K_s]:
					playing.playerone.fire(playing.pBullet[pBulletNumber], 1, 1)
				elif keys_pressed[K_w]:
					playing.playerone.fire(playing.pBullet[pBulletNumber], 1, -1)
				else:
					playing.playerone.fire(playing.pBullet[pBulletNumber], 1, 0)
		#FIRE KEYS END




		if keys_pressed[K_LEFT]:
			if keys_pressed[K_UP]:
				playing.playerone.dx = -1
				playing.playerone.dy = -1
				playing.playerone.walk(playing.playerone.dx, playing.playerone.dy)
			elif keys_pressed[K_DOWN]:
				playing.playerone.dx = -1
				playing.playerone.dy = 1
				playing.playerone.walk(playing.playerone.dx, playing.playerone.dy)
			else:
				playing.playerone.dx = -1
				playing.playerone.dy = 0
				playing.playerone.walk(playing.playerone.dx, playing.playerone.dy)
		if keys_pressed[K_RIGHT]:
			if keys_pressed[K_UP]:
				playing.playerone.dx = 1
				playing.playerone.dy = -1
				playing.playerone.walk(playing.playerone.dx, playing.playerone.dy)
			elif keys_pressed[K_DOWN]:
				playing.playerone.dx = 1
				playing.playerone.dy = 1
				playing.playerone.walk(playing.playerone.dx, playing.playerone.dy)
			else:
				playing.playerone.dx = 1
				playing.playerone.dy = 0
				playing.playerone.walk(playing.playerone.dx, playing.playerone.dy)
		if keys_pressed[K_UP]:
			if keys_pressed[K_RIGHT] or keys_pressed[K_LEFT]:
				pass
			else:
				playing.playerone.dx = 0
				playing.playerone.dy = -1
				playing.playerone.walk(playing.playerone.dx, playing.playerone.dy)
		if keys_pressed[K_DOWN]:
			if keys_pressed[K_RIGHT] or keys_pressed[K_LEFT]:
				pass
			else:
				playing.playerone.dx = 0
				playing.playerone.dy = 1
				playing.playerone.walk(playing.playerone.dx, playing.playerone.dy)


	#if keys_pressed[K_RETURN]:
	#	print "Poop"
	#	playing.paused = not playing.paused
	#	fpsClock.tick(FPS)
	#mouse is now in render of player class
	gameClock.tick()
	time += gameClock.get_time()
	#print time

	playing.renderAll()
	playing.time = time
	textPrint.prints(DISPLAYSURF, "Time Elapsed : {}".format(str(time)))
	textPrint.prints(DISPLAYSURF, "Points Earned : {}".format(playing.playerone.points))
	#playing.renderAll()
	pygame.display.update()
	fpsClock.tick(FPS)






#load the object tiles
#tileone = pygame.image.load('tile.png')
#tiletwo = tileone
#tilethree = tileone
