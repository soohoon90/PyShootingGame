################################################################################
## Programmer's Block
################################################################################

# TITLE		AXOGEN ENGINE
# CODER		HOON CHO
# VERSION	RC 1
# DATE		MAY 27

################################################################################
## Module Work
################################################################################

import math, pygame, random, sys, time

################################################################################
## Constants Init
################################################################################

RESX = 800									# X RESOLUTION
RESY = 600									# Y RESOLUTION
MIDX = RESX / 2
MIDY = RESY / 2

NOMOVE = 0									# VALUE FOR NO MOVEMENT

RESPATH = "resources/"						# PATH TO RESOURCES FOLDER
FONTPATH = RESPATH + "font/"				# PATH TO FONT FOLDER
IMGPATH = RESPATH + "image/"				# PATH TO IMAGE FOLDER
WAVPATH = RESPATH + "music/"				# PATH TO WAV FOLDER

PATHNAMES =  RESPATH+"names.txt"
PATHNUMBERS = RESPATH+"numbers.txt"

FPS = 40									# FRAMES PER SECOND
CHS = 30									# NUMBER OF CHANNELS
STARTTIME = time.time()						# START TIME

HOWMANYBULLET = 5							# HOW MANY IN BULLET DICTIONARY
HOWMANYFOE = 7								# HOW MANY IN FOE DICTIONARY
HOWMANYITEM = 5								# HOW MANY IN FOE DICTIONARY

ALPHABET = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

################################################################################
## High Score Init
################################################################################

names = open(PATHNAMES,"r").readlines()
numbers = open(PATHNUMBERS,"r").readlines()

for i in range(len(names)):
	names[i] = names[i].strip()
for i in range(len(numbers)):
	numbers[i] = numbers[i].strip()

for i in range(len(names)-1,-1,-1):
	if names[i] == "":
		del names[i]

for i in range(len(numbers)-1,-1,-1):
	if numbers[i] == "":
		del numbers[i]

################################################################################
## Variable Init
################################################################################

game = {}
game['hits'] = 0
game['kills'] = 0
game['misses'] = 0
game['hurts'] = 0
game['score'] = 0
game['money'] = 137
game['state'] = 0
game['over'] = 0
game['name'] = ""

## preset dictionary init
set_char = {}
set_bullet = []
set_foe = []
set_item = []
for i in range(HOWMANYBULLET):	set_bullet.append({})
for i in range(HOWMANYFOE):		set_foe.append({})
for i in range(HOWMANYITEM):	set_item.append({})

## object lists init (to be used in blitEverything)
foes = []
items = []
bullets = []

## upgrade preset dictionary init
upgrademax = {}
upgradenow = {}
upgradeby = {}
upgradecost = {}

################################################################################
## Game Init
################################################################################										

pygame.init()													# init pygame
pygame.font.init()												# init font
pygame.mixer.init()												# init sounds
pygame.mixer.set_num_channels(CHS)								# inc. # of channel	
screen = pygame.display.set_mode((RESX, RESY+50), 0, 32)		# init screen
clock = pygame.time.Clock()										# init clock
pygame.display.set_caption("Axogen: SC Crisis")					# set title

### load fonts
fontSan = pygame.font.Font(FONTPATH+"FreeSansBold.ttf", 30)
fontSanN = pygame.font.Font(FONTPATH+"FreeSans.ttf", 24)
fontName = pygame.font.Font(FONTPATH+"FreeSansBold.ttf", 42)

