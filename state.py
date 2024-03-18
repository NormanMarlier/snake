import pygame
import random

from pygame.math import Vector2


class State():
    def __init__(self, game):
        self.game = game
        self.prev_state = None

    def update(self, delta_time, actions):
        pass

    def render(self, surface):
        pass

    def enter_state(self):
        if len(self.game.state_stack) > 1:
            self.prev_state = self.game.state_stack[-1]
        self.game.state_stack.append(self)
    
    def exit_state(self):
        self.game.state_stack.pop()


class Title(State):
	def __init__(self, game):
		super(Title, self).__init__(game)

		# Menu
		self.menu_color = (255, 255, 255)
		self.menu_options = {0: "Start", 1: "Ranking", 2: "Credits"}
		self.index = 0
		# Cursor
		self.cursor_color = (0, 255, 255)
		self.cursor_rect = pygame.Rect(0, 0, 30, 30)
		self.cursor_pos_y = self.game.GAME_H//2 - 15
		self.cursor_rect.x, self.cursor_rect.y = self.game.GAME_W//4 + 10, self.cursor_pos_y

	def update(self, delta_time, actions):
		self.update_cursor(actions)
		if actions["RETURN"]:
			self.transition_state()
		self.game.reset_keys()
	
	def update_cursor(self, actions):
		if actions["DOWN"]:
			self.index = (self.index + 1) % len(self.menu_options)
		elif actions["UP"]:
			self.index = (self.index - 1) % len(self.menu_options)
		self.cursor_rect.y = self.cursor_pos_y + (self.index * 32)
	
	def transition_state(self):
		if self.menu_options[self.index] == "Start":
			new_state = StartingMenu(self.game)
			new_state.enter_state()
		elif self.menu_options[self.index] == "Ranking":
			new_state = RankingMenu(self.game)
			new_state.enter_state()
		elif self.menu_options[self.index] == "Credits":
			new_state = CreditsMenu(self.game)
			new_state.enter_state()
	
	def render_menu(self, surface):
		for index, val in zip(range(len(self.menu_options)), self.menu_options.values()):
			y = self.game.GAME_H//2 + index * 32
			self.game.draw_text(surface, str(val), (255, 255, 255), self.game.GAME_W//2, y)
	
	def render(self, surface):
		surface.fill((0, 0, 0))
		self.game.draw_text(surface, "Snake", (255, 255, 255), self.game.GAME_W//2, self.game.GAME_H//4)
		pygame.draw.rect(surface, self.cursor_color, self.cursor_rect)
		self.render_menu(surface)


class StartingMenu(State):
	def __init__(self, game):
		super(StartingMenu, self).__init__(game)
		self.game.player_name = ""

	def update(self, delta_time, actions):
		self.update_character(actions)

		if actions["RETURN"] and len(self.game.player_name) > 0:
			new_state = GameWorld(self.game)
			new_state.enter_state()
		
		self.game.reset_keys()
	
	def update_character(self, actions):
		if actions["character"]: self.game.player_name += actions["character"]
		elif actions["BACKSPACE"]: self.game.player_name = self.game.player_name[:-1]
	
	def render(self, surface):
		surface.fill((0, 0, 0))
		text = "Name: " + self.game.player_name
		self.game.draw_text(surface, text, (255, 255, 255), self.game.GAME_W//2, self.game.GAME_H//2)


class CreditsMenu(State):
	def __init__(self, game):
		super(CreditsMenu, self).__init__(game)
	
	def update(self, delta_time, actions):
		if actions["RETURN"]:
			self.exit_state()
		self.game.reset_keys()
	
	def render(self, surface):
		surface.fill((0, 0, 0))
		self.game.draw_text(surface, "CREDITS", (255, 255, 255), self.game.GAME_W//2, self.game.GAME_H//2)
		self.game.draw_text(surface, "made by me", (255, 255, 255), self.game.GAME_W//2, self.game.GAME_H//2 + 30)


class RankingMenu(State):
	def __init__(self, game):
		super(RankingMenu, self).__init__(game)
		self.game.load_score()

	def update(self, delta_time, actions):
		if actions["RETURN"]:
			self.exit_state()
		self.game.reset_keys()

	def render(self, surface):
		surface.fill((0, 0, 0))
		if bool(self.game.sl_manager.ranking):
			
			for i, (k, v) in enumerate(zip(self.game.sl_manager.ranking.keys(), self.game.sl_manager.ranking.values())):
				text = str(len(self.game.sl_manager.ranking) - i) + ". " + str(k) + ": " + str(v)
				pos_y = self.game.GAME_H//2 - i * 32
				self.game.draw_text(surface, text, (255, 255, 255), self.game.GAME_W//2, pos_y)
		else:
			self.game.draw_text(surface, "There are no ranking yet !", (255, 255, 255), self.game.GAME_W//2, self.game.GAME_H//2)
			

class PauseMenu(State):
	def __init__(self, game):
		super(PauseMenu, self).__init__(game)

		# Color
		self.menu_color = (0, 0, 0)
		# Rectangle
		self.menu_rect = pygame.Rect(0, 0, self.game.GAME_W//4, self.game.GAME_H//4)
		self.menu_rect.center = (self.game.GAME_W//2, self.game.GAME_H//2)
		# Set the menu options
		self.menu_options = {0: "Restart", 1: "Exit"}
		self.index = 0
		# Cursor
		self.cursor_color = (255, 255, 255)
		self.cursor_rect = pygame.Rect(0, 0, 20, 20)
		self.cursor_pos_y = self.menu_rect.y + 38
		self.cursor_rect.x, self.cursor_rect.y = self.menu_rect.x + 10, self.cursor_pos_y
	
	def update(self, delta_time, actions):
		self.update_cursor(actions)
		if actions["RETURN"]:
			self.transition_state()
		self.game.reset_keys()
	
	def update_cursor(self, actions):
		if actions["DOWN"]:
			self.index = (self.index + 1) % len(self.menu_options)
		elif actions["UP"]:
			self.index = (self.index - 1) % len(self.menu_options)
		self.cursor_rect.y = self.cursor_pos_y + (self.index * 32)
	
	def transition_state(self):
		if self.menu_options[self.index] == "Restart":
			self.exit_state()
		elif self.menu_options[self.index] == "Exit":
			self.game.save_score()
			while len(self.game.state_stack) > 1:
				self.game.state_stack.pop()
	
	def render_menu(self, surface):
		top_y = self.menu_rect.y + 47
		for index, val in zip(range(len(self.menu_options)), self.menu_options.values()):
			y = top_y + index * 32
			self.game.draw_text(surface, str(val), (255, 255, 255), self.game.GAME_W//2, y)

	def render(self, surface):
		self.prev_state.render(surface)
		pygame.draw.rect(surface, self.menu_color, self.menu_rect)
		pygame.draw.rect(surface, self.cursor_color, self.cursor_rect)
		self.render_menu(surface)
		

class GameWorld(State):
	def __init__(self, game):
		super(GameWorld, self).__init__(game)
		
		self.player = Player(self.game)
        # Grass color
		self.grass_dark_color = (175, 215, 70)
		self.grass_light_color = (167, 209, 61)
		# Apple
		self.fruit = Fruit(self.game)
	
	def check_collision(self):
		if self.fruit.pos == self.player.body[0]:
			self.fruit.randomize()
			self.player.add_block()
			self.player.play_crunch_sound()

		while self.fruit.pos in self.player.body:
			self.fruit.randomize()

	def check_fail(self):
		if self.player.body[0] in self.player.body[1:]:
			self.game.save_score()
			self.player.reset()
    
	def update(self, delta_time, actions):
		if actions["SPACE"]:
			# Set direction to 0
			self.player.direction = Vector2(0, 0)
			new_state = PauseMenu(self.game)
			new_state.enter_state()
		self.player.update(delta_time, actions)
		self.check_collision()
		self.check_fail()
		self.update_score()
		self.game.reset_keys()
	
	def update_score(self):
		self.game.score = len(self.player.body) - 3
	
	def render_score(self, surface):
		score_text = str(self.game.score)
		score_surface = self.game.font.render(score_text, True, (56, 74, 12))
		score_x = int(self.game.CELL_SIZE * self.game.CELL_NUMBER - 60)
		score_y = int(self.game.CELL_SIZE * self.game.CELL_NUMBER - 40)
		score_rect = score_surface.get_rect(center = (score_x, score_y))
		apple_rect = self.game.apple.get_rect(midright = (score_rect.left, score_rect.centery))
		bg_rect = pygame.Rect(apple_rect.left, apple_rect.top, apple_rect.width + score_rect.width + 6, apple_rect.height)

		pygame.draw.rect(surface, (167, 209, 61), bg_rect)
		surface.blit(score_surface, score_rect)
		surface.blit(self.game.apple, apple_rect)
		pygame.draw.rect(surface, (56, 74, 12), bg_rect, 2)

	def render(self, surface):
		surface.fill(self.grass_dark_color)
		self.draw_grass(surface)
		self.fruit.render(surface)
		self.player.render(surface)
		self.render_score(surface)
    
	def draw_grass(self, surface):
		for row in range(self.game.CELL_NUMBER):
			for col in range(self.game.CELL_NUMBER):
				if (row % 2 == 0) and (col % 2 == 0):
					grass_rect = pygame.Rect(col * self.game.CELL_SIZE, row * self.game.CELL_SIZE, self.game.CELL_SIZE, self.game.CELL_SIZE)
					pygame.draw.rect(surface, self.grass_light_color, grass_rect)
				if (row % 2 != 0) and (col % 2 != 0):
					grass_rect = pygame.Rect(col * self.game.CELL_SIZE, row * self.game.CELL_SIZE, self.game.CELL_SIZE, self.game.CELL_SIZE)
					pygame.draw.rect(surface, self.grass_light_color, grass_rect)


class Player():
	def __init__(self, game):
		self.game = game
		self.reset()
		self.new_block = False
		self.speed = 0.17 # s/cell

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
		
	def update(self, delta_time, actions):
		# Update actions
		self.update_actions(actions)
		# Update time
		self.acc_move += delta_time
		# Move snake
		if (self.acc_move >= self.speed) and (self.direction != Vector2(0, 0)):
			self.move_snake()
			self.acc_move = 0.
	
	def update_actions(self, actions):
		if actions["UP"]:
			self.direction = Vector2(0, -1)
		elif actions["DOWN"]:
			self.direction = Vector2(0, 1)
		elif actions["LEFT"]:
			self.direction = Vector2(-1, 0)
		elif actions["RIGHT"]:
			self.direction = Vector2(1, 0)

	def render(self, surface):
		self.draw_snake(surface)

	def draw_snake(self, surface):
		self.update_head_graphics()
		self.update_tail_graphics()

		for index,block in enumerate(self.body):
			x_pos = int(block.x * self.game.CELL_SIZE)
			y_pos = int(block.y * self.game.CELL_SIZE)
			block_rect = pygame.Rect(x_pos, y_pos, self.game.CELL_SIZE, self.game.CELL_SIZE)

			if index == 0:
				surface.blit(self.head, block_rect)
			elif index == len(self.body) - 1:
				surface.blit(self.tail, block_rect)
			else:
				# Direction between i+1 and i block
				previous_dir = block - self.body[index + 1]
				# Direction between i-1 and i block
				next_dir = self.body[index - 1] - block
				# Same horizontal component
				if (previous_dir.y == 0) and (next_dir.y == 0):
					surface.blit(self.body_horizontal, block_rect)
				# Same vertical component
				elif (previous_dir.x == 0) and (next_dir.x == 0):
					surface.blit(self.body_vertical, block_rect)
				else:
					# It exists 4 cases
					# 1 : next up and previous right or next left and previous down
					# 2 : next up and previous left or next right and previous down
					# 3 : next down and previous right or next left and previous up
					# 4 : next down and previous left or next right and previous up
					next_up = (next_dir.x == 0) and (next_dir.y < 0)
					next_down = (next_dir.x == 0) and (next_dir.y > 0)
					if next_dir.y == self.game.CELL_NUMBER - 1:
						next_up = True
						next_down = False
					if next_dir.y == -self.game.CELL_NUMBER + 1:
						next_up = False
						next_down = True
					next_right = (next_dir.y == 0) and (next_dir.x > 0)
					next_left = (next_dir.y == 0) and (next_dir.x < 0)
					if next_dir.x == self.game.CELL_NUMBER - 1:
						next_right = False
						next_left = True
					if next_dir.x ==  -self.game.CELL_NUMBER + 1:
						next_right = True
						next_left = False
					previous_up = (previous_dir.x == 0) and (previous_dir.y < 0)
					previous_down = (previous_dir.x == 0) and (previous_dir.y > 0)
					if previous_dir.y == self.game.CELL_NUMBER - 1:
						previous_up = True
						previous_down = False
					if previous_dir.y == -self.game.CELL_NUMBER + 1:
						previous_up = False
						previous_down = True	
					previous_right = (previous_dir.y == 0) and (previous_dir.x > 0)
					previous_left = (previous_dir.y == 0) and (previous_dir.x < 0)
					if previous_dir.x == self.game.CELL_NUMBER - 1:
						previous_right = False
						previous_left = True
					if previous_dir.x == -self.game.CELL_NUMBER + 1:
						previous_right = True
						previous_left = False
					
					if (next_up and previous_left) or (next_right and previous_down):
						surface.blit(self.body_tr, block_rect)
					elif (next_up and previous_right) or (next_left and previous_down):
						surface.blit(self.body_tl, block_rect)
					elif (next_down and previous_left) or (next_right and previous_up):
						surface.blit(self.body_br, block_rect)
					elif (next_down and previous_right) or (next_left and previous_up):
						surface.blit(self.body_bl, block_rect)

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

	def check_coordinate(self, coord):
		return coord % self.game.CELL_NUMBER
	
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
		self.new_block = False
		self.acc_move = 0.


class Fruit():
	def __init__(self, game):
		self.game = game
		self.randomize()

	def render(self, surface):
		fruit_rect = pygame.Rect(int(self.pos.x * self.game.CELL_SIZE), int(self.pos.y * self.game.CELL_SIZE), self.game.CELL_SIZE, self.game.CELL_SIZE)
		surface.blit(self.game.apple, fruit_rect)

	def randomize(self):
		self.x = random.randint(0, self.game.CELL_NUMBER - 1)
		self.y = random.randint(0, self.game.CELL_NUMBER - 1)
		self.pos = Vector2(self.x, self.y)
