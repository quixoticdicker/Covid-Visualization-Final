import random
import math

class Boid:
  def __init__(self, pos, rad, max_speed):
    self.position = pos
    self.radius = rad
    self.max_speed = max_speed
    
    # randomly choose initial velocity
    rad = random.random() * math.pi * 2
    component_x = math.cos(rad) * self.max_speed
    component_y = math.sin(rad) * self.max_speed
    self.velocity = (component_x, component_y)
    # not necessary, but let's set it anyway
    self.next_velocity = self.velocity

  # a couple of static utility functions
  
  def normalize(vect, desired_magnitude = 1):
    magnitude = math.sqrt(vect[0] * vect[0] + vect[1] * vect[1])
    if magnitude == 0:
      magnitude = 0.1
    mult = desired_magnitude / magnitude
    return (vect[0] * mult, vect[1] * mult)

  def distance(boid1, boid2):
    dx = boid1.position[0] - boid2.position[0]
    dy = boid1.position[1] - boid2.position[1]
    return math.sqrt(dx * dx + dy * dy)

  # end of static utility functions

  def move(self, delta_time, bounds):
    self.velocity = Boid.normalize((self.velocity[0] + self.change[0], self.velocity[1] + self.change[1]), self.max_speed)
    new_x = self.position[0] + (self.velocity[0] * delta_time)
    new_y = self.position[1] + (self.velocity[1] * delta_time)

    # bounds will cause wrap-around
    #while (new_x > bounds[0]):
    #  new_x = new_x - bounds[0]
    #while (new_x < 0):
    #  new_x = new_x + bounds[0]
    #while (new_y > bounds[1]):
    #  new_y = new_y - bounds[1]
    #while (new_y < 0):
    #  new_y = new_y + bounds[1]
    
    # bounds will cause bounce
    if (new_x > bounds[0]):
      new_x = bounds[0] - (new_x - bounds[0])
      self.velocity = (-self.velocity[0], self.velocity[1])
    if (new_x < 0):
      new_x = - new_x
      self.velocity = (-self.velocity[0], self.velocity[1])
    if (new_y > bounds[1]):
      new_y = bounds[1] - (new_y - bounds[1])
      self.velocity = (self.velocity[0], -self.velocity[1])
    if (new_y < 0):
      new_y = - new_y
      self.velocity = (self.velocity[0], -self.velocity[1])
    self.next_velocity = self.velocity
    self.position = (new_x, new_y)

  # velocity is a combination of:
  # avoiding other boids,
  # following similar velocities, and
  # moving towards the center of the group
  def calculateVelocity(self, nearby_boids, separation_weight, alignment_weight, cohesion_weight):
    # no changes if there are no nearby boids
    if (len(nearby_boids) == 0):
      return

    sum_dx = 0
    sum_dy = 0
    for boid in nearby_boids:
      #dist = Boid.distance(self, boid)
      away_vect = Boid.normalize((self.position[0] - boid.position[0], self.position[1] - boid.position[1]))
      sum_dx = sum_dx - away_vect[0]# / (abs(dist)))
      sum_dy = sum_dy - away_vect[1]# / (abs(dist)))
    avoid_vector = (sum_dx, sum_dy)

    sum_vx = 0
    sum_vy = 0
    for boid in nearby_boids:
      sum_vx = sum_vx + boid.velocity[0]
      sum_vy = sum_vy + boid.velocity[1]
    ave_vx = sum_vx / len(nearby_boids)
    ave_vy = sum_vy / len(nearby_boids)
    match_vector = Boid.normalize((ave_vx, ave_vy))

    sum_x = 0
    sum_y = 0
    for boid in nearby_boids:
      sum_x = sum_x - boid.position[0]
      sum_y = sum_y - boid.position[1]
    center_x = sum_x / len(nearby_boids)
    center_y = sum_y / len(nearby_boids)
    center_vector = Boid.normalize((center_x - self.position[0], center_y - self.position[1]))

    new_velocity = Boid.normalize(((avoid_vector[0] * separation_weight) + (match_vector[0] * alignment_weight) + (center_vector[0] * cohesion_weight), (avoid_vector[1] * separation_weight) + (match_vector[1] * alignment_weight) + (center_vector[1] * cohesion_weight)))

    self.next_velocity = (new_velocity[0] * self.max_speed, new_velocity[1] * self.max_speed)


  def calculateAcceleration(self, nearby_boids, separation_weight, alignment_weight, cohesion_weight):
    if (len(nearby_boids) == 0):
      self.change = [0, 0]
      return
  
    repulsive_force = [0, 0]
    g = 4500
    for boid in nearby_boids:
      dist = Boid.distance(self, boid)
      away_vect = Boid.normalize((self.position[0] - boid.position[0], self.position[1] - boid.position[1]))
      repulsive_force[0] = repulsive_force[0] - g * (away_vect[0] / (dist * dist))
      repulsive_force[1] = repulsive_force[1] - g * (away_vect[1] / (dist * dist))

    center = [0, 0]
    h = 30
    for boid in nearby_boids:
      center[0] = center[0] + boid.position[0]
      center[1] = center[1] + boid.position[1]
    center[0] = center[0] / len(nearby_boids)
    center[1] = center[1] / len(nearby_boids)
    attractive_force = Boid.normalize((self.position[0] - center[0], self.position[1] - center[1]), h)
    
    directive_force = [0, 0]
    f = 30
    for boid in nearby_boids:
      directive_force[0] = directive_force[0] + f * boid.velocity[0]
      directive_force[1] = directive_force[1] + f * boid.velocity[1]
    directive_force = Boid.normalize(directive_force)

    self.change = [-attractive_force[0] * cohesion_weight - repulsive_force[0] * separation_weight - directive_force[0] * alignment_weight, -attractive_force[1] * cohesion_weight - repulsive_force[1] * separation_weight - directive_force[1] * alignment_weight]
