import pygame
import sys,random
import enum
from pygame.math import Vector2


# Constants
CELL_SIZE = 20
CELL_NUMBER = 40

class Ori(enum.Enum):
	UP = 0
	DOWN = 1
	LEFT = 2
	RIGHT = 3

class FRUIT:
	def __init__(self):
		self.apple = pygame.image.load('Graphics/apple.png').convert_alpha()
		self.randomize()

	def draw_fruit(self, screen):
		fruit_rect = pygame.Rect(int(self.pos.x * CELL_SIZE), int(self.pos.y * CELL_SIZE), CELL_SIZE, CELL_SIZE)
		screen.blit(self.apple, fruit_rect)

	def randomize(self):
		self.x = random.randint(0, CELL_NUMBER - 1)
		self.y = random.randint(0, CELL_NUMBER - 1)
		self.pos = Vector2(self.x, self.y)


class SNAKE:
	def __init__(self):
		self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
		self.ori = [Ori.RIGHT, Ori.RIGHT, Ori.RIGHT]
		self.direction = Vector2(0, 0)
		self.new_block = False

		self.head_up = pygame.image.load('Graphics/head_up.png').convert_alpha()
		self.head_down = pygame.image.load('Graphics/head_down.png').convert_alpha()
		self.head_right = pygame.image.load('Graphics/head_right.png').convert_alpha()
		self.head_left = pygame.image.load('Graphics/head_left.png').convert_alpha()
		
		self.tail_up = pygame.image.load('Graphics/tail_up.png').convert_alpha()
		self.tail_down = pygame.image.load('Graphics/tail_down.png').convert_alpha()
		self.tail_right = pygame.image.load('Graphics/tail_right.png').convert_alpha()
		self.tail_left = pygame.image.load('Graphics/tail_left.png').convert_alpha()

		self.body_vertical = pygame.image.load('Graphics/body_vertical.png').convert_alpha()
		self.body_horizontal = pygame.image.load('Graphics/body_horizontal.png').convert_alpha()

		self.body_tr = pygame.image.load('Graphics/body_tr.png').convert_alpha()
		self.body_tl = pygame.image.load('Graphics/body_tl.png').convert_alpha()
		self.body_br = pygame.image.load('Graphics/body_br.png').convert_alpha()
		self.body_bl = pygame.image.load('Graphics/body_bl.png').convert_alpha()
		self.crunch_sound = pygame.mixer.Sound('Sound/crunch.wav')

	def draw_snake(self, screen):
		self.update_head_graphics()
		self.update_tail_graphics()

		for index,block in enumerate(self.body):
			x_pos = int(block.x * CELL_SIZE)
			y_pos = int(block.y * CELL_SIZE)
			block_rect = pygame.Rect(x_pos, y_pos, CELL_SIZE, CELL_SIZE)

			if index == 0:
				screen.blit(self.head, block_rect)
			elif index == len(self.body) - 1:
				screen.blit(self.tail, block_rect)
			else:
				previous_block = self.body[index + 1] - block
				next_block = self.body[index - 1] - block
				if previous_block.x == next_block.x:
					screen.blit(self.body_vertical,block_rect)
				elif previous_block.y == next_block.y:
					screen.blit(self.body_horizontal,block_rect)
				else:
					if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
						screen.blit(self.body_tl,block_rect)
					elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
						screen.blit(self.body_bl,block_rect)
					elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
						screen.blit(self.body_tr,block_rect)
					elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
						screen.blit(self.body_br,block_rect)

	def update_head_graphics(self):
		head_relation = self.body[1] - self.body[0]
		if head_relation == Vector2(1, 0): self.head = self.head_left
		elif head_relation == Vector2(-1, 0): self.head = self.head_right
		elif head_relation == Vector2(0, 1): self.head = self.head_up
		elif head_relation == Vector2(0, -1): self.head = self.head_down

	def update_tail_graphics(self):
		tail_relation = self.body[-2] - self.body[-1]
		if tail_relation == Vector2(1, 0): self.tail = self.tail_left
		elif tail_relation == Vector2(-1, 0): self.tail = self.tail_right
		elif tail_relation == Vector2(0, 1): self.tail = self.tail_up
		elif tail_relation == Vector2(0, -1): self.tail = self.tail_down

	def move_snake(self):
		if self.new_block == True:
			body_copy = self.body[:]
			body_copy.insert(0,body_copy[0] + self.direction)
			self.body = body_copy[:]
			self.new_block = False
		else:
			body_copy = self.body[:-1]
			body_copy.insert(0,body_copy[0] + self.direction)
			self.body = body_copy[:]

	def add_block(self):
		self.new_block = True

	def play_crunch_sound(self):
		self.crunch_sound.play()

	def reset(self):
		self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
		self.direction = Vector2(0, 0)


class MAIN:
	def __init__(self):
		self.snake = SNAKE()
		self.fruit = FRUIT()

	def update(self):
		self.snake.move_snake()
		self.check_collision()
		self.check_fail()

	def draw_elements(self, screen):
		self.draw_grass(screen)
		self.fruit.draw_fruit(screen)
		self.snake.draw_snake(screen)
		self.draw_score(screen)

	def check_collision(self):
		if self.fruit.pos == self.snake.body[0]:
			self.fruit.randomize()
			self.snake.add_block()
			self.snake.play_crunch_sound()

		for block in self.snake.body[1:]:
			if block == self.fruit.pos:
				self.fruit.randomize()

	def check_fail(self):
		if self.snake.body[0] in self.snake.body[1:]:
			self.game_over()
		
	def game_over(self):
		self.snake.reset()

	def draw_grass(self, screen):
		grass_color = (167, 209, 61)
		

	def draw_score(self, screen):
		score_text = str(len(self.snake.body) - 3)
		score_surface = GAME_FONT.render(score_text, True, (56, 74, 12))
		score_x = int(CELL_SIZE * CELL_NUMBER - 60)
		score_y = int(CELL_SIZE * CELL_NUMBER - 40)
		score_rect = score_surface.get_rect(center = (score_x, score_y))
		apple_rect = self.fruit.apple.get_rect(midright = (score_rect.left, score_rect.centery))
		bg_rect = pygame.Rect(apple_rect.left, apple_rect.top, apple_rect.width + score_rect.width + 6, apple_rect.height)

		pygame.draw.rect(screen, (167, 209, 61), bg_rect)
		screen.blit(score_surface, score_rect)
		screen.blit(self.fruit.apple, apple_rect)
		pygame.draw.rect(screen, (56, 74, 12), bg_rect, 2)

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
screen = pygame.display.set_mode((CELL_NUMBER * CELL_SIZE, CELL_NUMBER * CELL_SIZE))
clock = pygame.time.Clock()
GAME_FONT = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 25)
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

main_game = MAIN()
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                main_game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_RIGHT:
                main_game.snake.direction = Vector2(1, 0)
            if event.key == pygame.K_DOWN:
                main_game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_LEFT:
                main_game.snake.direction = Vector2(-1, 0)

    screen.fill((175, 215, 70))
    main_game.draw_elements(screen)
    pygame.display.update()
    clock.tick(60)