### load images
imgRed = pygame.image.load(IMGPATH+"red.png").convert_alpha()
imgBlack = pygame.image.load(IMGPATH+"black10.png").convert_alpha()
imgWhite = pygame.image.load(IMGPATH+"white30.png").convert_alpha()
imgTitle = pygame.image.load(IMGPATH+"title.png").convert()
imgDisclaimer = pygame.image.load(IMGPATH+"disclaimer.png").convert()
imgNaming = pygame.image.load(IMGPATH+"naming.png").convert()
imgStory = pygame.image.load(IMGPATH+"story.png").convert()
imgTutorial = pygame.image.load(IMGPATH+"tutorial.png").convert()
imgUpgrade = pygame.image.load(IMGPATH+"upgrade.png").convert()
imgBg = pygame.image.load(IMGPATH+"bg.png").convert()
imgBgBar = pygame.image.load(IMGPATH+"bgbar.png").convert_alpha()
imgChar = pygame.image.load(IMGPATH+"brian.png").convert_alpha()
imgChar2 = pygame.image.load(IMGPATH+"brian2.png").convert_alpha()
imgChar3 = pygame.image.load(IMGPATH+"brian3.png").convert_alpha()
imgFoe = pygame.image.load(IMGPATH+"min.png").convert_alpha()
imgFoe2 = pygame.image.load(IMGPATH+"dan.png").convert_alpha()
imgFoe3 = pygame.image.load(IMGPATH+"steph.png").convert_alpha()
imgFoe4 = pygame.image.load(IMGPATH+"fab.png").convert_alpha()
imgFoe5 = pygame.image.load(IMGPATH+"andrew2.png").convert_alpha()
imgFoe6 = pygame.image.load(IMGPATH+"hoon2.png").convert_alpha()
imgFoe7 = pygame.image.load(IMGPATH+"blake.png").convert_alpha()
imgBullet = pygame.image.load(IMGPATH+"bullet.png").convert_alpha()
imgBullet2 = pygame.image.load(IMGPATH+"bullet2.png").convert_alpha()
imgBullet3 = pygame.image.load(IMGPATH+"bullet3.png").convert_alpha()
imgBullet4 = pygame.image.load(IMGPATH+"bullet4.png").convert_alpha()
imgItem = pygame.image.load(IMGPATH+"item.png").convert_alpha()
imgItem2 = pygame.image.load(IMGPATH+"item2.png").convert_alpha()
imgMoney = pygame.image.load(IMGPATH+"money.png").convert_alpha()

### load sounds
wavGattle = pygame.mixer.Sound(WAVPATH+"eff_gattle.wav")
wavPistol = pygame.mixer.Sound(WAVPATH+"eff_pistol.wav")
wavShotgun = pygame.mixer.Sound(WAVPATH+"eff_shotgun.wav")
wavNade = pygame.mixer.Sound(WAVPATH+"eff_grenade.wav")
wavWarning = pygame.mixer.Sound(WAVPATH+"eff_warning.wav")
wavFanfare = pygame.mixer.Sound(WAVPATH+"eff_fanfare.wav")
wavTing = pygame.mixer.Sound(WAVPATH+"eff_ting.wav")
wavBuzzer = pygame.mixer.Sound(WAVPATH+"eff_buzzer.wav")
wavUpgrade = pygame.mixer.Sound(WAVPATH+"eff_upgrade.wav")
wavHeal = pygame.mixer.Sound(WAVPATH+"eff_heal.wav")
wavReload = pygame.mixer.Sound(WAVPATH+"eff_phew2.wav")
wavReloadDone = pygame.mixer.Sound(WAVPATH+"eff_phew.wav")
wavCrap = pygame.mixer.Sound(WAVPATH+"eff_brian2.wav")
wavOYes = pygame.mixer.Sound(WAVPATH+"eff_brian3.wav")

################################################################################
## Bullet Presets
################################################################################
## img, size, attack, angle, speed
################################################################################

## Granade
set_bullet[0]['img'] = imgBullet2
set_bullet[0]['attack'] = 10
set_bullet[0]['speed'] = 12

## Level 1
set_bullet[1]['img'] = imgBullet
set_bullet[1]['attack'] = 1
set_bullet[1]['speed'] = 8

## Level 2
set_bullet[2]['img'] = imgBullet3
set_bullet[2]['attack'] = 3
set_bullet[2]['speed'] = 10

## Level 3
set_bullet[3]['img'] = imgBullet4
set_bullet[3]['attack'] = 5
set_bullet[3]['speed'] = 12

################################################################################
## Upgrade Presets
################################################################################

upgrademax['clip'] = 5
upgrademax['spread'] = 4
upgrademax['damage'] = 2
upgrademax['maxhealth'] = 5
upgrademax['rapid'] = 1
upgrademax['faster'] = 1

upgradenow['clip'] = 0
upgradenow['spread'] = 0
upgradenow['damage'] = 0
upgradenow['maxhealth'] = 0
upgradenow['rapid'] = 0
upgradenow['faster'] = 0

upgradeby['clip'] = 25
upgradeby['spread'] = 1
upgradeby['damage'] = 1
upgradeby['maxhealth'] = 10
upgradeby['faster'] = 3

upgradecost['clip'] = 86
upgradecost['spread'] = 147
upgradecost['damage'] = 168
upgradecost['maxhealth'] = 137
upgradecost['rapid'] = 274
upgradecost['faster'] = 197
upgradecost['health'] = 7
upgradecost['nade'] = 64
upgradecost['xtranade'] = 14

################################################################################
## Foe Presets
################################################################################
## imgs, pos, health, attack, angle, range, speed, scoreby
################################################################################

