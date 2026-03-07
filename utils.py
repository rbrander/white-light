import sys
import pygame
from constants import HEIGHT, LIGHT_COLOR, MS_PER_DAY, MS_PER_HOUR, MS_PER_MINUTE, MS_PER_SECOND, WIDTH

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


def format_time(time:int) -> list[str]:
  formatted_strings = []
  remaining = time

  # days
  num_days = remaining // MS_PER_DAY
  if num_days > 0:
    formatted_strings.append(f"{num_days} day{"s" if num_days > 1 else ""}")
    remaining -= num_days * MS_PER_DAY

  # hours
  num_hours = remaining // MS_PER_HOUR
  if num_hours > 0:
    formatted_strings.append(f"{num_hours} hour{"s" if num_hours > 1 else ""}")
    remaining -= num_hours * MS_PER_HOUR

  # minutes
  num_minutes = remaining // MS_PER_MINUTE
  if num_minutes > 0:
    formatted_strings.append(f"{num_minutes} minute{"s" if num_minutes > 1 else ""}")
    remaining -= num_minutes * MS_PER_MINUTE

  # seconds
  num_seconds = remaining // MS_PER_SECOND
  if num_seconds > 0:
    formatted_strings.append(f"{num_seconds} second{"s" if num_seconds > 1 else ""}")
    remaining -= num_seconds * MS_PER_SECOND

  return formatted_strings
