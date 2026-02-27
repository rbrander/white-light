"""
TODO:
- add menu
  - add new game
  - add save game
  - add quit game
- set icon (button image)
- create a button class
- add a blue button
- add a way to upgrade to a square button
- add a way to deactive a button (perhaps change alpha to indicate grayed out)
"""

import pygame
import sys

GAME_NAME = "Button Burst"
WIDTH, HEIGHT = 600, 800
FPS = 60
score = 0

# green, red
# blue, white

def main():
  global score
  pygame.init()
  screen = pygame.display.set_mode((WIDTH, HEIGHT))
  pygame.display.set_caption(GAME_NAME)
  # TODO: pygame.display.set_icon()
  clock = pygame.time.Clock()

  font = pygame.font.SysFont("Arial", 36)
  btn_up_sound = pygame.mixer.Sound("assets/button-click-up.ogg")
  btn_down_sound = pygame.mixer.Sound("assets/button-click-down.ogg")

  background_color = (239, 243, 228)



  buch_art_golden_ui = pygame.image.load("assets/buch-ui.png").convert_alpha()
  left_guage = buch_art_golden_ui.subsurface(pygame.Rect(11, 18, 92, 64))
  left_guage_dest_rect = left_guage.get_rect(center=(WIDTH//2 - 100, HEIGHT//2 - 100))

  sprite_sheet = pygame.image.load("assets/push-buttons.png").convert_alpha()

  green_round_btn_up_rect = pygame.Rect(35,  71, 118, 89)
  green_round_btn_down_rect = pygame.Rect(172, 71, 118, 89)
  red_round_btn_up_rect = pygame.Rect(332,  71, 118, 89)
  red_round_btn_down_rect = pygame.Rect(469, 71, 118, 89)

  green_btn_up = sprite_sheet.subsurface(green_round_btn_up_rect)
  green_btn_down = sprite_sheet.subsurface(green_round_btn_down_rect)
  red_btn_up = sprite_sheet.subsurface(red_round_btn_up_rect)
  red_btn_down = sprite_sheet.subsurface(red_round_btn_down_rect)

  green_btn_rect = green_btn_up.get_rect(center=(WIDTH//2, HEIGHT//2))
  red_btn_rect = red_btn_up.get_rect(center=(WIDTH//2, HEIGHT//2 + 100))

  running = True
  isButtonDown = False
  downButtonColor: str | None = None # green, red, or None
  while running:
    showRedButton = score >= 10
    for event in pygame.event.get():
      match event.type:
        case pygame.QUIT:
          running = False
        case pygame.MOUSEBUTTONUP:
          if event.button == 1:
            isButtonDown = False
            downButtonColor = None
            btn_up_sound.play()
        case pygame.MOUSEBUTTONDOWN:
          if event.button == 1:
            if green_btn_rect.collidepoint(event.pos):
              downButtonColor = 'green'
              isButtonDown = True
              btn_down_sound.play()
              score += 1
            elif showRedButton and red_btn_rect.collidepoint(event.pos):
              downButtonColor = 'red'
              isButtonDown = True
              btn_down_sound.play()
              score += 10

    # clear background
    screen.fill(background_color)

    # guage
    screen.blit(left_guage, left_guage_dest_rect)

    # green button
    img = green_btn_down if isButtonDown and downButtonColor == 'green' else green_btn_up
    screen.blit(img, green_btn_rect)

    # red button
    if showRedButton:
      img = red_btn_down if isButtonDown and downButtonColor == 'red' else red_btn_up
      screen.blit(img, red_btn_rect)

    # score text
    text_surface = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(text_surface, (10, 10))

    pygame.display.flip()
    clock.tick(FPS)

  pygame.quit()
  sys.exit()

if __name__ == "__main__":
  main()