## small ones
## small slow 
set_foe[0]['img'] = imgFoe
set_foe[0]['health'] = 2
set_foe[0]['attack'] = 5
set_foe[0]['range'] = 1
set_foe[0]['speed'] = 1
set_foe[0]['scoreby'] = 17

## small slight fast
set_foe[1]['img'] = imgFoe2
set_foe[1]['health'] = 1
set_foe[1]['attack'] = 4
set_foe[1]['range'] = 1
set_foe[1]['speed'] = 2
set_foe[1]['scoreby'] = 26

## big ones
## big slow 
set_foe[2]['img'] = imgFoe3
set_foe[2]['health'] = 7
set_foe[2]['attack'] = 7
set_foe[2]['range'] = 1
set_foe[2]['speed'] = 1.6
set_foe[2]['scoreby'] = 58

## big fast
set_foe[3]['img'] = imgFoe4
set_foe[3]['health'] = 15
set_foe[3]['attack'] = 9
set_foe[3]['range'] = 1
set_foe[3]['speed'] = 2.4
set_foe[3]['scoreby'] = 132

## big fast
set_foe[4]['img'] = imgFoe5
set_foe[4]['health'] =28
set_foe[4]['attack'] = 11
set_foe[4]['range'] = 1
set_foe[4]['speed'] = 1.9
set_foe[4]['scoreby'] = 179

## big fast
set_foe[5]['img'] = imgFoe6
set_foe[5]['health'] = 139
set_foe[5]['attack'] = 14
set_foe[5]['range'] = 1
set_foe[5]['speed'] = 1.8
set_foe[5]['scoreby'] = 278

## huge fast one - boss
set_foe[6]['img'] = imgFoe7
set_foe[6]['health'] = 2500
set_foe[6]['attack'] = 23
set_foe[6]['range'] = 1
set_foe[6]['speed'] = 3
set_foe[6]['scoreby'] = 13273

################################################################################
## Item Presets
################################################################################
## imgs, type
################################################################################

set_item[0]['img'] = imgMoney
set_item[0]['type'] = 0

set_item[1]['img'] = imgItem
set_item[1]['type'] = 1

set_item[2]['img'] = imgItem2
set_item[2]['type'] = 2

################################################################################
## Event List Setup
################################################################################
## waves is list of scripted events
################################################################################

## Stage 1
## 0 and 1
waves = []
waves.append(["warn",0])
waves.append(["summon",FPS*3,[[0,25]]])
waves.append(["summon",FPS,[[0,10]]])
waves.append(["summon",FPS,[[0,10]]])
waves.append(["wait",FPS*5])
waves.append(["warn",0])
waves.append(["summon",FPS*3,[[0,10],[1,5]]])
waves.append(["summon",FPS*2,[[1,10]]])
waves.append(["summon",FPS*2,[[0,10]]])
waves.append(["wait",FPS*99999])
waves.append(["timer",0])
waves.append(["end",FPS*5])

## Stage 2
## 0 and 1 and 2
waves.append(["warn",0])
waves.append(["summon",FPS*3,[[0,10],[1,5]]])
waves.append(["summon",FPS,[[0,10]]])
waves.append(["summon",FPS,[[1,10]]])
waves.append(["summon",FPS,[[0,10]]])
waves.append(["wait",FPS*10])
waves.append(["warn",0])
waves.append(["summon",FPS*3,[[0,10],[2,5]]])
waves.append(["summon",FPS,[[1,10]]])
waves.append(["summon",FPS,[[1,10]]])
waves.append(["summon",FPS,[[2,10]]])
waves.append(["wait",FPS*10])
waves.append(["warn",0])
waves.append(["summon",FPS*3,[[0,10],[1,5]]])
waves.append(["summon",FPS,[[2,10]]])
waves.append(["summon",FPS,[[1,10]]])
waves.append(["summon",FPS,[[0,10]]])
waves.append(["wait",99999])
waves.append(["timer",0])
waves.append(["end",FPS*5])

