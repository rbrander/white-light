import os
import pygame
from buttons import MenuButton
from constants import DARK_BLUE, DARK_COLOR, DARK_PURPLE, FPS, GAME_NAME, LIGHT_COLOR, WIDTH
from game import game
from utils import draw_grid_overlay, exit_program;

"""
TODO:
  - update new game to fade to and from white
  - add hover state
  - add selected state
  - add keyboard navigation?
  - add options (ie. volume)
"""

def draw_background(screen: pygame.Surface):
  screen.fill(DARK_COLOR)
  color1 = DARK_BLUE
  color2 = DARK_PURPLE
  width, height = screen.get_size()
  gradient_surface = pygame.Surface((width, height), pygame.SRCALPHA)
  for y in range(height):
    for x in range(width):
      # Calculate position along the diagonal (0 to 1)
      pos = (x + y) / (width + height - 2)
      pos = max(0, min(1, pos))

      # Interpolate colors
      r = int(color1[0] + (color2[0] - color1[0]) * pos)
      g = int(color1[1] + (color2[1] - color1[1]) * pos)
      b = int(color1[2] + (color2[2] - color1[2]) * pos)

      # Set the pixel color
      gradient_surface.set_at((x, y), (r, g, b))
  screen.blit(gradient_surface, (0, 0))


def main_menu(screen: pygame.Surface):
  large_font = pygame.font.Font(os.path.join("assets", "kenney-fonts", "kenvector_future_thin.ttf"), 64)
  medium_font = pygame.font.Font(os.path.join("assets", "kenney-fonts", "kenvector_future_thin.ttf"), 42)

  new_game_btn = MenuButton("New  Game", medium_font, 300)
  exit_btn = MenuButton("Exit", medium_font, 450)
  menu_buttons:list[MenuButton] = [
    new_game_btn,
    exit_btn,
  ]

  def new_game():
    game(screen)

  clock = pygame.time.Clock()
  running = True
  while running:
    # get input
    for event in pygame.event.get():
      match event.type:
        case pygame.QUIT:
          exit_program()
        case pygame.KEYDOWN:
          if event.key == pygame.K_ESCAPE:
            running = False
            break
      new_game_btn.handle_event(event, on_down=new_game)
      exit_btn.handle_event(event, on_down=exit_program)

    # clear background
    draw_background(screen)

    # title
    title = large_font.render(GAME_NAME, True, LIGHT_COLOR)
    screen.blit(title, title.get_rect(center=(WIDTH//2, 150)))

    # menu buttons
    for menu_button in menu_buttons:
      menu_button.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)
