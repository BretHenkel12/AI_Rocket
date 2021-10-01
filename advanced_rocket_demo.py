import pygame
import time
import sys
import numpy as np


player = False
weights = np.array([-0.978,4.0123])

clock = pygame.time.Clock()
screen = pygame.display.set_mode((500,500))
pygame.mouse.set_visible(1)
pygame.display.set_caption('Rocket AI')
x = 240
y = 100.1
engine_force = 0
v = 0
count = 0

score = 0

while True:
    if player==False:
        state = np.array([(400-y)/10,v/10])
        thrust = np.dot(state,weights)
        thrust = 2 / (1 + np.exp(-thrust))
        engine_force = thrust
    clock.tick(60)
    screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                y = 100
                v = 0
                count = 0
                time.sleep(1)
            if (event.key == pygame.K_UP) & player:
                engine_force = 2
                print("up")
        elif (event.type == pygame.KEYUP) & player:
            if event.key == pygame.K_UP:
                engine_force = 0
                print("off")
    grav_force = 1
    a = grav_force - engine_force
    v += a
    y += v*0.02
    # x,y = pygame.mouse.get_pos()
    pygame.draw.rect(screen, (255, 0, 0), (x, int(y), 20, 20))
    pygame.draw.rect(screen, (255,255,255), (0,400,500,100))
    pygame.display.update()
    count+=1
    if (y>=380):
        #print("your speed was")
        #print(v)
        #print("count")
        #print(count)
        print("score")
        print(100 - v - count/10)
        y = 100
        v = 0
        count = 0
        time.sleep(2)
    if (y<=0):
        #print("off top")
        time.sleep(1)
        y = 100
        v = 0
        count = 0
    if (count>5000):
        y = 100
        v = 0
        count = 0
        time.sleep(0.5)