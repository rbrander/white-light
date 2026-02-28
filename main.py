"""
TODO:
- add menu
  - add new game
  - add save game
  - add quit game
- create a button class
- add end game state
  - add sound
  - fade to white
  - go back to menu
- add a way to upgrade buttons (so they contribute more)
- add custom pixel font
"""

import pygame
import sys
import os
from guage import Guage
from utils import get_scaled_surface

GAME_NAME = "Button Burst"
WIDTH, HEIGHT = 600, 800
FPS = 60

# green, red
# blue, white

def main():
  pygame.init()
  screen = pygame.display.set_mode((WIDTH, HEIGHT))
  pygame.display.set_caption(GAME_NAME)

  font = pygame.font.SysFont(None, 36)
  btn_up_sound = pygame.mixer.Sound(os.path.join("assets", "button-click-up.ogg"))
  btn_down_sound = pygame.mixer.Sound(os.path.join("assets", "button-click-down.ogg"))

  guage = Guage(5, 3.5)

  # sprite_sheet = pygame.image.load(os.path.join("assets", "push-buttons.png")).convert_alpha()
  sprite_sheet = pygame.image.load(os.path.join("assets", "rgb-buttons.png")).convert_alpha()

  red_round_btn_up_rect = pygame.Rect(332,  71, 118, 89)
  red_round_btn_down_rect = pygame.Rect(469, 71, 118, 89)
  red_square_btn_up_rect = pygame.Rect(332,  192, 120, 105)
  red_square_btn_down_rect = pygame.Rect(469, 192, 120, 105)
  green_round_btn_up_rect = pygame.Rect(35,  71, 118, 89)
  green_round_btn_down_rect = pygame.Rect(172, 71, 118, 89)
  green_square_btn_up_rect = pygame.Rect(35,  192, 120, 105)
  green_square_btn_down_rect = pygame.Rect(172, 192, 120, 105)
  blue_round_btn_up_rect = pygame.Rect(35,  343, 118, 89)
  blue_round_btn_down_rect = pygame.Rect(172, 343, 118, 89)
  blue_square_btn_up_rect = pygame.Rect(35,  465, 120, 105)
  blue_square_btn_down_rect = pygame.Rect(172, 465, 120, 105)

  btn_scale = 1.2
  red_btn_up = get_scaled_surface(sprite_sheet, red_square_btn_up_rect, btn_scale)
  red_btn_down = get_scaled_surface(sprite_sheet, red_square_btn_down_rect, btn_scale)
  green_btn_up = get_scaled_surface(sprite_sheet, green_square_btn_up_rect, btn_scale)
  green_btn_down = get_scaled_surface(sprite_sheet, green_square_btn_down_rect, btn_scale)
  blue_btn_up = get_scaled_surface(sprite_sheet, blue_square_btn_up_rect, btn_scale)
  blue_btn_down = get_scaled_surface(sprite_sheet, blue_square_btn_down_rect, btn_scale)

  red_btn_rect = red_btn_up.get_rect(topleft=(50, HEIGHT//2 + 50))
  green_btn_rect = green_btn_up.get_rect(topleft=((WIDTH - green_btn_up.get_width())//2 , HEIGHT//2 + 50))
  blue_btn_rect = blue_btn_up.get_rect(topleft=(WIDTH - blue_btn_up.get_width() - 50, HEIGHT//2 + 50))

  pygame.display.set_icon(pygame.transform.smoothscale(red_btn_up, (32, 32)))

  clock = pygame.time.Clock()
  running = True
  isButtonDown = False
  red_count = 0
  green_count = 0
  blue_count = 0
  threshold = 10
  downButtonColor: str | None = None # green, red, blue, or None
  while running:
    isGreenButtonActive = red_count >= threshold
    isBlueButtonActive = green_count >= threshold
    for event in pygame.event.get():
      match event.type:
        case pygame.QUIT:
          running = False
        case pygame.KEYDOWN:
          if event.key == pygame.K_ESCAPE:
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
              red_count = min(red_count + 1, 100)
              if isGreenButtonActive == False and red_count >= threshold:
                btn_up_sound.play() # to indicate green button now active
            elif isGreenButtonActive and green_btn_rect.collidepoint(event.pos):
              downButtonColor = 'green'
              isButtonDown = True
              btn_down_sound.play()
              green_count = min(green_count + 1, 100)
              if isBlueButtonActive == False and green_count >= threshold:
                btn_up_sound.play() # to indicate blue button now active
            elif isBlueButtonActive and blue_btn_rect.collidepoint(event.pos):
              downButtonColor = 'blue'
              isButtonDown = True
              btn_down_sound.play()
              blue_count = min(blue_count + 1, 100)

    # clear background
    #screen.fill((239, 243, 228))
    screen.fill((60, 60, 60))
    #pygame.draw.rect(screen, (239, 243, 228), pygame.Rect(0, HEIGHT//2, WIDTH, HEIGHT//2))

    # guage
    rgb = (red_count // 20, green_count // 20, blue_count // 20)
    guage.draw(screen, (WIDTH-guage.get_width())//2, 100, rgb)

    # red button
    img = red_btn_down if isButtonDown and downButtonColor == 'red' else red_btn_up
    screen.blit(img, red_btn_rect.topleft)

    # green button
    img = green_btn_down if isGreenButtonActive == False or (isButtonDown and downButtonColor == 'green') else green_btn_up
    screen.blit(img, green_btn_rect.topleft)

    # blue button
    img = blue_btn_down if isBlueButtonActive == False or (isButtonDown and downButtonColor == 'blue') else blue_btn_up
    screen.blit(img, blue_btn_rect.topleft)

    # score text
    # Brightness/luminance (perceived lightness) -- Human eye is more sensitive to green, then red, then blue.
    brightness = (0.2126*red_count + 0.7152*green_count + 0.0722*blue_count) / 255
    text_surface = font.render(f"{brightness * 100:.1f}% Done ({red_count}%, {green_count}%, {blue_count}%)", True, (239, 243, 228)) #(0, 0, 0))
    screen.blit(text_surface, (10, 10))

    # color circle
    circle_color = ((red_count / 100) * 255, (green_count / 100) * 255, (blue_count / 100) * 255)
    pygame.draw.circle(screen, circle_color, (138, 210), 60)

    pygame.display.flip()
    clock.tick(FPS)

  pygame.quit()
  sys.exit()

if __name__ == "__main__":
  main()