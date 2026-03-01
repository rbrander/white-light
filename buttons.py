import pygame
import os
from utils import get_scaled_surface
from typing import Literal

ButtonType = Literal["round", "square"]
ButtonColor = Literal["red", "green", "blue"]

SCALE = 1.2 # size for rendering vs sprite sheet size
BUCH_BTN_SCALE = 2 # size for scaling buch buttons
RGB_BUTTON_RECTS = { # Rectangles for each button found on rgb-buttons sprite sheet
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
BUCH_BUTTON_RECTS = { # Rectangles for each button found on buch-buttons sprite sheet
  "left": {
    "up": pygame.Rect(1, 74, 24, 24),
    "down": pygame.Rect(1, 99, 24, 24)
  },
  "left_with_ring": {
    "up": pygame.Rect(76, 99, 46, 24),
    "down": pygame.Rect(76, 74, 46, 24)
  },
  "middle": {
    "up": pygame.Rect(26, 74, 23, 24),
    "down": pygame.Rect(26, 99, 23, 24)
  },
  "right": {
    "up": pygame.Rect(50, 74, 25, 24),
    "down": pygame.Rect(50, 99, 25, 24)
  },
  "right_with_ring": {
    "up": pygame.Rect(123, 99, 47, 24),
    "down": pygame.Rect(123, 74, 47, 24)
  },
  "green_ball": {
    "dark": pygame.Rect(10, 16, 14, 14),
    "light": pygame.Rect(10, 32, 14, 14),
    "pressed": pygame.Rect(10, 48, 14, 14)
  },
  "blue_ball": {
    "dark": pygame.Rect(26, 16, 14, 14),
    "light": pygame.Rect(26, 32, 14, 14),
    "pressed": pygame.Rect(26, 48, 14, 14)
  },
  "red_ball": {
    "dark": pygame.Rect(42, 16, 14, 14),
    "light": pygame.Rect(42, 32, 14, 14),
    "pressed": pygame.Rect(42, 48, 14, 14)
  },
  "grey_ball": {
    "dark": pygame.Rect(58, 16, 14, 14),
    "light": pygame.Rect(58, 32, 14, 14),
    "pressed": pygame.Rect(58, 48, 14, 14)
  }
}

class ButtonBase:
  def __init__(self, position: tuple[int, int], size: tuple[int, int]):
    self.is_pressed: bool = False
    self.rect = pygame.Rect(position, size)

  def handle_event(self, event: pygame.event.Event, on_down: function | None = None, on_up: function | None = None):
    match event.type:
      case pygame.MOUSEBUTTONUP:
        if event.button == 1 and self.rect.collidepoint(event.pos):
          self.is_pressed = False
          if on_up != None:
            on_up()
      case pygame.MOUSEBUTTONDOWN:
        if event.button == 1 and self.rect.collidepoint(event.pos):
          self.is_pressed = True
          if on_down != None:
            on_down()


class RGBButton(ButtonBase):
  def __init__(self, sprite_sheet: pygame.Surface, color: ButtonColor, type: ButtonType, position: tuple[int, int]):
    self.btn_up: pygame.Surface = get_scaled_surface(sprite_sheet, RGB_BUTTON_RECTS[color][type]["up"], SCALE)
    self.btn_down: pygame.Surface = get_scaled_surface(sprite_sheet, RGB_BUTTON_RECTS[color][type]["down"], SCALE)
    super().__init__(position, self.btn_up.get_size())
    self.color: ButtonColor = color
    self.type: ButtonType = type

  def draw(self, surface: pygame.Surface):
    img = self.btn_down if self.is_pressed else self.btn_up
    surface.blit(img, self.rect.topleft)

class BuchButton(ButtonBase):
  def __init__(self, sprite_sheet: pygame.Surface, position: tuple[int, int], color: ButtonColor | None = None):
    self.color = color
    self.position = position
    self.left_up = get_scaled_surface(sprite_sheet, BUCH_BUTTON_RECTS["left"]["up"], BUCH_BTN_SCALE)
    self.left_down = get_scaled_surface(sprite_sheet, BUCH_BUTTON_RECTS["left"]["down"], BUCH_BTN_SCALE)
    self.middle_up = get_scaled_surface(sprite_sheet, BUCH_BUTTON_RECTS["middle"]["up"], BUCH_BTN_SCALE)
    self.middle_down = get_scaled_surface(sprite_sheet, BUCH_BUTTON_RECTS["middle"]["down"], BUCH_BTN_SCALE)
    # TODO: build right using color; if color is none use "right" otherwise use "right_with_ring" overlaying color-ed ball
    self.right_up = get_scaled_surface(sprite_sheet, BUCH_BUTTON_RECTS["right" if color == None else "right_with_ring"]["up"], BUCH_BTN_SCALE)
    self.right_down = get_scaled_surface(sprite_sheet, BUCH_BUTTON_RECTS["right" if color == None else "right_with_ring"]["down"], BUCH_BTN_SCALE)
    size = (self.left_up.get_width()+self.middle_up.get_width()+self.right_up.get_width(), self.middle_up.get_height())
    super().__init__(position, size)

  def draw(self, surface: pygame.Surface, font: pygame.font.Font | None = None, text: str = ""):
    # draw left
    surface.blit(self.left_down if self.is_pressed else self.left_up, self.position)
    # draw middle
    surface.blit(self.middle_down if self.is_pressed else self.middle_up, (self.position[0] + self.left_up.get_width(), self.position[1]))
    # draw right
    surface.blit(self.right_down if self.is_pressed else self.right_up, (self.position[0] + self.left_up.get_width() + self.middle_up.get_width(), self.position[1]))
    # draw text
    if font != None and text != "":
      text_surface = font.render(text, True, (0,0,0)).convert_alpha()
      surface.blit(text_surface, text_surface.get_rect(topleft=(self.position[0] + 24, self.position[1] + 9)))

class Buttons:
  def __init__(self):
    self.rgb_sprite_sheet = pygame.image.load(os.path.join("assets", "rgb-buttons.png")).convert_alpha()
    self.buch_buttons_sprite_sheet = pygame.image.load(os.path.join("assets", "buch-buttons.png")).convert_alpha()

  def create_rgb(self, color: ButtonColor, type: ButtonType, position: tuple[int, int]):
    return RGBButton(self.rgb_sprite_sheet, color, type, position)

  def create_buch(self, position: tuple[int, int], color: ButtonColor | None = None):
    return BuchButton(self.buch_buttons_sprite_sheet, position, color)
