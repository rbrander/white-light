"""
TODO:
- add menu
  - add new game
  - add save game
  - add quit game
- create a button class
- add a way to upgrade to a square button
- add a way to deactive a button (perhaps change alpha to indicate grayed out)
"""

import pygame
import sys
import os

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

  font = pygame.font.SysFont("Arial", 36)
  btn_up_sound = pygame.mixer.Sound(os.path.join("assets", "button-click-up.ogg"))
  btn_down_sound = pygame.mixer.Sound(os.path.join("assets", "button-click-down.ogg"))


  buch_ui = pygame.image.load(os.path.join("assets","buch-ui.png")).convert_alpha()
  left_guage_raw = buch_ui.subsurface(pygame.Rect(11, 18, 84, 64))
  left_guage_raw_dest_rect = left_guage_raw.get_rect(center=(WIDTH//2 - 100, HEIGHT//2 - 100))
  GUAGE_SIZE_MULTIPLIER = 2
  left_guage = pygame.transform.scale(left_guage_raw, (left_guage_raw_dest_rect.width * GUAGE_SIZE_MULTIPLIER, left_guage_raw_dest_rect.height * GUAGE_SIZE_MULTIPLIER))
  left_guage_dest_rect = left_guage.get_rect(center=(WIDTH//2 - 100*GUAGE_SIZE_MULTIPLIER, HEIGHT//2 - 100*GUAGE_SIZE_MULTIPLIER))


  sprite_sheet = pygame.image.load(os.path.join("assets", "push-buttons.png")).convert_alpha()

  red_round_btn_up_rect = pygame.Rect(332,  71, 118, 89)
  red_round_btn_down_rect = pygame.Rect(469, 71, 118, 89)
  green_round_btn_up_rect = pygame.Rect(35,  71, 118, 89)
  green_round_btn_down_rect = pygame.Rect(172, 71, 118, 89)
  blue_round_btn_up_rect = pygame.Rect(35,  343, 118, 89)
  blue_round_btn_down_rect = pygame.Rect(172, 343, 118, 89)

  red_btn_up = sprite_sheet.subsurface(red_round_btn_up_rect)
  red_btn_down = sprite_sheet.subsurface(red_round_btn_down_rect)
  green_btn_up = sprite_sheet.subsurface(green_round_btn_up_rect)
  green_btn_down = sprite_sheet.subsurface(green_round_btn_down_rect)
  blue_btn_up = sprite_sheet.subsurface(blue_round_btn_up_rect)
  blue_btn_down = sprite_sheet.subsurface(blue_round_btn_down_rect)

  red_btn_rect = red_btn_up.get_rect(center=(WIDTH//2, HEIGHT//2 + 0))
  green_btn_rect = green_btn_up.get_rect(center=(WIDTH//2, HEIGHT//2 + 100))
  blue_btn_rect = blue_btn_up.get_rect(center=(WIDTH//2, HEIGHT//2 + 200))

  pygame.display.set_icon(pygame.transform.scale(red_btn_up, (32, 32)))

  clock = pygame.time.Clock()
  running = True
  isButtonDown = False
  downButtonColor: str | None = None # green, red, blue, or None
  while running:
    showGreenButton = score >= 10
    showBlueButton = score >= 100
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
            if red_btn_rect.collidepoint(event.pos):
              downButtonColor = 'red'
              isButtonDown = True
              btn_down_sound.play()
              score += 1
            elif showGreenButton and green_btn_rect.collidepoint(event.pos):
              downButtonColor = 'green'
              isButtonDown = True
              btn_down_sound.play()
              score += 10
            elif showBlueButton and blue_btn_rect.collidepoint(event.pos):
              downButtonColor = 'blue'
              isButtonDown = True
              btn_down_sound.play()
              score += 100

    # clear background
    screen.fill((239, 243, 228))

    # guage
    screen.blit(left_guage, left_guage_dest_rect)

    # red button
    img = red_btn_down if isButtonDown and downButtonColor == 'red' else red_btn_up
    screen.blit(img, red_btn_rect)

    # green button
    if showGreenButton:
      img = green_btn_down if isButtonDown and downButtonColor == 'green' else green_btn_up
      screen.blit(img, green_btn_rect)

    # blue button
    if showBlueButton:
      img = blue_btn_down if isButtonDown and downButtonColor == 'blue' else blue_btn_up
      screen.blit(img, blue_btn_rect)

    # score text
    text_surface = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(text_surface, (10, 10))

    pygame.display.flip()
    clock.tick(FPS)

  pygame.quit()
  sys.exit()

if __name__ == "__main__":
  main()