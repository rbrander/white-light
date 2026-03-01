import pygame
import os
from utils import get_scaled_surface
from typing import Literal

ButtonType = Literal["round", "square"]
ButtonColor = Literal["red", "green", "blue"]

SCALE = 1.2 # size for rendering vs sprite sheet size
BUTTON_RECTS = { # Rectangles for each button found on sprite sheet
  "red": {
    "round": {
      "up": pygame.Rect(332,  71, 118, 89),
      "down": pygame.Rect(469, 71, 118, 89)
    },
    "square": {
      "up": pygame.Rect(332,  192, 120, 105),
      "down": pygame.Rect(469, 192, 120, 105)
    }
  },
  "green": {
    "round": {
      "up": pygame.Rect(35,  71, 118, 89),
      "down": pygame.Rect(172, 71, 118, 89)
    },
    "square": {
      "up": pygame.Rect(35,  192, 120, 105),
      "down": pygame.Rect(172, 192, 120, 105)
    }
  },
  "blue": {
    "round": {
      "up": pygame.Rect(35,  343, 118, 89),
      "down": pygame.Rect(172, 343, 118, 89)
    },
    "square": {
      "up": pygame.Rect(35,  465, 120, 105),
      "down": pygame.Rect(172, 465, 120, 105)
    }
  }
}

class Button:
  def __init__(self, sprite_sheet: pygame.Surface, color: ButtonColor, type: ButtonType, position: tuple[int, int]):
    self.btn_up: pygame.Surface = get_scaled_surface(sprite_sheet, BUTTON_RECTS[color][type]["up"], SCALE)
    self.btn_down: pygame.Surface = get_scaled_surface(sprite_sheet, BUTTON_RECTS[color][type]["down"], SCALE)
    self.is_pressed: bool = False
    self.color: ButtonColor = color
    self.type: ButtonType = type
    self.position = position
    self.rect = pygame.Rect(position, self.btn_up.get_size())

  @property
  def down(self):
    return self.btn_down

  @property
  def up(self):
    return self.btn_up

  def handle_event(self, event: pygame.event.Event, on_down: function, on_up: function):
    match event.type:
      case pygame.MOUSEBUTTONUP:
        if event.button == 1 and self.rect.collidepoint(event.pos):
          self.is_pressed = False
          on_up()
      case pygame.MOUSEBUTTONDOWN:
        if event.button == 1 and self.rect.collidepoint(event.pos):
          self.is_pressed = True
          on_down()

  def draw(self, surface: pygame.Surface):
    img = self.down if self.is_pressed else self.up
    surface.blit(img, self.rect.topleft)

class Buttons:
  def __init__(self):
    self.sprite_sheet = pygame.image.load(os.path.join("assets", "rgb-buttons.png")).convert_alpha()

  def create(self, color: ButtonColor, type: ButtonType, position: tuple[int, int]):
    return Button(self.sprite_sheet, color, type, position)

