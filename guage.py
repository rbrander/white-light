import pygame
import os

GUAGE_SIZE_MULTIPLIER = 2

class Size:
  def __init__(self, width, height):
    self.width = width
    self.height = height

  def get_size(self, multiplier = 1):
    return (self.get_width(multiplier), self.get_height(multiplier))

  def get_width(self, multiplier = 1):
    return self.width * multiplier

  def get_height(self, multiplier = 1):
    return self.height * multiplier

def get_scaled_surface(surface:pygame.Surface, rect:pygame.Rect, multiplier:int):
  return pygame.transform.scale(surface.subsurface(rect),(rect.width*multiplier, rect.height*multiplier))

class Guage:
  def __init__(self, num_bars, multiplier = GUAGE_SIZE_MULTIPLIER):
    self.num_bars = num_bars
    self.multiplier = multiplier

    # load graphic asset and assign rectangles to pieces
    buch_ui = pygame.image.load(os.path.join("assets","guage.png")).convert_alpha()
    left_guage_rect = pygame.Rect(11, 18, 84, 64)
    empty_odd_bar_rect = pygame.Rect(96, 22, 8, 16)
    empty_even_bar_rect = pygame.Rect(105, 22, 8, 16)
    red_odd_bar_rect = pygame.Rect(155, 24, 8, 12)
    red_even_bar_rect = pygame.Rect(164, 24, 8, 12)
    green_odd_bar_rect = pygame.Rect(155, 64, 8, 12)
    green_even_bar_rect = pygame.Rect(164, 64, 8, 12)
    blue_odd_bar_rect = pygame.Rect(155, 44, 8, 12)
    blue_even_bar_rect = pygame.Rect(164, 44, 8, 12)
    right_guage_red_rect = pygame.Rect(114, 20, 32, 20)
    right_guage_blue_rect = pygame.Rect(114, 40, 32, 20)
    right_guage_green_rect = pygame.Rect(114, 60, 32, 20)

    # create local surfaces and sizes for fast drawing
    self.bar_y_offset = empty_odd_bar_rect.top - left_guage_rect.top
    self.bar_light_y_offset = self.bar_y_offset + (empty_odd_bar_rect.height - red_odd_bar_rect.height)//2
    self.right_guage_red_offset = right_guage_red_rect.top - left_guage_rect.top
    self.empty_bar_size = Size(empty_odd_bar_rect.width, empty_odd_bar_rect.height)
    self.filled_bar_size = Size(red_odd_bar_rect.width, red_odd_bar_rect.height)
    self.left_guage_size = Size(left_guage_rect.width, left_guage_rect.height)
    self.right_guage_red_size = Size(right_guage_red_rect.width, right_guage_red_rect.height)
    self.right_guage_blue_size = Size(right_guage_blue_rect.width, right_guage_blue_rect.height)
    self.right_guage_green_size = Size(right_guage_green_rect.width, right_guage_green_rect.height)

    self.left_guage = get_scaled_surface(buch_ui, left_guage_rect, multiplier)
    self.right_guage_red = get_scaled_surface(buch_ui, right_guage_red_rect, multiplier)
    self.right_guage_blue = get_scaled_surface(buch_ui, right_guage_blue_rect, multiplier)
    self.right_guage_green = get_scaled_surface(buch_ui, right_guage_green_rect, multiplier)
    self.empty_odd_bar = get_scaled_surface(buch_ui, empty_odd_bar_rect, multiplier)
    self.empty_even_bar = get_scaled_surface(buch_ui, empty_even_bar_rect, multiplier)
    self.red_odd_bar = get_scaled_surface(buch_ui, red_odd_bar_rect, multiplier)
    self.red_even_bar = get_scaled_surface(buch_ui, red_even_bar_rect, multiplier)
    self.green_odd_bar = get_scaled_surface(buch_ui, green_odd_bar_rect, multiplier)
    self.green_even_bar = get_scaled_surface(buch_ui, green_even_bar_rect, multiplier)
    self.blue_odd_bar = get_scaled_surface(buch_ui, blue_odd_bar_rect, multiplier)
    self.blue_even_bar = get_scaled_surface(buch_ui, blue_even_bar_rect, multiplier)

  def get_width(self):
    left_width = self.left_guage_size.get_width(self.multiplier)
    bars_width = self.num_bars * self.empty_bar_size.get_width(self.multiplier)
    right_width = self.right_guage_red_size.get_width(self.multiplier)
    return left_width + bars_width + right_width

  def draw(self, surface, x, y, num_bars = (1, 2, 3)):
    # draw left
    surface.blit(self.left_guage, (x, y))
    # draw bars
    bar_y = y + self.multiplier * self.bar_y_offset
    filled_bar_y = y + self.multiplier * self.bar_light_y_offset
    bar_width = self.empty_bar_size.get_width(self.multiplier)
    left_guage_width = self.left_guage_size.get_width(self.multiplier)
    for i in range(self.num_bars):
      bar_x = x + left_guage_width + i * bar_width
      # draw empty bars
      surface.blit(self.empty_odd_bar if i == 0 else self.empty_even_bar, (bar_x, bar_y))
      surface.blit(self.empty_odd_bar if i == 0 else self.empty_even_bar, (bar_x, bar_y+self.right_guage_red_size.get_height(self.multiplier)))
      surface.blit(self.empty_odd_bar if i == 0 else self.empty_even_bar, (bar_x, bar_y+self.right_guage_red_size.get_height(self.multiplier)+self.right_guage_blue_size.get_height(self.multiplier)))
      # draw filled bars
      is_red_filled = i < num_bars[0]
      is_green_filled = i < num_bars[1]
      is_blue_filled = i < num_bars[2]
      if is_red_filled:
        surface.blit(self.red_odd_bar if i == 0 else self.red_even_bar, (bar_x, filled_bar_y))
      if is_green_filled:
        surface.blit(self.green_odd_bar if i == 0 else self.green_even_bar, (bar_x, filled_bar_y+self.right_guage_red_size.get_height(self.multiplier)))
      if is_blue_filled:
        surface.blit(self.blue_odd_bar if i == 0 else self.blue_even_bar, (bar_x, filled_bar_y+self.right_guage_red_size.get_height(self.multiplier)+self.right_guage_blue_size.get_height(self.multiplier)))
    # draw right
    right_y = y + self.multiplier * self.right_guage_red_offset
    right_x = x + left_guage_width + self.num_bars * bar_width
    surface.blit(self.right_guage_red, (right_x, right_y))
    surface.blit(self.right_guage_green, (right_x, right_y + self.right_guage_red_size.get_height(self.multiplier)))
    surface.blit(self.right_guage_blue, (right_x, right_y + self.right_guage_red_size.get_height(self.multiplier)+self.right_guage_blue_size.get_height(self.multiplier)))


