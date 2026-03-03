import pygame
from buttons import Buttons
from main_menu import main_menu
from constants import GAME_NAME, WIDTH, HEIGHT
from utils import exit_program

def main():
  pygame.init()
  screen = pygame.display.set_mode((WIDTH, HEIGHT))
  pygame.display.set_caption(GAME_NAME)

  buttons = Buttons()
  red_btn = buttons.create_rgb("red", "square", (0, 0))
  pygame.display.set_icon(pygame.transform.smoothscale(red_btn.btn_up, (32, 32)))

  main_menu(screen)
  exit_program()

if __name__ == "__main__":
  main()