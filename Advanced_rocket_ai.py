import pygame
import time
import sys
import numpy as np
import cv2 as cv
from pygame.locals import *
import random
import pandas as pd


df = pd.DataFrame({
    'w1':[None],
    'w2':[None],
    'score':[None],
    'v':[None]
})


clock = pygame.time.Clock()
screen = pygame.display.set_mode((500,500))
pygame.mouse.set_visible(1)
pygame.display.set_caption('Rocket AI')
x = 240
y = 100.1
engine_force = 0
v = 0
count = 0
df.loc[0,'w1'] = random.randrange(-100,100)/100
df.loc[0,'w2'] = random.randrange(-100,100)/100
advanced = False
score = 0
reps = 0
while reps<200:
    state = np.array([(400-y)/10,v/10])
    weights_df = df.iloc[reps]['w1':'w2']
    thrust = np.dot(state,weights_df)
    thrust = 2 / (1 + np.exp(-thrust))
    engine_force = thrust
    #clock.tick(60)
    screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                y = 100
                v = 0
                count = 0
                reps += 1
                if advanced:
                    df.loc[reps] = [seed_weight_1 + random.randrange(-100, 100) / 1000,
                                    seed_weight_2 + random.randrange(-100, 100) / 1000, None, None]
                else:
                    df.loc[reps] = [random.randrange(-100, 100) / 100, random.randrange(-100, 100) / 100, None, None]
                #time.sleep(0.5)

            '''if event.key == pygame.K_UP:
                engine_force = 2
                print("up")
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                engine_force = 0
                print("off")
        '''
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
        score = 100 - v - count/20
        df.loc[reps,'score'] = score
        df.loc[reps,'v'] = v
        #time.sleep(2)
        y = 100
        v = 0
        count = 0
        reps += 1
        score = 0
        if advanced:
            df.loc[reps] = [seed_weight_1 + random.randrange(-100, 100) / 1000,
                            seed_weight_2 + random.randrange(-100, 100) / 1000, None, None]
        else:
            df.loc[reps] = [random.randrange(-100, 100) / 100, random.randrange(-100, 100) / 100, None, None]
        print(reps)
    if (y<=0):
        #print("off top")
        #time.sleep(2)
        y = 100
        v = 0
        count = 0
        df.loc[reps, 'score'] = score
        df.loc[reps, 'v'] = v
        reps+=1
        if advanced:
            df.loc[reps] = [seed_weight_1 + random.randrange(-100, 100) / 1000,
                            seed_weight_2 + random.randrange(-100, 100) / 1000, None, None]
        else:
            df.loc[reps] = [random.randrange(-100, 100) / 100, random.randrange(-100, 100) / 100, None, None]
        print(reps)
    if (count>4000):
        #print("too long")
        y = 100
        v = 0
        count = 0
        df.loc[reps, 'score'] = score
        df.loc[reps, 'v'] = v
        reps += 1
        if advanced:
            df.loc[reps] = [seed_weight_1 + random.randrange(-100, 100) / 1000, seed_weight_2 + random.randrange(-100, 100) / 1000, None, None]
        else:
            df.loc[reps] = [random.randrange(-100, 100) / 100, random.randrange(-100, 100) / 100, None, None]
        print(reps)
    if (reps>100):
        advanced = True
        mask = df['score'] == df.score.max()
        best = df[mask]
        seed_weight_1 = float(best['w1'])
        seed_weight_2 = float(best['w2'])
    if (reps>200):
        advanced = True
print(df)
mask = df['score'] == df.score.max()
best = df[mask]
seed_weight_1 = float(best['w1'])
seed_weight_2 = float(best['w2'])
print(best)
print(seed_weight_1)
print(seed_weight_2)