## Stage 3
## 0 and 1 and 2 and 3
waves.append(["warn",0])
waves.append(["summon",FPS*3,[[3,10],[2,5]]])
waves.append(["summon",FPS,[[1,10]]])
waves.append(["summon",FPS,[[1,10]]])
waves.append(["summon",FPS,[[3,10]]])
waves.append(["summon",FPS,[[2,10]]])
waves.append(["summon",FPS,[[2,10]]])
waves.append(["wait",FPS*10])
waves.append(["warn",0])
waves.append(["summon",FPS*3,[[2,10],[3,5]]])
waves.append(["summon",FPS,[[2,10]]])
waves.append(["summon",FPS,[[1,10]]])
waves.append(["summon",FPS,[[3,10]]])
waves.append(["summon",FPS,[[3,10]]])
waves.append(["summon",FPS,[[2,10]]])
waves.append(["wait",FPS*10])
waves.append(["warn",0])
waves.append(["summon",FPS*3,[[2,10],[3,5]]])
waves.append(["summon",FPS,[[2,10]]])
waves.append(["summon",FPS,[[1,10]]])
waves.append(["summon",FPS,[[3,10]]])
waves.append(["summon",FPS,[[3,10]]])
waves.append(["summon",FPS,[[2,10]]])
waves.append(["wait",99999])
waves.append(["timer",0])
waves.append(["end",FPS*5])

## Stage 4
## 0 and 1 and 2 and 3 and 4
waves.append(["warn",0])
waves.append(["summon",FPS*3,[[0,10],[1,5]]])
waves.append(["summon",FPS,[[0,10]]])
waves.append(["summon",FPS,[[1,10]]])
waves.append(["summon",FPS,[[2,10]]])
waves.append(["summon",FPS,[[4,10]]])
waves.append(["summon",FPS,[[1,10]]])
waves.append(["summon",FPS,[[3,10]]])
waves.append(["summon",FPS,[[2,10],[2,5]]])
waves.append(["summon",FPS,[[4,10]]])
waves.append(["summon",FPS,[[1,10]]])
waves.append(["summon",FPS,[[3,10]]])
waves.append(["summon",FPS,[[2,10],[3,5]]])
waves.append(["summon",FPS,[[1,10]]])
waves.append(["summon",FPS,[[3,10]]])
waves.append(["summon",FPS,[[2,10]]])
waves.append(["summon",FPS,[[1,10]]])
waves.append(["summon",FPS,[[2,10]]])
waves.append(["wait",99999])
waves.append(["timer",0])
waves.append(["end",FPS*5])

## Stage 5
## 1 and 2 and 3 and 4 and 5
waves.append(["warn",0])
waves.append(["summon",FPS*3,[[5,10]]])
waves.append(["summon",FPS,[[4,10]]])
waves.append(["summon",FPS,[[3,10]]])
waves.append(["summon",FPS,[[2,10]]])
waves.append(["summon",FPS,[[1,10]]])
waves.append(["summon",FPS,[[5,5]]])
waves.append(["wait",99999])
waves.append(["warn",0])
waves.append(["summon",FPS*3,[[5,10]]])
waves.append(["summon",FPS,[[4,10]]])
waves.append(["summon",FPS,[[3,10]]])
waves.append(["summon",FPS,[[2,10]]])
waves.append(["summon",FPS,[[1,10]]])
waves.append(["summon",FPS,[[5,5]]])
waves.append(["wait",99999])
waves.append(["warn",0])
waves.append(["summon",FPS*3,[[5,10]]])
waves.append(["summon",FPS,[[4,10]]])
waves.append(["summon",FPS,[[3,10]]])
waves.append(["summon",FPS,[[2,10]]])
waves.append(["summon",FPS,[[1,10]]])
waves.append(["summon",FPS,[[5,5]]])
waves.append(["wait",99999])
waves.append(["timer",0])
waves.append(["end",FPS*5])

## Final Stage
## 0~6
waves.append(["warn",0])
waves.append(["summon",FPS*3,[[0,5],[1,5],[2,5],[3,5],[4,10],[5,10]]])
waves.append(["summon",FPS*2,[[6,1]]])
waves.append(["summon",FPS*2,[[0,5],[1,5],[2,5],[3,10],[4,10],[5,5]]])
waves.append(["wait",FPS*10])
waves.append(["warn",0])
waves.append(["summon",FPS*3,[[0,5],[1,5],[2,5],[3,5],[4,10],[5,10]]])
waves.append(["wait",FPS*5])
waves.append(["warn",0])
waves.append(["summon",FPS*3,[[0,5],[1,5],[2,5],[3,15],[4,5],[5,15]]])
waves.append(["wait",99999])
waves.append(["timer",0])
waves.append(["realend",150])

################################################################################
## Entity Class Setup
################################################################################

