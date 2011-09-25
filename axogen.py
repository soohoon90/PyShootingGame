################################################################################
## Programmer's Block
################################################################################

# TITLE		AXOGEN
# CODER		HOON CHO
# VERSION	RC 1
# DATE		MAY 27

################################################################################
## Module Work
################################################################################

from ax import *

################################################################################
## Intro 
################################################################################

scrNaming()
if not game['name'] in names:	scrIntro()
scrShop()

################################################################################
## Game Loop
################################################################################

while 1:

	################################################
	## Tick Works
	################################################
	
	clock.tick(FPS)
	
	if len(waves) > 0:
		waves[0][1] -= 1
		if waves[0][0] == "wait" and len(foes) == 0:
			del waves[0]
		if waves[0][1] <= 0:
			if waves[0][0] == "warn":
				wavWarning.play()
			elif waves[0][0] == "summon":
				for summon in waves[0][2]:
					appendList(createFoeList(summon[1], set_foe[summon[0]]), foes)
			elif waves[0][0] == "end":
				wavFanfare.play()
				# scrEnd()
				scrShop()
			elif waves[0][0] == "timer":
				wavTing.play()
			elif waves[0][0] == "realend":
				game['over'] = 2
				break
			del waves[0]

	if char.state['invinsible']:
		char.state['invinsibletick'] -=1
		if char.state['invinsibletick'] <= 0:
			char.state['invinsible'] = 0
	
	if char.state['reload']:
		char.state['reloadtick'] -=1
		if char.state['reloadtick'] <= 0:
			char.state['reload'] = 0
			wavReloadDone.play()
			char.state['ammo'] = char.state['clip']
		
	if char.health <= 0:
		game['over'] = 1
		break

	################################################
	## Event Works
	################################################

	pygame.event.pump()
	for events in pygame.event.get():
		if events.type == pygame.KEYDOWN:
			if events.key == pygame.K_ESCAPE:
				sys.exit(0)
			if events.key == pygame.K_r and not char.state['reload']:
				startReload()
		if events.type == pygame.MOUSEBUTTONDOWN:
			if events.button == 1 and not char.state['rapid'] and char.state['ammo'] > 0 and not char.state['reload']:
				char.doShootMulti(char.state['damage'], char.state['spread'], 10)
				wavPistol.play()
				char.state['ammo'] -= 1
			if events.button == 3 and char.state['nade'] > 0:
				char.doNade()
				wavNade.play()
				char.state['nade'] -= 1
	
	keystate = pygame.key.get_pressed()
	mousestate = pygame.mouse.get_pressed()
	
	keyup = keystate[pygame.K_UP] or keystate[pygame.K_w]
	keydown = keystate[pygame.K_DOWN] or keystate[pygame.K_s]
	keyleft = keystate[pygame.K_LEFT] or keystate[pygame.K_a]
	keyright = keystate[pygame.K_RIGHT] or keystate[pygame.K_d]
	
	keymove = keyup or keydown or keyleft or keyright
	if keymove:

		if keyup and keyright:
			char.angle = math.pi / 4
		elif keyup and keyleft:
			char.angle = 3 * math.pi / 4
		elif keydown and keyright:
			char.angle = math.pi / 4 * -1
		elif keydown and keyleft:
			char.angle = 3 * math.pi / 4 * -1
		elif keyup:
			char.angle = math.pi / 2
		elif keydown:
			char.angle = math.pi / 2 * -1
		elif keyright:
			char.angle = 0
		elif keyleft:
			char.angle = math.pi
		
		char.doMove()
		
	if mousestate[0] and char.state['rapid'] and char.state['ammo'] > 0 and not char.state['reload']:
		char.doShootMulti(char.state['damage'], char.state['spread'], 30)
		char.state['ammo'] -= 1
		wavGattle.play()
		
	################################################
	## Bullet Works
	################################################

	for bullet in bullets:
		bullet.doMove()

	## if bullet miss and goes out of screen
	for i in range(len(bullets)-1, -1, -1):
		if not bullets[i].checkOnScreen():
			bullets.pop(i)
			game['misses'] += 1
			game['score'] -= 5
	
	## check if a bullet is in contact with a foe
	for i in range(len(bullets)-1, -1, -1):
		for ii in range(len(foes)):
			if bullets[i].checkCollision(foes[ii]):
				bullets[i].doAttack(foes[ii])
				game['score'] += 5
				game['hits'] += 1
				del bullets[i]
				break
	
	if char.state['ammo'] == 0 and not char.state['reload']:
		startReload()
		
	################################################
	## Foe Works
	################################################

	for i in range(len(foes)):
		foes[i].doMove()
		foes[i].angle = foes[i].getAngle(char.posx+char.sizex/2, char.posy+char.sizey/2)
		if not char.state['invinsible']:
			if foes[i].checkCollision(char):
				foes[i].doAttack(char)
				char.doAttack(foes[i])
				wavCrap.play()
				char.state['invinsible'] = 1
				char.state['invinsibletick'] = char.state['invinsibleby']
	
	## foe dies when hp is smaller than 0
	for i in range(len(foes)-1, -1, -1):
		if foes[i].health <= 0:
			game['score'] += foes[i].scoreby
			createItem(foes[i])
			game['kills'] += 1
			del foes[i]
	
	################################################
	## Item Works
	################################################
	for i in range(len(items)-1, -1, -1):
		if items[i].checkCollision(char):
			char.doItem(items[i].type)
			del items[i]
	
	showEverything()
	
################################################################################
## Post Game Script (Game Over)
################################################################################
updateHighScore()
scrOutro()