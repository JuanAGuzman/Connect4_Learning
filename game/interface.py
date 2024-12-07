import pygame
from pygame.locals import *
from game.app.scenes import *

class GUIBoard:
    
    def __init__(self, size: tuple[int, int] = (960, 640)) -> None:
        pygame.init()
        self.running = True
        self.screen = pygame.display.set_mode(size)
        self.clock = pygame.time.Clock()

        self.players = {}

        self.game_management = GameStateManager("Menu")
        self.scenes = {
              "Menu":MenuScene(self.screen, self.game_management),
              "Play":PlayScene(self.screen, self.game_management),
              "Players":PlayerScene(self.screen, self.game_management),
              "Credits":CreditScene(self.screen, self.game_management),
              "Qtable":QtableScene(self.screen, self.game_management),
              "Quit":QuitScene(self.screen, self.game_management),
              "End": EndScene(self.screen, self.game_management),
              "QTableEnd": QTableEndScene(self.screen, self.game_management)
              }

    def run(self, fps: int = 60) -> None:
        while self.running:
            current_scene = self.game_management.get_state()
            self.scenes[current_scene].draw()
            self.scenes[current_scene].set_players(self.game_management.players)
            self.scenes[current_scene].set_winner(self.game_management.winner)
            self.scenes[current_scene].run(pygame.event.get())
            
            self.close(pygame.event.get())
            
            if self.running:
                self.running = self.scenes[current_scene].running
            
            pygame.display.update()
            self.clock.tick(fps)

        pygame.quit()

    def close(self, events) -> None:
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False


class GameStateManager:
    def __init__(self, current_state):
        self.current_state = current_state
        self.players = None
        self.winner = None

    def get_state(self):
        return self.current_state
    
    def set_state(self, state, players = None, winner = None):
        if state:
            self.current_state = state
            self.players = players
            self.winner = winner
