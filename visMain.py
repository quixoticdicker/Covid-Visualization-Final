# import the pygame module, so you can use it
import pygame
import time
import random

# define a main function
def main():
    
    # initialize the pygame module
    pygame.init()
    # load and set the logo
    logo = pygame.image.load("icon.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("Game Usage During Quarantine")
    
    pygame.font.init()
    font = pygame.font.SysFont("Courier", 20)
    
    messages = {
      "2020-03-01": "Data begins",
      "2020-03-15": "Shelter in place orders have started",
      "2020-04-07": "All states are sheltering in place",
      "2020-04-24": "States begin reopening"
    }

    width = 640
    height = 480
    # create a surface on screen that has the size of 640 x 480
    screen = pygame.display.set_mode((width, height))

    # define a variable to control the main loop
    running = True

    screen_glow = pygame.image.load("screen_glow.png")
    road_horizontal = pygame.image.load("road_horizontal.png")
    road_vertical = pygame.image.load("road_vertical.png")
    intersection = pygame.image.load("intersection.png")
    house = pygame.image.load("house.png")

    off_lights = []
    on_lights = []

    road_x_start = 96
    road_x_gap = 136

    for i in range(road_x_start, width, road_x_gap):
      screen.blit(road_vertical, (i, 0))

    road_y_start = 90
    road_y_gap = 130

    for i in range(road_y_start, height, road_y_gap):
      screen.blit(road_horizontal, (0, i))

    for i in range(road_x_start, width, road_x_gap):
      for j in range(road_y_start, height, road_y_gap):
        screen.blit(intersection, (i-1, j-1))

    for i in range(0, width, road_x_gap):
      for j in range(0, height, road_y_gap):
        screen.blit(house, (i, j))
        off_lights.append((i + 14, j + 26))
        off_lights.append((i + 50, j + 26))
        off_lights.append((i + 14, j + 49))
        off_lights.append((i + 50, j + 49))

    f = open("multiTimeline.csv", "r")
    data = f.read()
    dates = data.split("\n")
    interest = float(dates[3].split(",")[1])
    num_lights = (interest / 1.25)
    while (num_lights > len(on_lights)):
      # turn on a random light
      on_lights.append(off_lights.pop(random.randrange(len(off_lights))))

    for light in on_lights:
      screen.blit(screen_glow, light)

    start_date = dates[3].split(",")[0]
    if start_date in messages:
      message_screen = font.render(messages[start_date], False, (255, 255, 255), (0, 0, 0))
      screen.blit(message_screen, (screen.get_width() - message_screen.get_width(), 110 - (message_screen.get_height() / 2)))

    date_screen = font.render(start_date, False, (255, 255, 255), (0, 0, 0))
    screen.blit(date_screen, (0, 110 - (date_screen.get_height() / 2)))

    title_screen = font.render("Google searches of \"play games on zoom\"", False, (255, 255, 255), (0, 0, 0))
    screen.blit(title_screen, (0, 370 - (title_screen.get_height() / 2)))

    pygame.display.flip()

    seconds = time.time()
    last = seconds
    day = 3
    # main loop
    while running:
        seconds = time.time()
        if (seconds - last > 1):
            last = seconds
            day = day + 1
            if (day >= len(dates) - 1):
              day = 3
            interest = float(dates[day].split(",")[1])
            date = dates[day].split(",")[0]
            date_screen = font.render(date, False, (255, 255, 255), (0, 0, 0))
            
            if date in messages:
              message_screen = font.render(messages[date], False, (255, 255, 255), (0, 0, 0))
              # blit the road first to clear out the previous text
              screen.blit(road_horizontal, (0, road_y_start))
              for i in range(road_x_start, width, road_x_gap):
                screen.blit(intersection, (i-1, road_y_start - 1))
              screen.blit(message_screen, (screen.get_width() - message_screen.get_width(), 110 - (message_screen.get_height() / 2)))
            
            # don't need to blit the road before this because the date is always the same width
            screen.blit(date_screen, (0, 110 - (date_screen.get_height() / 2)))
            
            num_lights = int(interest / 1.25)
            prev_lights = len(on_lights)
            while (num_lights < len(on_lights)):
              off_lights.append(on_lights.pop(random.randrange(len(on_lights))))
            while (num_lights > len(on_lights)):
              on_lights.append(off_lights.pop(random.randrange(len(off_lights))))

            for i in range(0, width, road_x_gap):
              for j in range(0, height, road_y_gap):
                screen.blit(house, (i, j))
            for light in on_lights:
              screen.blit(screen_glow, light)
            pygame.display.flip()

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
