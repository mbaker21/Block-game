import pygame
import random
import sys
import math

pygame.init()

WIDTH = 800
HEIGHT = 600

pygame.display.set_caption('Block Game')

VLIGHT_BLUE = (217, 255, 255)
PASTEL_YELLOW = (255,252,166)
LIGHT_PINK = (255, 182, 188)
WHITE = (255, 255, 255)
BACKGROUND_COLOR = (0, 0, 0)

#Player
player_size = 40
player_pos = [370, 480]

ENEMY_SPEED = 10

#Bullet
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 40
bulletstate = 'ready'

BULLET_SPEED = 17

screen = pygame.display.set_mode((WIDTH, HEIGHT))

game_over = False

score = 0

clock = pygame.time.Clock()

myFont = pygame.font.SysFont("monospace", 35)

#Enemy
enemy_size = 45
enemy_pos = [random.randint(0,WIDTH - enemy_size), 0]
enemy = pygame.draw.rect(screen, VLIGHT_BLUE, (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))
enemy_list = [enemy, enemy_pos]

def set_level(score, ENEMY_SPEED):
	if score < 40:
		ENEMY_SPEED = 3
	elif score < 70:
		ENEMY_SPEED = 5
	elif score < 100:
		ENEMY_SPEED = 7
	else:
		ENEMY_SPEED = 10
	return ENEMY_SPEED

def drop_enemies(enemy_list):
	delay = random.random()
	if len(enemy_list) < 10 and delay < 0.1:
		x_pos = random.randint(0, WIDTH-enemy_size)
		y_pos = 0
		enemy_list.append([x_pos, y_pos])

def draw_enemy(enemy_list, enemy):
	for enemy_pos in enemy_list:
		pygame.draw.rect(screen, VLIGHT_BLUE, (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))

def update_enemy_positions(enemy_list, score):
	for idx, enemy_pos in enumerate(enemy_list):
		if enemy_pos[1] >= 0 and enemy_pos[1] < HEIGHT:
			enemy_pos[1] += ENEMY_SPEED
		else:
			enemy_list.pop(idx)
			score += 1
	return score

def collision_bullet(enemy_pos, enemy_list, bulletX, bulletY):
	for enemy_pos in enemy_list:
		if isCollision(enemy, bulletX, bulletY):
			return True
	return False
	
def collision_check(enemy_list, player_pos):
	for enemy_pos in enemy_list:
		if detect_collision(enemy_pos, player_pos):
			return True
	return False

def detect_collision(player_pos, enemy_pos):
	p_x = player_pos[0]
	p_y = player_pos[1]

	e_x = enemy_pos[0]
	e_y = enemy_pos[1]

	if (e_x >= p_x and e_x < (p_x + player_size)) or (p_x >= e_x and p_x < (e_x + enemy_size)):
		if (e_y >= p_y and e_y < (p_y + player_size)) or (p_y >= e_y and p_y < (e_y + enemy_size)):
			return True
	return False

def fire_bullet(x, y):
	#Declare balletstate as a global if it needs changed
	global bulletstate
	bulletstate = 'fire'
		#Move the bullet to the just above the player
	pygame.draw.circle(screen, PASTEL_YELLOW, (x + 15, y - 5), 5)

def isCollision(enemy_pos, bulletX, bulletY):
	e_x = enemy_pos[0]
	e_y = enemy_pos[1]

	distance = math.sqrt(math.pow(e_x - bulletX,2) + (math.pow(e_y - bulletY,2)))
	if distance < 27 :
		return True
	else:
		return False

while not game_over:

	for event in pygame.event.get():
	
		if event.type == pygame.QUIT:
				sys.exit()

		if event.type == pygame.KEYDOWN:

			x = player_pos[0]
			y = player_pos[1]

			if event.key == pygame.K_LEFT:
				x -= player_size
			if event.key == pygame.K_RIGHT:
				x += player_size
			if event.key == pygame.K_SPACE:
				bulletX = x
				fire_bullet(bulletX, bulletY)

			player_pos = [x, y]


	screen.fill(BACKGROUND_COLOR)
	if enemy_pos[1] >= 0 and enemy_pos[1] < HEIGHT:
		enemy_pos[1] -= 20
	else:
		enemy_pos[1] = 1

	#Collision
	for enemy in enemy_list:
		if collision_bullet(enemy_pos, enemy_list, bulletX, bulletY):
			bulletY = 480
			bulletstate = 'ready'
			enemy_list.remove(enemy)
			score += 3
 
		#Bullet Movement
	if bulletY <= 0:
		bulletY =480
		bulletstate = 'ready'
		
	if bulletstate == 'fire':
		fire_bullet(bulletX, bulletY)
		bulletY -= bulletY_change

	drop_enemies(enemy_list)
	score = update_enemy_positions(enemy_list, score)
	ENEMY_SPEED = set_level(score, ENEMY_SPEED)

	text = "Score:" + str(score)
	label = myFont.render(text, 1, PASTEL_YELLOW)
	screen.blit(label, (WIDTH-200, HEIGHT-40))


	if collision_check(enemy_list, player_pos):
		game_over = True
		break

	draw_enemy(enemy_list, enemy)

	pygame.draw.rect(screen, LIGHT_PINK, (player_pos[0], player_pos[1], player_size, player_size))


	clock.tick(30)

	pygame.display.update()