class entity():

	################################################
	### Some Default values
	################################################
	
	type = 0
	img = None
	sizex, sizey = 0,0
	posx, posy = 0,0
	health = 1
	maxhealth = 10
	range = 1
	attack = 1
	angle = 0
	speed = 0
	scoreby = 10
	
	################################################
	### Class Init Work - convert preset into vars
	################################################
	
	def __init__(self, preset):
		if preset.has_key('type'):		self.type = preset['type']
		if preset.has_key('img'):		self.img = preset['img']
		if preset.has_key('img2'):		self.img2 = preset['img2']
		if preset.has_key('img3'):		self.img3 = preset['img3']
		if preset.has_key('img'):		self.sizex = self.img.get_width()
		if preset.has_key('img'):		self.sizey = self.img.get_height()
		if preset.has_key('sizex'):		self.sizex = preset['sizex']
		if preset.has_key('sizey'):		self.sizey = preset['sizey']
		if preset.has_key('posx'):		self.posx = preset['posx']
		if preset.has_key('posy'):		self.posy =preset['posy']
		if preset.has_key('health'):	self.health = preset['health']
		if preset.has_key('attack'):	self.attack = preset['attack']
		if preset.has_key('range'):		self.range = preset['range']
		if preset.has_key('angle'):		self.angle = preset['angle']
		if preset.has_key('speed'):		self.speed = preset['speed']
		if preset.has_key('scoreby'):	self.scoreby = preset['scoreby']
	
	################################################
	### Check Functions (functions that checks a state (boolean))
	################################################	

	# returns two booleans of whether self is within the boundary
	def checkOnScreen(self):
		x, y = False, False
		if self.posx + self.sizex < RESX and self.posx > 0:
			x = True
		if self.posy + self.sizey < RESY and self.posy > 0:
			y = True
		
		if x and y:
			return True
		else:
			return False

	# args = the target
	# returns boolean of whether it is hit or not
	def checkCollision(self, foe):
		return (self.getDistance(foe) <= 0)
	
	# args = the target
	# returns boolean of whether it is in preset range
	def checkRange(self,foe):
		return (self.getDistance(foe) <= self.range)

	################################################
	### Do Functions (functions that actually do something)
	################################################

	# args = the target
	# attacks the foe and lowers their hp
	def doAttack(self, foe):
		if self.checkRange(foe):
			foe.health -= self.attack

	# args = screen resolution (default: 800, 600)
	# use the outer limit (screen size) to bounce around
	def doBounceAround(self):
		if self.posx + self.sizex + self.movebyx < RESX-1 and self.posx + self.movebyx > +1:
			self.posx += self.movebyx
		if self.posy + self.sizey + self.movebyy < RESY-1 and self.posy + self.movebyy > +1:
			self.posy += self.movebyy

		if self.posx + self.sizex + self.movebyx >= RESX-1:
			self.movebyx *= -1.0
		elif self.posx + self.movebyx <= +1:
			self.movebyx *= -1.0
		elif self.posy + self.sizey + self.movebyy >= RESY-1:
			self.movebyy *= -1.0		
		elif self.posy + self.movebyy <= +1:
			self.movebyy *= -1.0
	
	# args = which item effect
	# do item effect
	def doItem(self, which):
		if which == 0:
			game['money'] += random.randint(8,13)
		elif which == 1:
			if char.health + 3 <= char.state['maxhealth']:
				char.health += 3
				wavOYes.play()
		elif which == 2:
			char.state['nade'] += 1
			wavOYes.play()
			
	# args = limit
	# change position according to moveby value
	def doMove(self):
		y = self.speed * math.sin(self.angle) * -1
		x = self.speed * math.cos(self.angle)
		self.posx += x
		self.posy += y
	
	# change position according to moveby value
	def doMoveTo(self,x,y):
		self.posx += x
		self.posy += y

	def doNade(self):
		which = 0
		self.doShootMulti(0, char.state['nadeby'], 360)
	
	def doShootMulti(self, which, many, width):
		MOUSEX, MOUSEY = pygame.mouse.get_pos()
		mouseangle = char.getAngle(MOUSEX, MOUSEY)
		if many > 1:
			theta = width*math.pi/180.0
			baseangle = mouseangle - theta/2
			increment = theta / (many-1)
		else:
			baseangle = mouseangle
			increment = 0
		for i in range(many):
			temp_set = set_bullet[which]
			temp_set['angle'] = baseangle + increment * i
			temp_set['posx'] = char.posx + char.sizex / 2 - set_bullet[which]['img'].get_width()/2
			temp_set['posy'] = char.posy + char.sizey / 2 - set_bullet[which]['img'].get_height()/2
			bullets.append(entity(temp_set))
			
	################################################		
	## Get Functions (functions that returns values)
	################################################

	# args = the destination coordinates
	# returns the angle toward the destination
	def getAngle(self, desx, desy):
		distancex = desx - (self.posx + self.sizex /2)
		distancey = desy - (self.posy + self.sizey /2)
		distancey *= -1
		return math.atan2(distancey, distancex)

	# args = the target
	# returns the outer distance to the target		
	def getDistance(self, foe):
		centerx = self.posx + self.sizex / 2
		centery = self.posy + self.sizey / 2
		foecenterx = foe.posx + foe.sizex / 2
		foecentery = foe.posy + foe.sizey / 2
		diffx = centerx - foecenterx
		diffy = centery - foecentery
		distance = math.hypot(diffx, diffy)
		
		sizes = (self.sizex + self.sizey) / 4
		foesizes = (foe.sizex + foe.sizey) / 4
		
		outerdistance = distance - sizes - foesizes
		
		return outerdistance
		
	################################################
	## Set Functions (functions that sets values)
	################################################

	def setRandomMoveby(self):
		self.movebyx = random.uniform(-self.maxspeed, self.maxspeed) 
		self.movebyy = random.uniform(-self.maxspeed, self.maxspeed)
		
	def setRandomPos(self):
		if random.randint(0,1):					# top and bottom sides
			if random.randint(0,1):				# top side
				posx = RESX * random.random()
				posy = self.sizey/2
			else:								# bottom side
				posx = RESX * random.random()
				posy = RESY - self.sizey*1.5
		else:									# left and right sides
			if random.randint(0,1):				# left side
				posx = self.sizex/2
				posy = RESY * random.random()
			else:								# right side
				posx = RESX - self.sizex*1.5
				posy = RESY * random.random()
		
		self.posx, self.posy = posx, posy
		
