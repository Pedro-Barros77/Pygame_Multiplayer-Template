import pygame
from datetime import datetime

from domain.services import game_controller, drawer
from domain.utils import colors, math_utillity as math, enums, constants
from domain.utils.math_utillity import sum_tuple_infix as t

class Game:
    def __init__(self, client_type: enums.ClientType):
        self.screen = None
        self.clock = None
        self.drawer = None
        self.pressed_keys = []
        self.start_time = None
        self.monitor_size = (0,0)
        self.client_type = client_type
        self.player_conn_id = 0
    
    
    def start(self):
        pygame.init()
        
        if self.monitor_size == (0,0):
            self.monitor_size = (pygame.display.Info().current_w-50, pygame.display.Info().current_h - 100)

        self.screen = pygame.display.set_mode(self.monitor_size)
        
        game_controller.playing = True
        
        self.start_time = datetime.now()

        self.clock = pygame.time.Clock()
        self.drawer = drawer.Drawer(self)
        
        if self.client_type == enums.ClientType.HOST:
            game_controller.host_game(self, constants.SERVER_ADDRESS, constants.SERVER_PORT)
        elif self.client_type == enums.ClientType.CLIENT:
            game_controller.enter_game(self, constants.SERVER_ADDRESS, constants.SERVER_PORT)
        
        self.game_loop()

    def game_loop(self):
        while game_controller.playing:
            
            game_controller.handle_events(self)

            self.screen.fill(colors.BLACK)
            
            _text = self.drawer.get_text_surface('Pygame Start Template (Pedro Barros)', colors.WHITE, 80, 'Arial')
            _timer = self.drawer.get_text_surface(str(datetime.now() - self.start_time), colors.RED, 50, 'Arial')
            
            self.screen.blit(_timer, math.space_to_center(_timer.get_size(), self.screen.get_size()) |t| (0,50))
            self.screen.blit(_text, math.space_to_center(_text.get_size(), self.screen.get_size()) |t| (0,-50))

            pygame.display.update()
            self.clock.tick(60)
        
