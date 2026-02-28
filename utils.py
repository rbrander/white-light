import pygame

def get_scaled_surface(surface:pygame.Surface, rect:pygame.Rect, multiplier:int):
  return pygame.transform.smoothscale_by(surface.subsurface(rect), multiplier)
