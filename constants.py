import pygame

GAME_NAME = "White  Light"
WIDTH, HEIGHT = 600, 800
FPS = 60

BLACK = pygame.color.Color(0, 0, 0)
WHITE = pygame.color.Color(255, 255, 255)
LIGHT_COLOR = pygame.color.Color(239, 243, 228)
DARK_COLOR = pygame.color.Color(60, 60, 60)
DARK_BLUE = pygame.color.Color(0, 0, 100)
DARK_PURPLE = pygame.color.Color(70, 0, 70)

# e.g. 1d 2h 3m 4s = 1*86,400,000 + 2*3,600,000 + 3*60,000 + 4*1,000 = 93,784,000
MS_PER_SECOND = 1000
MS_PER_MINUTE = MS_PER_SECOND * 60 # 60_000
MS_PER_HOUR = MS_PER_MINUTE * 60 # 3_600_000
MS_PER_DAY = MS_PER_HOUR * 24 # 86_400_000
