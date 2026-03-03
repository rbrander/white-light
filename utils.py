import sys
import pygame
from constants import HEIGHT, LIGHT_COLOR, WIDTH

def exit_program():
  pygame.quit()
  sys.exit()

def get_scaled_surface(surface:pygame.Surface, rect:pygame.Rect, multiplier:int):
  return pygame.transform.smoothscale_by(surface.subsurface(rect), multiplier)

def draw_grid_overlay(screen:pygame.Surface, x_gap:int = 50, y_gap:int = 100):
  """
  draw a grid of lines spaced out by provided gap
  """
  for x in range(0, WIDTH, x_gap):
    pygame.draw.line(screen, LIGHT_COLOR, (x, 0), (x, HEIGHT), 2)
  for y in range(0, HEIGHT, y_gap):
    pygame.draw.line(screen, LIGHT_COLOR, (0, y), (WIDTH, y), 2)
