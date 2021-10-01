#Imports
import pygame
import sys
import numpy as np
import random
import pandas as pd

#User Setup
v_vs_t = 0.30   #0 to 1, higher is saying v is more important
how_many_per_gen = 10
generations = 5
shrinking_factor = 10
max_v_allowed = 30

#Creating the Data Frame
df = pd.DataFrame({
    'w1':[None],
    'w2':[None],
    'score':[None],
    'v':[None],
    'count':[None]
})


#Setting up Python
clock = pygame.time.Clock()
screen = pygame.display.set_mode((500,500))
pygame.mouse.set_visible(1)
pygame.display.set_caption('Rocket AI')

#Initial State
x = 240
y = 100.1
engine_force = 0
v = 0

#Initial Settings
count = 0
df.loc[0,'w1'] = random.randrange(-100,100)/100
df.loc[0,'w2'] = random.randrange(-100,100)/100
advanced = False
score = 0
reps = 0
repset = 1

#The Loop
while reps<how_many_per_gen*generations:
    #Calculates the decision
    state = np.array([(400-y)/10,v/10])
    weights_df = df.iloc[reps]['w1':'w2']
    thrust = np.dot(state,weights_df)
    thrust = 2 / (1 + np.exp(-thrust))
    engine_force = thrust

    #clock.tick(60)
    #screen.fill((0,0,0))

    #Waits for key presses or the escape
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
                    df.loc[reps] = [seed_weight_1 + random.randrange(-100, 100) / (100*repset), seed_weight_2 + random.randrange(-100, 100) / (shrinking_factor*repset), None, None, None]
                else:
                    df.loc[reps] = [random.randrange(-100, 100) / 100, random.randrange(-100, 100) / 100, None, None, None]
                #time.sleep(0.5)

                #User Input Section
            '''if event.key == pygame.K_UP:
                engine_force = 2
                print("up")
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                engine_force = 0
                print("off")
        '''

    #Determines the kinematics
    grav_force = 1
    a = grav_force - engine_force
    v += a
    y += v*0.02

    #If using graphical interface
    # x,y = pygame.mouse.get_pos()
    #pygame.draw.rect(screen, (255, 0, 0), (x, int(y), 20, 20))
    #pygame.draw.rect(screen, (255,255,255), (0,400,500,100))
    #pygame.display.update()
    count+=1

    #Checks for impact
    if (y>=380):
        score = 1000 - v*25*v_vs_t - count*(1-v_vs_t)
        if v>max_v_allowed:
            score = v/1000
        df.loc[reps,'score'] = score
        df.loc[reps,'v'] = v
        df.loc[reps,'count'] = count
        #time.sleep(2)
        y = 100
        v = 0
        count = 0
        reps += 1
        score = 0
        if advanced:
            df.loc[reps] = [seed_weight_1 + random.randrange(-100, 100) / (100*repset), seed_weight_2 + random.randrange(-100, 100) / (shrinking_factor*repset), None, None, None]
        else:
            df.loc[reps] = [random.randrange(-100, 100) / 100, random.randrange(-100, 100) / 100, None, None,None]
        print(reps)

    if (y<=0 or count>4000):
        #time.sleep(2)
        y = 100
        v = 0
        count = 0
        df.loc[reps, 'score'] = score
        df.loc[reps, 'v'] = v
        df.loc[reps, 'count'] = count
        reps+=1
        if advanced:
            df.loc[reps] = [seed_weight_1 + random.randrange(-100, 100) / (100*repset), seed_weight_2 + random.randrange(-100, 100) / (shrinking_factor*repset), None, None, None]
        else:
            df.loc[reps] = [random.randrange(-100, 100) / 100, random.randrange(-100, 100) / 100, None, None, None]
        print(reps)

    #Adjusts the seed settings after the first generation
    if (reps>(how_many_per_gen*repset)):
        advanced = True
        mask = df['score'] == df.score.max()
        best = df[mask]
        print("best")
        print(best)
        print("there is it")
        seed_weight_1 = float(best['w1'])
        seed_weight_2 = float(best['w2'])
        repset+=1




#Prints outputs when finished
print(df)
mask = df['score'] == df.score.max()
best = df[mask]
seed_weight_1 = float(best['w1'])
seed_weight_2 = float(best['w2'])
print(best)
print(seed_weight_1)
print(seed_weight_2)