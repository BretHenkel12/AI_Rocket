import pygame
import time
from colors import *
from mapVals import *
import pandas as pd
import random
import sys

#Set the screen parameters
width = 400
height = 250
#Set up the parameters for drawing
#New things
radius = 10
line_width = 2
#Do you want two hidden layers
double_hidden = True

#Set up the stuff for pygame
clock = pygame.time.Clock()
screen = pygame.display.set_mode((width, height))
pygame.mouse.set_visible(0)
pygame.display.set_caption('MY NETWORK')

#Allows the weighted arrays to be randomly seeded
def seed_weights(h, rows):
    seeds = []
    for i in range(rows):
        seeds.append(random.randrange(-100, 100) / 100)
    return (seeds)

#These are the color ranges that are used for the lines
redRange = (130,255)
greenRange = (77,255)

#The main loop
while True:
    #Control frame rate
    clock.tick(2)
    #Find random values for a, h1, h2, and z
    a = random.randrange(1,6)
    h1 = random.randrange(1,6)
    h2 = random.randrange(1,6)
    z = random.randrange(1,6)

    #Seed the first weighted array
    h1_weights = pd.DataFrame()
    for i in range(h1):
        seeds = seed_weights(h1,a)
        h1_weights[i] = seeds
    #Seed the second weighted array
    h2_weights = pd.DataFrame()
    for i in range(h2):
        seeds = seed_weights(h2, h1)
        h2_weights[i] = seeds
    if (double_hidden):
        # Seed the final weighted array
        z_weights = pd.DataFrame()
        for i in range(z):
            seeds = seed_weights(z, h2)
            z_weights[i] = seeds
    else:
        #Seed the final weighted array
        z_weights = pd.DataFrame()
        for i in range(z):
            seeds = seed_weights(z,h1)
            z_weights[i] = seeds
    #Sets the x location of the circles
    if (double_hidden):
        a_x = 50
        h1_x = 150
        h2_x = 250
        z_x = 350
    else:
        a_x = 50
        h1_x = 200
        z_x = 350
        h2_x = 0

    #Finds equal vertical spacing for the circles
    a_yspace = height/(a+1)
    h1_yspace = height/(h1+1)
    h2_yspace = height/(h2+1)
    z_yspace = height/(z+1)

    a_pos = []
    h1_pos = []
    h2_pos = []
    z_pos = []

    #Fills the screen with black
    screen.fill(black)

    #Find all of the positions of the circles
    a_y_current = 0
    for i in range(a):
        a_y_current += a_yspace
        a_pos.append((a_x,a_y_current))
    h1_y_current = 0
    for i in range(h1):
        h1_y_current += h1_yspace
        h1_pos.append((h1_x, h1_y_current))
    z_y_current = 0
    for i in range(z):
        z_y_current += z_yspace
        z_pos.append((z_x, z_y_current))
    if (double_hidden):
        h2_y_current = 0
        for i in range(h2):
            h2_y_current += h2_yspace
            h2_pos.append((h2_x, h2_y_current))

    #draws in the lines
    for i in range(a):
        for j in range(h1):
            w = h1_weights.iloc[i][j]
            if (w < 0):
                color = (mapVals(w, redRange),0,0)
            else:
                color = (0,mapVals(w, greenRange),0)
            pygame.draw.line(screen, color, a_pos[i], h1_pos[j], line_width)
    if (double_hidden):
        for i in range(h1):
            for j in range(h2):
                w = h2_weights.iloc[i][j]
                if (w < 0):
                    color = (mapVals(w, redRange), 0, 0)
                else:
                    color = (0, mapVals(w, greenRange), 0)
                pygame.draw.line(screen, color, h1_pos[i], h2_pos[j], line_width)
        for i in range(h2):
            for j in range(z):
                w = z_weights.iloc[i][j]
                if (w < 0):
                    color = (mapVals(w, redRange), 0, 0)
                else:
                    color = (0, mapVals(w, greenRange), 0)
                pygame.draw.line(screen, color, h2_pos[i], z_pos[j], line_width)
    else:
        for i in range(h1):
            for j in range(z):
                w = z_weights.iloc[i][j]
                if (w < 0):
                    color = (mapVals(w, redRange), 0, 0)
                else:
                    color = (0, mapVals(w, greenRange), 0)
                pygame.draw.line(screen, color, h1_pos[i], z_pos[j], line_width)

    #draw the circles
    for i in range(a):
        pygame.draw.circle(screen, white, a_pos[i], radius)
    for i in range(h1):
        pygame.draw.circle(screen, white, h1_pos[i], radius)
    for i in range(z):
        pygame.draw.circle(screen, white, z_pos[i], radius)
    if (double_hidden):
        for i in range(h2):
            pygame.draw.circle(screen, white, h2_pos[i], radius)

    pygame.display.update()
    #print(inter_weights)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()