################################################################################
## Function Setup
################################################################################

def appendList(what, towhat):
	for each in what:
		towhat.append(each)

def changeScore(howmuch):
	global iScore
	global iPoint
	
	if howmuch < 0:
		iScore += howmuch
	else:
		iScore += howmuch
		iPoint += howmuch

def createFoeList(howmany,preset):
	foeArray = []
	for i in range(howmany):
		foeArray.append(entity(preset))
		foeArray[i].setRandomPos()
	return foeArray
	
def createItem(thing):
	if random.randint(0,25):
		which = 0
	else:
		if random.randint(0,5):
			which = 1
		else:
			which = 2

	if random.randint(0,2):		
		newitem = entity(set_item[which])
		newitem.posx = thing.posx
		newitem.posy = thing.posy
		items.append(newitem)
	
def fadeOutIn(pic):
	for i in range (10):
		screen.blit(imgBlack, (0,0))
		pygame.display.flip()
		time.sleep(0.05)
	for i in range(10):
		screen.blit(pic, (0,0))
		for ii in range(6-i):
			screen.blit(imgBlack, (0,0))
		pygame.display.flip()
		time.sleep(0.05)

def startReload():
	char.state['reload'] = 1
	char.state['reloadtick'] = char.state['reloadby']
	wavReload.play()

def updateHighScore():

	if game['name'] == "NEWBIE":
		return

	slot = len(numbers)
	for i in range(len(numbers)):
		if game['score'] > int(numbers[i]):
			slot = i
			break
	
	names.insert(slot, game['name'].upper())
	numbers.insert(slot, str(game['score']))
	
	fileNames = open(PATHNAMES,"w")
	fileNumbers = open(PATHNUMBERS,"w")
	
	for i in names:		fileNames.write(i+"\n")
	for j in numbers: 	fileNumbers.write(j+"\n")

def upgrade(choice):
	char.state[choice] += upgradeby[choice]
	game['money'] -= upgradecost[choice] * (upgradenow[choice]+1)
	upgradenow[choice] += 1
	wavUpgrade.play()

def upgradeLvlLine(chioce):
	return str(upgradenow[chioce]) +"/"+ str(upgrademax[chioce])

def waitForKey():
	over = 0
	while 1:
		for events in pygame.event.get():
			if events.type == pygame.KEYDOWN:
				over = 1
				break
		if over:
			over = 0
			break

################################################################################
## Blit & Show Functions
################################################################################
## Function to blit stuff onto the screen
################################################################################

def blitBar():
	AMMOLINE = str(char.state['ammo'])+"/"+str(char.state['clip'])
	HEALTHLINE = str(char.health)+"/"+str(char.state['maxhealth'])
	
	screen.blit(imgBgBar,(0,585))
	screen.blit(fontSan.render(str(game['score']),True,(0,0,0)),(120,603))
	screen.blit(fontSanN.render("$"+str(game['money']),True,(48,10,10)),(230,606))
	screen.blit(fontSan.render(str(char.state['nade']),True,(0,0,0)),(390,603))
	screen.blit(fontSan.render(AMMOLINE,True,(0,0,0)),(545,603))
	screen.blit(fontSan.render(HEALTHLINE,True,(0,0,0)),(700,603))

