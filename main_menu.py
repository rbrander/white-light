import os
import pygame
from buttons import MenuButton
from constants import DARK_COLOR, FPS, GAME_NAME, LIGHT_COLOR, WIDTH
from game import game
from utils import draw_grid_overlay, exit_program;

"""
TODO:
  - update new game to fade to and from white
  - add hover state
  - add selected state
  - add keyboard navigation?
  - add save game
  - add continue / load game
  - add options (ie. volume)
"""

def main_menu(screen: pygame.Surface):
  font = pygame.font.Font(os.path.join("assets", "kenney-fonts", "kenpixel_mini.ttf"), 42)

  new_game_btn = MenuButton("New Game", font, 200)
  exit_btn = MenuButton("Exit", font, 400)
  menu_buttons:list[MenuButton] = [
    new_game_btn,
    #MenuButton("Save Game", font),
    #MenuButton("Continue Game", font),
    #MenuButton("Options", font),
    exit_btn,
  ]

  def new_game():
    game(screen)

  dt = 0
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

    # update

    # draw
    # clear background
    screen.fill(DARK_COLOR)

    # menu buttons
    for menu_button in menu_buttons:
      menu_button.draw(screen)

    # title
    title = font.render(GAME_NAME, True, LIGHT_COLOR)
    screen.blit(title, title.get_rect(center=(WIDTH//2, 50)))

    # Grid overlay
    # draw_grid_overlay(screen)

    pygame.display.flip()
    dt = clock.tick(FPS)
