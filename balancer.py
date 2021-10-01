import pygame
import sys
from colors import *
import math

player = True

width = 500
height = 500

clock = pygame.time.Clock()
screen = pygame.display.set_mode((width, height))
pygame.mouse.set_visible(0)
pygame.display.set_caption('THE BALANCER')

# Physics constants
g = 9.81
m_b = 10
length = 140
I = (1 / 3) * m_b * pow(length, 2)
dt = 0.01

#Variables
base_pos = (250,390)
centroid_pos = (250,320)
top_pos = (250,250)
tht_deg = 0
tht = tht_deg*math.pi/180
tht_dd = 0
tht_d = 0
v_x = 0
a_x = 0
v_y = 0
a_y = 0
R_y = m_b*g


#Controls
R_x = 0
counter = 0

while True:
    clock.tick(60)
    screen.fill(black)

    #Update Positions and Draw
    top_pos = (centroid_pos[0] + 0.5*length*math.sin(tht), centroid_pos[1] - 0.5*length*math.cos(tht))
    base_pos = (centroid_pos[0] - 0.5*length*math.sin(tht), centroid_pos[1] + 0.5*length*math.cos(tht))
    pygame.draw.circle(screen, blue, base_pos, 20)
    pygame.draw.line(screen, white, base_pos, top_pos, 10)
    pygame.display.update()


    #The physics (dynamics)
    a_y = tht_dd*math.sin(tht)*length*0.5 + tht_d*tht_d*length*math.cos(tht)*0.5
    R_y = m_b*a_y - m_b*g
    tht_dd = (-length*0.5*math.cos(tht)*R_x - length*0.5*math.sin(tht)*R_y)/I
    a_x = R_x/m_b - tht_dd*math.cos(tht)*length*0.5 + tht_d*tht_d*0.5*length*math.sin(tht)


    #The integration
    tht_d += dt*tht_dd
    tht += dt*tht_d
    v_x += a_x*dt
    v_y += a_y*dt
    centroid_pos = (centroid_pos[0] + v_x*dt, centroid_pos[1] + v_y*dt)


    if player:
        R_x = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    keys = pygame.key.get_pressed()
    if player:
        if keys[pygame.K_LEFT]:
            R_x = -250
        if keys[pygame.K_RIGHT]:
            R_x = 250
    #else:
        #ML.makeDecisions(tht_dd, tht_d, tht)