def blitChar():
	if char.state['invinsible']:
		screen.blit(char.img2,(char.posx,char.posy))
	elif char.state['reload']:
		screen.blit(char.img3,(char.posx,char.posy))
	else:
		screen.blit(char.img,(char.posx,char.posy))

def blitHighScores(start):
	blitText("HiScores", start, 1)
	for i in range(5):
		blitText(names[i]+":"+numbers[i], start+50+50*i, 1)

def blitOver():
	screen.blit(imgRed, (0,0))
	blitText("GAME OVER!!", 100)
	blitText("HIT ESC TO QUIT", 150)
	blitHighScores(250)

def blitText(txt, y, w=0):
	if w: c = (255,255,255)
	else: c = (0,0,0)
	txtimg = fontName.render(txt,True,c)
	x = MIDX - txtimg.get_width()/2
	screen.blit(txtimg,(x,y))
	
def blitThings():
	for bullet in bullets:
		screen.blit(bullet.img,(bullet.posx,bullet.posy))
	for foe in foes:
		screen.blit(foe.img,(foe.posx,foe.posy))
	for item in items:
		screen.blit(item.img,(item.posx,item.posy))

def blitWin():
	screen.blit(imgWhite, (0,0))
	blitText("Congratulations!!", 100)
	blitText("You have beaten the game!!", 150)
	blitText("Hit Esc to Quit!!", 200)
	blitHighScores(250)	
	
def showEverything():
	screen.blit(imgBg, (0,0))
	blitChar()
	blitThings()
	blitBar()
	
	if game['over'] == 1:	blitOver()
	elif game['over'] == 2:	blitWin()
	
	pygame.display.flip()

def showNaming():
	screen.blit(imgNaming, (0,0))
	
	txt = fontName.render(game['name'],True,(255,255,255))
	x = MIDX - txt.get_width()/2
	y = MIDY - txt.get_height()/2
	
	screen.blit(txt,(x,y))
	
	pygame.display.flip()

def showShop():

	screen.blit(imgUpgrade, (0,0))
	
	screen.blit(fontSan.render(upgradeLvlLine('clip'),True,(0,0,0)),(115,140))
	screen.blit(fontSan.render(upgradeLvlLine('spread'),True,(0,0,0)),(300,140))
	screen.blit(fontSan.render(upgradeLvlLine('damage'),True,(0,0,0)),(480,140))
	screen.blit(fontSan.render(upgradeLvlLine('maxhealth'),True,(0,0,0)),(660,140))
	screen.blit(fontSan.render(upgradeLvlLine('rapid'),True,(0,0,0)),(115,340))
	screen.blit(fontSan.render(upgradeLvlLine('faster'),True,(0,0,0)),(300,340))
	
	if upgradenow['clip'] < upgrademax['clip']:
		screen.blit(fontSan.render("$"+str(upgradecost['clip'] * (upgradenow['clip']+1)),True,(0,0,0)),(115,170))
	if upgradenow['spread'] < upgrademax['spread']:
		screen.blit(fontSan.render("$"+str(upgradecost['spread'] * (upgradenow['spread']+1)),True,(0,0,0)),(300,170))
	if upgradenow['damage'] < upgrademax['damage']:
		screen.blit(fontSan.render("$"+str(upgradecost['damage'] * (upgradenow['damage']+1)),True,(0,0,0)),(480,170))
	if upgradenow['maxhealth'] < upgrademax['maxhealth']:
		screen.blit(fontSan.render("$"+str(upgradecost['maxhealth'] * (upgradenow['maxhealth']+1)),True,(0,0,0)),(660,170))
	if upgradenow['rapid'] < upgrademax['rapid']:
		screen.blit(fontSan.render("$"+str(upgradecost['rapid']),True,(0,0,0)),(115,370))
	if upgradenow['faster'] < upgrademax['faster']:
		screen.blit(fontSan.render("$"+str(upgradecost['faster']),True,(0,0,0)),(300,370))
	screen.blit(fontSan.render("$"+str(upgradecost['health'] * (char.state['maxhealth']-char.health)),True,(0,0,0)),(480,370))
	screen.blit(fontSan.render("$"+str(upgradecost['nade'] + char.state['nade'] * upgradecost['xtranade']),True,(0,0,0)),(660,370))

	blitBar()
	
	pygame.display.flip()

################################################################################
## Screen Functions Setup
################################################################################
## Functions that have its own screen apart from main game loop
################################################################################

