import pygame
import os
from buttons import Buttons
from guage import Guage
from text import DisappearingText, draw_text_shadow
from constants import BLACK, WIDTH,HEIGHT,FPS,LIGHT_COLOR,DARK_COLOR
from utils import draw_grid_overlay, exit_program, format_time


"""
TODO:
- add pygame.mixer.Channel for managing multiple sounds and volume
- upgrade buttons
  - add sound
- if escape pressed, allow continue from main screen
- end game state
  - add sound/music
"""

def game_over_screen(screen: pygame.Surface, play_time_in_ms: int):
  background = screen.copy() # snapshot of the game state at end-of-game

  large_font = pygame.font.Font(os.path.join("assets", "kenney-fonts", "kenvector_future.ttf"), 64)
  medium_font = pygame.font.Font(os.path.join("assets", "kenney-fonts", "kenpixel.ttf"), 48)
  small_font = pygame.font.Font(os.path.join("assets", "kenney-fonts", "kenpixel.ttf"), 24)

  clock = pygame.time.Clock()
  alpha = 0
  running = True
  while running:
    alpha = min(alpha + 3, 255)
    running = alpha < 255

    # listen for events to exit
    for event in pygame.event.get():
      match event.type:
        case pygame.QUIT:
          exit_program()
        case pygame.KEYDOWN:
          if event.key == pygame.K_ESCAPE:
            running = False
            break

    # draw background and white transparent overlay
    screen.blit(background, (0, 0))
    white_surface = pygame.Surface(background.get_size(), pygame.SRCALPHA)
    pygame.draw.rect(white_surface, (255, 255, 255, alpha), white_surface.get_rect())
    screen.blit(white_surface, (0, 0))

    pygame.display.flip()
    clock.tick(FPS)

  # if the alpha is at the max, we can assume the user waited for the animation to finish, otherwise they bailed
  if alpha == 255:
    # draw a grey rectangle
    grey_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    padding = 40
    pygame.draw.rect(grey_surface, (DARK_COLOR.r, DARK_COLOR.g, DARK_COLOR.b, 128), (padding, padding, WIDTH-padding*2, HEIGHT-padding*2), border_radius = padding)
    screen.blit(grey_surface, (0, 0))

    # display text and wait for input to proceed
    heading = "You did it!"
    draw_text_shadow(screen, large_font, heading, (WIDTH//2, 150))

    subheading = "You created white light in"
    text_surface = small_font.render(subheading, True, BLACK)
    screen.blit(text_surface, text_surface.get_rect(center=(WIDTH//2, 300)))

    y_offset = 400
    y_offset_increment = 75
    time_strings = format_time(play_time_in_ms)
    for time_part in time_strings:
      text_surface = medium_font.render(time_part, True, BLACK)
      screen.blit(text_surface, text_surface.get_rect(center=(WIDTH//2, y_offset)))
      y_offset += y_offset_increment

    text_surface = small_font.render("Press a key or Click to exit", True, BLACK)
    screen.blit(text_surface, text_surface.get_rect(center=(WIDTH//2, 725)))

    pygame.display.flip()

    running = True
    while running:
      # listen for events to exit
      for event in pygame.event.get():
        match event.type:
          case pygame.QUIT:
            exit_program()
          case pygame.KEYDOWN:
            pass
          case pygame.MOUSEBUTTONDOWN:
            running = False
            break
      clock.tick(FPS)


def game(screen: pygame.Surface):
  large_font = pygame.font.Font(os.path.join("assets", "kenney-fonts", "kenpixel_high.ttf"), 64)
  medium_font = pygame.font.Font(os.path.join("assets", "kenney-fonts", "kenpixel_high.ttf"), 48)
  small_font = pygame.font.Font(os.path.join("assets", "kenney-fonts", "kenpixel_mini.ttf"), 22)

  btn_up_sound = pygame.mixer.Sound(os.path.join("assets", "button-click-up.ogg"))
  btn_down_sound = pygame.mixer.Sound(os.path.join("assets", "button-click-down.ogg"))
  upgrade_button_sound = pygame.mixer.Sound(os.path.join("assets", "soft-chime.ogg"))
  volume = 0.1
  btn_up_sound.set_volume(volume)
  btn_down_sound.set_volume(volume)
  upgrade_button_sound.set_volume(volume)

  guage = Guage(5, 3.5)

  buttons = Buttons()
  red_btn = buttons.create_rgb("red", "square", (50, HEIGHT//2 + 50))
  red_upgrade_btn = buttons.create_buch((50, HEIGHT//2 + 200), label = "Upgrade")
  btn_width = red_btn.rect.width # all buttons are the same size
  green_btn = buttons.create_rgb("green", "square", ((WIDTH - btn_width)//2 , HEIGHT//2 + 50))
  green_upgrade_btn = buttons.create_buch(((WIDTH - btn_width)//2, HEIGHT//2 + 200), label = "Upgrade")
  blue_btn = buttons.create_rgb("blue", "square", (WIDTH - btn_width - 50, HEIGHT//2 + 50))
  blue_upgrade_btn = buttons.create_buch((WIDTH - btn_width - 50, HEIGHT//2 + 200), label = "Upgrade")

  dt = 0
  clock = pygame.time.Clock()
  start_time = pygame.time.get_ticks()
  running = True
  red_increment = 1
  green_increment = 1
  blue_increment = 1
  red_count = 0 # value of 0 to 100
  green_count = 0 # value of 0 to 100
  blue_count = 0 # value of 0 to 100
  upgrade_cost_increase = 1.2 # next upgrade costs 120% of current upgrade
  red_upgrade_cost = 10 # starts wtih 10 and goes up by 20% each upgrade
  green_upgrade_cost = 10
  blue_upgrade_cost = 10
  disappearing_text = DisappearingText()
  while running:
    # exit check
    is_game_over = red_count >= 100 and green_count >= 100 and blue_count >= 100
    if is_game_over:
      game_over_screen(screen, pygame.time.get_ticks() - start_time)
      running = False
      break

    # update
    isRedUpgradeButtonActive = red_count >= red_upgrade_cost
    isGreenUpgradeButtonActive = green_count >= green_upgrade_cost
    isBlueUpgradeButtonActive = blue_count >= blue_upgrade_cost

    if isRedUpgradeButtonActive:
      # make a sound if the button is being activated (from being inactive)
      if not red_upgrade_btn.is_active:
        btn_up_sound.play()
      red_upgrade_btn.activate()
    else:
      red_upgrade_btn.deactive()

    if isGreenUpgradeButtonActive:
      # make a sound if the button is being activated (from being inactive)
      if not green_upgrade_btn.is_active:
        btn_up_sound.play()
      green_upgrade_btn.activate()
    else:
      green_upgrade_btn.deactive()

    if isBlueUpgradeButtonActive:
      # make a sound if the button is being activated (from being inactive)
      if not blue_upgrade_btn.is_active:
        btn_up_sound.play()
      blue_upgrade_btn.activate()
    else:
      blue_upgrade_btn.deactive()

    def on_red_down(pos):
      nonlocal red_count
      btn_down_sound.play()
      red_count = min(red_count + red_increment, 100)
      disappearing_text.add(f"+{red_increment}", pos)

    def on_green_down(pos):
      nonlocal green_count
      btn_down_sound.play()
      green_count = min(green_count + green_increment, 100)
      disappearing_text.add(f"+{green_increment}", pos)

    def on_blue_down(pos):
      nonlocal blue_count
      btn_down_sound.play()
      blue_count = min(blue_count + blue_increment, 100)
      disappearing_text.add(f"+{blue_increment}", pos)

    def on_btn_up():
      btn_up_sound.play()

    def on_upgrade_red(pos):
      nonlocal red_increment, red_count, red_upgrade_cost
      red_increment += 2
      disappearing_text.add(f"* {red_increment} *", pos)
      upgrade_button_sound.play()
      red_count = max(0, red_count - red_upgrade_cost)
      red_upgrade_cost = int(red_upgrade_cost * upgrade_cost_increase)

    def on_upgrade_green(pos):
      nonlocal green_increment, green_count, green_upgrade_cost
      green_increment += 2
      disappearing_text.add(f"* {green_increment} *", pos)
      upgrade_button_sound.play()
      green_count = max(0, green_count - green_upgrade_cost)
      green_upgrade_cost = int(green_upgrade_cost * upgrade_cost_increase)

    def on_upgrade_blue(pos):
      nonlocal blue_increment, blue_count, blue_upgrade_cost
      blue_increment += 2
      disappearing_text.add(f"* {blue_increment} *", pos)
      upgrade_button_sound.play()
      blue_count = max(0, blue_count - blue_upgrade_cost)
      blue_upgrade_cost = int(blue_upgrade_cost * upgrade_cost_increase)

    for event in pygame.event.get():
      match event.type:
        case pygame.QUIT:
          exit_program()
        case pygame.KEYDOWN:
          if event.key == pygame.K_ESCAPE:
            running = False
            break
      red_btn.handle_event(event, on_down=lambda: on_red_down(event.pos), on_up=on_btn_up)
      red_upgrade_btn.handle_event(event, on_up=lambda: on_upgrade_red(event.pos))
      green_btn.handle_event(event, on_down=lambda: on_green_down(event.pos), on_up=on_btn_up)
      green_upgrade_btn.handle_event(event, on_up=lambda: on_upgrade_green(event.pos))
      blue_btn.handle_event(event, on_down=lambda: on_blue_down(event.pos), on_up=on_btn_up)
      blue_upgrade_btn.handle_event(event, on_up=lambda: on_upgrade_blue(event.pos))

    disappearing_text.update(dt)

    # clear background
    screen.fill(DARK_COLOR)

    # guage
    rgb = (red_count // 20, green_count // 20, blue_count // 20)
    guage.draw(screen, (WIDTH-guage.get_width())//2, 100, rgb)

    # red button
    red_btn.draw(screen)
    red_upgrade_btn.draw(screen, small_font)
    # percent complete
    text_surface = medium_font.render(f"{red_count}%", True, LIGHT_COLOR)
    screen.blit(text_surface, text_surface.get_rect(center=(red_btn.rect.centerx, red_btn.rect.top - 30)))
    # upgrade cost text
    text_surface = small_font.render(f"cost {red_upgrade_cost}", True, LIGHT_COLOR)
    screen.blit(text_surface, text_surface.get_rect(center=(red_upgrade_btn.rect.centerx, red_upgrade_btn.rect.bottom + 20)))

    # green button
    green_btn.draw(screen)
    green_upgrade_btn.draw(screen, small_font)
    # percent complete
    text_surface = medium_font.render(f"{green_count}%", True, LIGHT_COLOR)
    screen.blit(text_surface, text_surface.get_rect(center=(green_btn.rect.centerx, green_btn.rect.top - 30)))
    # upgrade cost text
    text_surface = small_font.render(f"cost {green_upgrade_cost}", True, LIGHT_COLOR)
    screen.blit(text_surface, text_surface.get_rect(center=(green_upgrade_btn.rect.centerx, green_upgrade_btn.rect.bottom + 20)))

    # blue button
    blue_btn.draw(screen)
    blue_upgrade_btn.draw(screen, small_font)
    # percent complete
    text_surface = medium_font.render(f"{blue_count}%", True, LIGHT_COLOR)
    screen.blit(text_surface, text_surface.get_rect(center=(blue_btn.rect.centerx, blue_btn.rect.top - 30)))
    # upgrade cost text
    text_surface = small_font.render(f"cost {blue_upgrade_cost}", True, LIGHT_COLOR)
    screen.blit(text_surface, text_surface.get_rect(center=(blue_upgrade_btn.rect.centerx, blue_upgrade_btn.rect.bottom + 20)))


    # score text
    # Brightness/luminance (perceived lightness) -- Human eye is more sensitive to green, then red, then blue.
    brightness = (0.2126*red_count + 0.7152*green_count + 0.0722*blue_count)
    heading = f"{brightness:.1f} %"
    draw_text_shadow(screen, large_font, heading, (WIDTH//2, 50))

    # color circle
    circle_color = ((red_count / 100) * 255, (green_count / 100) * 255, (blue_count / 100) * 255)
    pygame.draw.circle(screen, circle_color, (138, 210), 60)

    disappearing_text.draw(screen, medium_font, LIGHT_COLOR)

    pygame.display.flip()
    dt = clock.tick(FPS)


