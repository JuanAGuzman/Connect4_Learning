import pygame

colors = {
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "yellow": (255, 255, 0)
          }

class CounterImage(pygame.sprite.Sprite):
    ROW_CENTER = (123, 202, 281, 360, 439, 518)
    COLUMN_CENTER = (403, 482, 561, 639, 718, 797, 876)
    def __init__(self, color, column, row):
        pygame.sprite.Sprite.__init__(self)

        image = pygame.image.load(f'game\sprites\{color}_token.png')
        self.image = pygame.transform.scale(image, (56, 56))

        self.rect = self.image.get_rect()
        self.rect.centerx = self.COLUMN_CENTER[column]
        self.rect.centery = 640 - self.ROW_CENTER[row]
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)

class BoardImage(pygame.sprite.Sprite):
    def __init__(self, position: tuple[int, int] = (640, 320)) -> None:
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('game\sprites\empty_table.png')

        self.rect = self.image.get_rect()
        self.rect.centerx = position[0]
        self.rect.centery = position[1]

class Text:
    def __init__(self, text, size, pos):
        self.font = pygame.font.Font("game\sprites\Grand9K Pixel.ttf", size)
        self.text = self.font.render(text, True, colors["white"])
        self.size = self.font.size(text)

        self.textRect = self.text.get_rect()
        self.textRect.center = pos

    def draw(self, screen):
        screen.blit(self.text, self.textRect)
        return self.size
    
class ValueText:
    def __init__(self, text, size, pos):
        self.font = pygame.font.Font("game\sprites\Grand9K Pixel.ttf", size)
        self.text = self.font.render(text, True, colors["black"])
        self.size = self.font.size(text)

        self.textRect = self.text.get_rect()
        self.textRect.center = pos

    def draw(self, screen):
        screen.blit(self.text, self.textRect)
        return self.size
    
class MenuButton:
    NEXT = {"MENU": "Menu", "PLAY": "Players", "Q-TABLES": "Qtable", "CREDITS": "Credits", "QUIT": "Quit", "PLAY AGAIN": "Players", "TRY AGAIN": "Qtable"}
    def __init__(self, params, scene):
        self.scene = scene
        self.pos, self.size = params[scene]

    def action(self, event):
        check = lambda event, i: self.pos[i] - self.size[i]/2 <= event.pos[i] <= self.pos[i] + self.size[i]/2

        if check(event, 0) and check(event, 1):
            return self.NEXT[self.scene]
        
class PlayerButton:
    def __init__(self, pos, size):
        self.pos = pos
        self.size = size

    def draw(self, screen):
        if self.pos and self.size:
            pygame.draw.rect(screen, colors["yellow"], pygame.Rect(self.pos, self.size),  2)
