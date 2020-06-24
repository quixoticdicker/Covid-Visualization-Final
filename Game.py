import pygame
import random
import math

from Boid import Boid

class Game:

  def __init__(self, start_date, num_boids):
    pygame.init()
    logo = pygame.image.load("icon.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("Game Usage During Quarantine")
    
    pygame.font.init()
    self.font = pygame.font.SysFont("Courier", 20)
    
    self.date = start_date
    self.message = ""
    self.title = "Average Daily Minecraft Players"
    self.score = 0
    self.gather_multiplier = 1.0
    self.boid_radius = 5
    self.can_collide = True
    self.invincible_counter = 0
    self.day = 0
    
    self.show_score_screen = False
    
    width = 640
    height = 480
    self.screen = pygame.display.set_mode((width, height))
    
    self.player_loc = [width / 2, height / 2]

    self.running = True
    
    self.score_panel_height = 64
    self.boid_vision = 32
    self.world_bounds = (width, height - self.score_panel_height)
    
    # create boids
    self.boids = []
    for i in range(int(num_boids)):
      self.boids.append(Boid((random.random() * width,random.random() * (height - self.score_panel_height)), self.boid_radius, 100))
    
    self.drawScorePanel()
    self.drawBoidPanel()

  def setNumBoids(self, num):
    while (num > len(self.boids)):
      self.boids.append(Boid((random.random() * self.screen.get_width(),random.random() * (self.screen.get_height() - self.score_panel_height)), self.boid_radius, 100))
    while (len(self.boids) > 0 and num < len(self.boids)):
      self.boids.pop(random.randrange(len(self.boids)))

  def drawScorePanel(self):
    pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect((0, 0), (self.screen.get_width(), self.score_panel_height)))
    
    date_screen = self.font.render(self.date, False, (255, 255, 255), (0, 0, 0))
    message_screen = self.font.render(self.message, False, (255, 255, 255), (0, 0, 0))
    title_screen = self.font.render(self.title, False, (255, 255, 255), (0, 0, 0))
    score_screen = self.font.render("score: {0}".format(self.score) , False, (255, 255, 255), (0, 0, 0))
    text_y  = (self.score_panel_height / 4) - (date_screen.get_height() / 2)
    text_y2 = (self.score_panel_height * 3 / 4) - (date_screen.get_height() / 2)
    self.screen.blit(title_screen, (0, text_y))
    self.screen.blit(score_screen, (0, text_y2))
    self.screen.blit(date_screen, (self.screen.get_width() - date_screen.get_width(), text_y))
    self.screen.blit(message_screen, (self.screen.get_width() - message_screen.get_width(), text_y2))
    pygame.display.flip()

  def drawBoidPanel(self):
    pygame.draw.rect(self.screen, (32, 32, 32), pygame.Rect((0, self.score_panel_height), (self.screen.get_width(), self.screen.get_height() - self.score_panel_height)))
    
    if (self.show_score_screen):
      final_font = pygame.font.SysFont("Courier", 40)
      final_score_screen = final_font.render("final score: {0}".format(self.score), False, (255, 255, 255), (32, 32, 32))
      restart_screen = self.font.render("restart? (y/n)", False, (255, 255, 255), (32, 32, 32))
      self.screen.blit(final_score_screen, ((self.screen.get_width() / 2) - (final_score_screen.get_width() / 2), (self.screen.get_height() / 2) - (final_score_screen.get_height() / 2)))
      self.screen.blit(restart_screen, ((self.screen.get_width() / 2) - (restart_screen.get_width() / 2), (self.screen.get_height() / 2) + (final_score_screen.get_height() / 2)))
    else:
      for boid in self.boids:
        pygame.draw.circle(self.screen, (0, 255, 0), (int(boid.position[0]), self.score_panel_height + int(boid.position[1])), boid.radius)
      pygame.draw.circle(self.screen, (255, 0, 0), (int(self.player_loc[0]), self.score_panel_height + int(self.player_loc[1])), self.boid_radius)
      pygame.display.flip()

  def distance(pos1, pos2):
    dx = pos1[0] - pos2[0]
    dy = pos1[1] - pos2[1]
    return math.sqrt(dx * dx + dy * dy)

  def update(self, delta_time):
    down_keys = pygame.key.get_pressed()
  
    # check if reset
    if (self.show_score_screen):
      # listen for y or n
      if (down_keys[pygame.K_y]):
        # restart
        self.day = 0
        self.show_score_screen = False
        self.score = 0
      elif (down_keys[pygame.K_n]):
        exit()

    # move player
    down_keys = pygame.key.get_pressed()
    player_speed = 200
    player_velocity = [0, 0]
    if (down_keys[pygame.K_UP]):
      player_velocity[1] -= 1
    if (down_keys[pygame.K_DOWN]):
      player_velocity[1] += 1
    if (down_keys[pygame.K_LEFT]):
      player_velocity[0] -= 1
    if (down_keys[pygame.K_RIGHT]):
      player_velocity[0] += 1
    player_velocity = Boid.normalize(player_velocity, player_speed)
    self.player_loc[0] += player_velocity[0] * delta_time
    self.player_loc[1] += player_velocity[1] * delta_time
    self.player_loc[0] = max(0, min(self.player_loc[0], self.world_bounds[0]))
    self.player_loc[1] = max(0, min(self.player_loc[1], self.world_bounds[1]))

    # check boid colision with player
    if (self.can_collide):
      for boid in self.boids:
        dist = Game.distance(self.player_loc, boid.position)
        if dist < self.boid_radius * 2:
          self.score += 1
          self.can_collide = False
    else:
      self.invincible_counter += delta_time
      if (self.invincible_counter > 1.0):
        self.can_collide = True
        self.invincible_counter = 0

    # calculate new boid vectors
    for boid1 in self.boids:
      near_boids = []
      for boid2 in self.boids:
        if (boid1 != boid2):
          if (Boid.distance(boid1, boid2) < self.boid_vision):
            near_boids.append(boid2)
      boid1.calculateAcceleration(near_boids, 1, self.gather_multiplier, self.gather_multiplier)

    # move boids
    for boid in self.boids:
      boid.move(delta_time, self.world_bounds)

    # draw screen
    self.drawScorePanel()
    self.drawBoidPanel()
