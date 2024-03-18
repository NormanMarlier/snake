import pygame
import os
import time
import json

from state import Title



class Game():
    def __init__(self):
        pygame.init()
        # Visualization
        self.CELL_SIZE = 40
        self.CELL_NUMBER = 20
        self.GAME_W = self.CELL_SIZE * self.CELL_NUMBER
        self.GAME_H = self.CELL_SIZE * self.CELL_NUMBER
        self.SCREEN_W = int(self.GAME_W * 1.2)
        self.SCREEN_H = int(self.GAME_H * 1.2)
        self.game_canvas = pygame.Surface((self.GAME_W, self.GAME_H))
        self.screen = pygame.display.set_mode((self.SCREEN_W, self.SCREEN_H))
        pygame.display.set_caption("Snake")
        # Actions
        self.actions = {"UP": False, "DOWN": False, "RIGHT": False, "LEFT": False,
                        "SPACE": False, "RETURN": False, "BACKSPACE": False, "character": ""}
        # Time
        self.dt, self.prev_dt = 0., 0.
        self.FRAMERATE = 60
        self.clock = pygame.time.Clock()
        # Assets
        self.load_assets()
        # States
        self.state_stack = []
        self.running, self.playing = True, False
        self.load_states()
        # Score
        self.player_name = ""
        self.score = 0
        # SaveLoadManager
        self.sl_manager = SaveLoadManager()
        self.sl_manager.load_data()
        
    def game_loop(self):

        while self.playing:
            self.get_dt()
            self.get_events()
            self.update()
            self.render()
            self.clock.tick(self.FRAMERATE)
    
    def update(self):
        self.state_stack[-1].update(self.dt, self.actions)

    def render(self):
        self.state_stack[-1].render(self.game_canvas)
        self.screen.blit(pygame.transform.scale(self.game_canvas, (self.SCREEN_W, self.SCREEN_H)), (0, 0))
        pygame.display.flip()
    
    def get_dt(self):
        now = time.time()
        self.dt = now - self.prev_dt
        self.prev_dt = now
    
    def get_events(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running, self.playing = False, False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.actions["SPACE"] = True
                if event.key == pygame.K_RETURN:
                    self.actions["RETURN"] = True
                if event.key == pygame.K_UP:
                    self.actions["UP"] = True
                if event.key == pygame.K_DOWN:
                    self.actions["DOWN"] = True
                if event.key == pygame.K_RIGHT:
                    self.actions["RIGHT"] = True
                if event.key == pygame.K_LEFT:
                    self.actions["LEFT"] = True
                if event.key == pygame.K_BACKSPACE:
                    self.actions["BACKSPACE"] = True

                if event.key == pygame.K_a:
                    self.actions["character"] = "a"
                if event.key == pygame.K_b:
                    self.actions["character"] = "b"
                if event.key == pygame.K_c:
                    self.actions["character"] = "c"
                if event.key == pygame.K_d:
                    self.actions["character"] = "d"
                if event.key == pygame.K_e:
                    self.actions["character"] = "e"
                if event.key == pygame.K_f:
                    self.actions["character"] = "f"
                if event.key == pygame.K_g:
                    self.actions["character"] = "g"
                if event.key == pygame.K_h:
                    self.actions["character"] = "h"
                if event.key == pygame.K_i:
                    self.actions["character"] = "i"
                if event.key == pygame.K_j:
                    self.actions["character"] = "j"
                if event.key == pygame.K_k:
                    self.actions["character"] = "k"
                if event.key == pygame.K_l:
                    self.actions["character"] = "l"
                if event.key == pygame.K_m:
                    self.actions["character"] = "m"
                if event.key == pygame.K_n:
                    self.actions["character"] = "n"
                if event.key == pygame.K_o:
                    self.actions["character"] = "o"
                if event.key == pygame.K_p:
                    self.actions["character"] = "p"
                if event.key == pygame.K_q:
                    self.actions["character"] = "q"
                if event.key == pygame.K_r:
                    self.actions["character"] = "r"
                if event.key == pygame.K_s:
                    self.actions["character"] = "s"
                if event.key == pygame.K_t:
                    self.actions["character"] = "t"
                if event.key == pygame.K_u:
                    self.actions["character"] = "u"
                if event.key == pygame.K_v:
                    self.actions["character"] = "v"
                if event.key == pygame.K_w:
                    self.actions["character"] = "w"
                if event.key == pygame.K_x:
                    self.actions["character"] = "x"
                if event.key == pygame.K_y:
                    self.actions["character"] = "y"
                if event.key == pygame.K_z:
                    self.actions["character"] = "z"
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.actions["SPACE"] = False
                if event.key == pygame.K_RETURN:
                    self.actions["RETURN"] = False
                if event.key == pygame.K_UP:
                    self.actions["UP"] = False
                if event.key == pygame.K_DOWN:
                    self.actions["DOWN"] = False
                if event.key == pygame.K_RIGHT:
                    self.actions["RIGHT"] = False
                if event.key == pygame.K_LEFT:
                    self.actions["LEFT"] = False
                if event.key == pygame.K_BACKSPACE:
                    self.actions["BACKSPACE"] = False

    def reset_keys(self):
        for keys in self.actions.keys():
            if keys == "character":
                self.actions[keys] = ""
            else:
                self.actions[keys] = False
    
    def draw_text(self, surface, text, color, x, y):
        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        surface.blit(text_surface, text_rect)
    
    def load_assets(self):
        self.FONTSIZE = 25
        self.font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', self.FONTSIZE)
        self.apple = pygame.image.load('Graphics/apple.png').convert_alpha()
    
    def load_states(self):
        self.title_screen = Title(self)
        self.state_stack.append(self.title_screen)
    
    def load_score(self):
        self.sl_manager.load_data()
    
    def save_score(self):
        self.sl_manager.save_data((self.player_name, self.score))
    

class SaveLoadManager():
    # Manage ranking
    # Save the top 10 score
    # Remember the name and the associated score
    def __init__(self):
        self.filename = "save.json"
        self.ranking = {}
        self.TOP_N = 10
    
    def sorted_ranking(self, ranking):
        return dict(sorted(ranking.items(), key=lambda item: item[1]))

    def load_data(self):
        try:
            with open(self.filename, "r+") as file:
                self.ranking = json.load(file)
                self.update_ranking(self.ranking)
        except:
            pass
    
    def save_data(self, data):
        """Add the new data to the current ranking."""
        self.update_ranking(data)
        with open(self.filename, "w+") as file:
            json.dump(self.ranking, file)

    def update_ranking(self, data):
        """Check if the new data can be integrated into the ranking
        
        Add the new data and sort the ranking. Then, keep the 10 best.
        Args:
            data, a tuple (name, score)
        """
        # If the player already exists
        if data[0] in self.ranking.keys():
            # Check if the new score is greater than before
            if data[1] > self.ranking[data[0]]:
                self.ranking[data[0]] = data[1]
        else:
            self.ranking[data[0]] = data[1]
        # Sorted the ranking and keep the 10 best
        self.ranking = self.sorted_ranking(self.ranking)
        self.ranking = {kv[0]:kv[1] for i, kv in enumerate(self.ranking.items()) if i <= self.TOP_N}


        


if __name__ == "__main__":
    game = Game()

    while game.running:
        game.playing = True
        game.game_loop()