def scrIntro():
	fadeOutIn(imgTitle)
	waitForKey()
	fadeOutIn(imgDisclaimer)
	waitForKey()
	fadeOutIn(imgStory)
	waitForKey()
	fadeOutIn(imgTutorial)
	waitForKey()

def scrNaming():
	while 1:
		pygame.event.pump()
		for events in pygame.event.get():
			if events.type == pygame.KEYDOWN:
				if events.key in range(pygame.K_a, pygame.K_z+1):
					game['name'] += ALPHABET[events.key-pygame.K_a].upper()
				if events.key == pygame.K_BACKSPACE:
					game['name'] = game['name'][:len(game['name'])-1]
				if events.key == pygame.K_RETURN and not game['name'] == "":
					game['name'] = game['name'].upper()
					if game['name'] == "NEWBIE":
						game['money'] += 1000
					return
		showNaming()

def scrShop():
	while 1:
		pygame.event.pump()
		for events in pygame.event.get():
			if events.type == pygame.KEYDOWN:
				if events.key == pygame.K_ESCAPE:
					return 0
				elif events.key == pygame.K_1 and upgradenow['clip'] < upgrademax['clip'] and game['money'] >= upgradecost['clip'] * (upgradenow['clip']+1):
					upgrade('clip')
				elif events.key == pygame.K_2 and upgradenow['spread'] < upgrademax['spread'] and game['money'] >= upgradecost['spread'] * (upgradenow['spread']+1):
					upgrade('spread')
				elif events.key == pygame.K_3 and upgradenow['damage'] < upgrademax['damage'] and game['money'] >= upgradecost['damage'] * (upgradenow['damage']+1):
					upgrade('damage')
				elif events.key == pygame.K_4 and upgradenow['maxhealth'] < upgrademax['maxhealth'] and game['money'] >= upgradecost['maxhealth'] * (upgradenow['maxhealth']+1):
					upgrade('maxhealth')
				elif events.key == pygame.K_5 and not upgradenow['rapid'] and game['money'] >= upgradecost['rapid'] * (upgradenow['rapid']+1):
					char.state['rapid'] = 1
					game['money'] -= upgradecost['rapid'] * (upgradenow['rapid']+1)
					upgradenow['rapid'] = 1
					wavUpgrade.play()
				elif events.key == pygame.K_6 and not upgradenow['faster'] and game['money'] >= upgradecost['faster'] * (upgradenow['faster']+1):
					char.speed += upgradeby['faster']
					game['money'] -= upgradecost['faster'] * (upgradenow['faster']+1)
					upgradenow['faster'] = 1
					wavUpgrade.play()
				elif events.key == pygame.K_7 and game['money'] >= upgradecost['health'] * (char.state['maxhealth']-char.health):
					game['money'] -= upgradecost['health'] * (char.state['maxhealth']-char.health)
					char.health = char.state['maxhealth']
					wavHeal.play()
				elif events.key == pygame.K_8 and game['money'] >= (upgradecost['nade'] + char.state['nade'] * upgradecost['xtranade']):
					game['money'] -= (upgradecost['nade'] + char.state['nade'] * upgradecost['xtranade'])
					char.state['nade'] += 1
					wavUpgrade.play()
				else:
					wavBuzzer.play()
		showShop()

def scrOutro():
	while 1:
		pygame.event.pump()
		for events in pygame.event.get():
			if events.type == pygame.KEYDOWN:
				if events.key == pygame.K_ESCAPE:
					sys.exit(0)
		showEverything()

################################################################################
## Char Preset
################################################################################
## imgs, size, pos, health, angle, speed
################################################################################

set_char['img'] = imgChar
set_char['img2'] = imgChar2
set_char['img3'] = imgChar3
set_char['posx'] = RESX / 2 - 25
set_char['posy'] = RESY / 2 - 25
set_char['attack'] = 2
set_char['health'] = 20
set_char['range'] = 1
set_char['angle'] = 0
set_char['speed'] = 3.5

################################################################################
## Object Init
################################################################################
## Set up character entity and its special attributes.
################################################################################

char = entity(set_char)
char.state = {}
char.state['invinsible'] = 0
char.state['invinsibleby'] = 90
char.state['invinsibletick'] = 0
char.state['reload'] = 0
char.state['reloadby'] = 60
char.state['reloadtick'] = 0
char.state['reloadwhich'] = 0
char.state['rapid'] = 0
char.state['nade'] = 1
char.state['nadeby'] = 100
char.state['ammo'] = 25
char.state['clip'] = 25
char.state['maxhealth'] = 30
char.state['spread'] = 1
char.state['damage'] = 1