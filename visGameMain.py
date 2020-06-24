# import the pygame module, so you can use it
import pygame
import time
import random

from Game import Game as MainGame

# define a main function
def main():

  # define a variable to control the main loop
  running = True

  f = open("minecraftaveragedailyplayers.csv", "r")
  data = f.read()
  dates = data.split("\n")
  dates = dates[1:]

  messages = {
      "2020-03-01": "Data begins",
      "2020-03-15": "Shelter in place orders have started",
      "2020-04-07": "All states are sheltering in place",
      "2020-04-24": "States begin reopening"
  }

  max_value = 0
  for date in dates:
    date_val = int(date.split(",")[1])
    if (date_val > max_value):
      max_value = date_val

  max_boids = 200
  starting_boids_number = max_boids * int(dates[0].split(",")[1]) / max_value
  game = MainGame(dates[0].split(",")[0], starting_boids_number)

  then = time.time()
  day_time = 0
  day = 0
  gather_multiplier = 1.0
  start_quarantine = False
  start_reopening = False
  gather_multiplier_delta = 1 / 23
  # main loop
  while running:
    now = time.time()
    delta_time = now - then
    game.update(delta_time)
    then = now

    day_time += delta_time
    if (day_time >= 1.0):
      day_time -= 1.0
      game.day += 1
      if (game.day < len(dates)):
        game.setNumBoids(max_boids * int(dates[game.day].split(",")[1]) / max_value)
        game.date = dates[game.day].split(",")[0]
        if game.date in messages:
          game.message = messages[game.date]
        if game.date == "2020-03-15":
          start_quarantine = True
        if game.date == "2020-04-24":
          start_reopening = True
          start_quarantine = False
        if start_quarantine and gather_multiplier > gather_multiplier_delta:
          gather_multiplier -= gather_multiplier_delta
          game.gather_multiplier = gather_multiplier
        if start_reopening and gather_multiplier < (1.0 - gather_multiplier_delta / 4):
          gather_multiplier += gather_multiplier_delta / 4
          game.gather_multiplier = gather_multiplier
      else:
        # end the game now
        game.show_score_screen = True

    # event handling, gets all event from the event queue
    for event in pygame.event.get():
      # only do something if the event is of type QUIT
      if event.type == pygame.QUIT:
        # change the value to False, to exit the main loop
        running = False

# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
  # call the main function
  main()
