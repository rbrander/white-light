import pygame

from constants import BLACK, LIGHT_COLOR

def draw_text_shadow(surface: pygame.Surface, font: pygame.font.Font, text: str, center: tuple[int, int], shadow_offset: int = 3):
  text_surface = font.render(text, True, LIGHT_COLOR)
  text_shadow = font.render(text, True, BLACK)
  surface.blit(text_shadow, text_shadow.get_rect(center=(center[0]+shadow_offset, center[1]+shadow_offset)))
  surface.blit(text_surface, text_surface.get_rect(center=center))

class TextNode:
  def __init__(self, text, x, y, duration_ms = 1000, speed = 0.25):
    self.text = text
    self.x = x
    self.y = y
    self.duration = duration_ms
    self.speed = speed
    self.elapsed = 0

  def update(self, dt):
    if self.elapsed > self.duration:
      return False # is done
    self.elapsed += dt
    self.y -= dt * self.speed
    return True # to be continued

  def draw(self, surface: pygame.Surface, font: pygame.font.Font, color: pygame.color.Color = (0, 0, 0)):
    if self.elapsed > self.duration:
      return

    alpha = int((1-(self.elapsed/self.duration)) * 255)
    text_surface = font.render(self.text, True, color).convert_alpha()
    text_surface_shadow = font.render(self.text, True, (0,0,0)).convert_alpha()
    if hasattr(text_surface, 'set_alpha'):
        text_surface.set_alpha(alpha)
        text_surface_shadow.set_alpha(alpha)

    surface.blit(text_surface_shadow, text_surface_shadow.get_rect(center=(self.x+3, self.y - 17)))
    surface.blit(text_surface, text_surface.get_rect(center=(self.x, self.y - 20)))


class DisappearingText:
  def __init__(self):
    self.text_nodes:list[TextNode] = []

  def add(self, text: str, pos: tuple[2]):
    self.text_nodes.append(TextNode(text, pos[0], pos[1]))

  def update(self, dt: float):
    alive_nodes:list[TextNode] = []
    for text_node in self.text_nodes:
      if text_node.update(dt) == True:
        alive_nodes.append(text_node)
    self.text_nodes = alive_nodes

  def draw(self, surface: pygame.Surface, font: pygame.font.Font, color: pygame.color.Color = (0, 0, 0)):
    for text_node in self.text_nodes:
      text_node.draw(surface, font, color)
