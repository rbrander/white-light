"""
TODO:
- add menu
  - add new game
  - add save game
  - add quit game
- add end game state
  - add sound
  - fade to white
  - go back to menu
- add a way to upgrade buttons (so they contribute more)
"""

import pygame
import sys
import os
from buttons import Buttons
from guage import Guage
from utils import get_scaled_surface
from text import DisappearingText

GAME_NAME = "Button Burst"
WIDTH, HEIGHT = 600, 800
FPS = 60
LIGHT_COLOR = pygame.color.Color(239, 243, 228)
DARK_COLOR = pygame.color.Color(60, 60, 60)

def main():
  pygame.init()
  screen = pygame.display.set_mode((WIDTH, HEIGHT))
  pygame.display.set_caption(GAME_NAME)

  font = pygame.font.Font(os.path.join("assets", "kenney-fonts", "kenpixel_mini.ttf"), 42)
  btn_up_sound = pygame.mixer.Sound(os.path.join("assets", "button-click-up.ogg"))
  btn_down_sound = pygame.mixer.Sound(os.path.join("assets", "button-click-down.ogg"))

  guage = Guage(5, 3.5)

  buttons = Buttons()
  red_btn = buttons.create("red", "square", (50, HEIGHT//2 + 50))
  btn_width = red_btn.rect.width # all buttons are the same size
  green_btn = buttons.create("green", "square", ((WIDTH - btn_width)//2 , HEIGHT//2 + 50))
  blue_btn = buttons.create("blue", "square", (WIDTH - btn_width - 50, HEIGHT//2 + 50))

  pygame.display.set_icon(pygame.transform.smoothscale(red_btn.up, (32, 32)))

  dt = 0
  clock = pygame.time.Clock()
  running = True
  red_count = 0
  green_count = 0
  blue_count = 0
  threshold = 10 # how many clicks until the next button is unlocked
  disappearing_text = DisappearingText()
  while running:
    # update
    isGreenButtonActive = red_count >= threshold
    isBlueButtonActive = green_count >= threshold

    def on_red_down(pos):
      nonlocal red_count
      btn_down_sound.play()
      red_count = min(red_count + 1, 100)
      disappearing_text.add("+1", pos)
      if isGreenButtonActive == False and red_count >= threshold:
        btn_up_sound.play() # to indicate green button now active

    def on_green_down(pos):
      nonlocal green_count
      btn_down_sound.play()
      green_count = min(green_count + 1, 100)
      disappearing_text.add("+1", pos)
      if isBlueButtonActive == False and green_count >= threshold:
        btn_up_sound.play() # to indicate blue button now active

    def on_blue_down(pos):
      nonlocal blue_count
      btn_down_sound.play()
      disappearing_text.add("+1", pos)
      blue_count = min(blue_count + 1, 100)

    def on_btn_up():
      btn_up_sound.play()

    for event in pygame.event.get():
      match event.type:
        case pygame.QUIT:
          running = False
          break
        case pygame.KEYDOWN:
          if event.key == pygame.K_ESCAPE:
            running = False
            break
      red_btn.handle_event(event, on_down=lambda: on_red_down(event.pos), on_up=on_btn_up)
      if isGreenButtonActive:
        green_btn.handle_event(event, on_down=lambda: on_green_down(event.pos), on_up=on_btn_up)
      if isBlueButtonActive:
        blue_btn.handle_event(event, on_down=lambda: on_blue_down(event.pos), on_up=on_btn_up)

    disappearing_text.update(dt)

    # clear background
    screen.fill(DARK_COLOR)

    # guage
    rgb = (red_count // 20, green_count // 20, blue_count // 20)
    guage.draw(screen, (WIDTH-guage.get_width())//2, 100, rgb)

    # red button
    red_btn.draw(screen)

    # green button
    if isGreenButtonActive:
      green_btn.draw(screen)
    else:
      screen.blit(green_btn.down, green_btn.rect.topleft)

    # blue button
    if isBlueButtonActive:
      blue_btn.draw(screen)
    else:
      screen.blit(blue_btn.down, blue_btn.rect.topleft)

    # score text
    # Brightness/luminance (perceived lightness) -- Human eye is more sensitive to green, then red, then blue.
    brightness = (0.2126*red_count + 0.7152*green_count + 0.0722*blue_count) / 255
    text_surface = font.render(f"{brightness * 100:.1f}% Done ({red_count}%, {green_count}%, {blue_count}%)", True, LIGHT_COLOR)
    text_shadow = font.render(f"{brightness * 100:.1f}% Done ({red_count}%, {green_count}%, {blue_count}%)", True, (0, 0, 0))
    shadow_offset = 3
    screen.blit(text_shadow, text_shadow.get_rect(center=(WIDTH//2+shadow_offset, 50+shadow_offset)))
    screen.blit(text_surface, text_surface.get_rect(center=(WIDTH//2, 50)))

    # color circle
    circle_color = ((red_count / 100) * 255, (green_count / 100) * 255, (blue_count / 100) * 255)
    pygame.draw.circle(screen, circle_color, (138, 210), 60)

    disappearing_text.draw(screen, font, LIGHT_COLOR)

    pygame.display.flip()
    dt = clock.tick(FPS)

  pygame.quit()
  sys.exit()

if __name__ == "__main__":
  main()