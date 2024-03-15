import pygame
import sys, random
from pygame.math import Vector2


# Constants
CELL_SIZE = 40
CELL_NUMBER = 20
WIDTH = CELL_SIZE * CELL_NUMBER
HEIGHT = CELL_SIZE * CELL_NUMBER
FONTSIZE = 25
FRAMERATE = 60


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
		self.reset()
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
				# Direction between i+1 and i block
				previous_dir = block - self.body[index + 1]
				# Direction between i-1 and i block
				next_dir = self.body[index - 1] - block
				# Same horizontal component
				if (previous_dir.y == 0) and (next_dir.y == 0):
					screen.blit(self.body_horizontal, block_rect)
				# Same vertical component
				elif (previous_dir.x == 0) and (next_dir.x == 0):
					screen.blit(self.body_vertical, block_rect)
				else:
					# It exists 4 cases
					# 1 : next up and previous right or next left and previous down
					# 2 : next up and previous left or next right and previous down
					# 3 : next down and previous right or next left and previous up
					# 4 : next down and previous left or next right and previous up
					next_up = (next_dir.x == 0) and ((next_dir.y < 0) or (next_dir.y == CELL_NUMBER - 1))
					next_down = (next_dir.x == 0) and ((next_dir.y > 0) or (next_dir.y == -CELL_NUMBER + 1))
					next_right = (next_dir.y == 0) and ((next_dir.x > 0) or (next_dir.x == -CELL_NUMBER + 1))
					next_left = (next_dir.y == 0) and ((next_dir.x < 0) or (next_dir.x == CELL_NUMBER - 1))
					previous_up = (previous_dir.x == 0) and ((previous_dir.y < 0) or (previous_dir.y == CELL_NUMBER - 1))
					previous_down = (previous_dir.x == 0) and ((previous_dir.y > 0) or (previous_dir.y == -CELL_NUMBER + 1))
					previous_right = (previous_dir.y == 0) and ((previous_dir.x > 0) or (previous_dir.x == -CELL_NUMBER + 1))
					previous_left = (previous_dir.y == 0) and ((previous_dir.x < 0) or (previous_dir.x == CELL_NUMBER - 1))
					if (next_up and previous_left) or (next_right and previous_down):
						screen.blit(self.body_tr, block_rect)
					elif (next_up and previous_right) or (next_left and previous_down):
						screen.blit(self.body_tl, block_rect)
					elif (next_down and previous_left) or (next_right and previous_up):
						screen.blit(self.body_br, block_rect)
					elif (next_down and previous_right) or (next_left and previous_up):
						screen.blit(self.body_bl, block_rect)


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

	@staticmethod
	def check_coordinate(coord):
		return coord % CELL_NUMBER
	
	def update_direction(self, start, dir):
		# Update the direction
		new_head = start + dir
		checked_x = self.check_coordinate(new_head.x)
		checked_y = self.check_coordinate(new_head.y)
		new_head.update(checked_x, checked_y)
		return new_head
		
	def check_direction(self, dir):
		return self.update_direction(self.body[0], dir) != self.body[1]

	def move_snake(self):
		if self.new_block == True:
			body_copy = self.body[:]
		else:
			body_copy = self.body[:-1]
		new_head = self.update_direction(self.body[0], self._direction)
		body_copy.insert(0, new_head)
		self.body = body_copy[:]
		self.new_block = False
	
	@property
	def direction(self):
		return self._direction
	
	@direction.setter
	def direction(self, dir):
		# Has to be a Vector2
		assert type(dir) == Vector2
		# Cannot go into the body
		if self.check_direction(dir):
			self._direction = dir

	def add_block(self):
		self.new_block = True

	def play_crunch_sound(self):
		self.crunch_sound.play()

	def reset(self):
		self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
		self._direction = Vector2(0, 0)


class MAIN:
	def __init__(self):
		self.snake = SNAKE()
		self.fruit = FRUIT()
		self.score = 0

	def update(self):
		self.snake.move_snake()
		self.check_collision()
		self.check_fail()
		self.update_score()

	def draw_elements(self, screen):
		screen.fill((175, 215, 70))
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
	
	def update_score(self):
		if self.snake.direction != Vector2(0, 0):
			self.score = len(self.snake.body) - 3

	def draw_grass(self, screen):
		grass_color = (167, 209, 61)
		for row in range(CELL_NUMBER):
			for col in range(CELL_NUMBER):
				if (row % 2 == 0) and (col % 2 == 0):
					grass_rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
					pygame.draw.rect(screen, grass_color, grass_rect)
				if (row % 2 != 0) and (col % 2 != 0):
					grass_rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
					pygame.draw.rect(screen, grass_color, grass_rect)

	def draw_score(self, screen):
		score_text = str(self.score)
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
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
GAME_FONT = pygame.font.Font('Font/PoetsenOne-Regular.ttf', FONTSIZE)
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 140)

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

    
    main_game.draw_elements(screen)
    pygame.display.update()
    clock.tick(FRAMERATE)