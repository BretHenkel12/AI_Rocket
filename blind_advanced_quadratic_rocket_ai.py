# Imports
import pygame
import sys
import numpy as np
import random
import pandas as pd

# User Setup
v_vs_t = 0.50           # 0 to 1, higher is saying v is more important
how_many_per_gen = 25
generations = 8
SF = 10                  #Shrinking factor
max_v_allowed = 30
seeing = True

#Our New Weights Function
def newWeight(SF, repset, Seed, adv):
    if adv:
        return(Seed + random.randrange(-100, 100) / (SF * repset))
    else:
        return(random.randrange(-100,100)/(SF * repset))


# Creating the Data Frame
df = pd.DataFrame({
    'w1': [None],
    'w2': [None],
    'w3': [None],
    'w4': [None],
    'w5': [None],
    'w6': [None],
    'score': [None],
    'v': [None],
    'count': [None]
})

# Setting up Python
clock = pygame.time.Clock()
screen = pygame.display.set_mode((500, 500))
pygame.mouse.set_visible(1)
pygame.display.set_caption('Rocket AI')

# Initial State
x = 240
y = 100.1
engine_force = 0
v = 0

# Initial Settings
count = 0
df.loc[0, 'w1'] = random.randrange(-100, 100) / 100
df.loc[0, 'w2'] = random.randrange(-100, 100) / 100
df.loc[0, 'w3'] = random.randrange(-100, 100) / 100
df.loc[0, 'w4'] = random.randrange(-100, 100) / 100
df.loc[0, 'w5'] = random.randrange(-100, 100) / 100
df.loc[0, 'w6'] = random.randrange(-100, 100) / 100
advanced = False
score = 1
reps = 0
repset = 1
thrust = np.double
# The Loop
while reps < how_many_per_gen * generations:
    # Calculates the decision
    state = np.array([(400 - y) / 10, pow(((400 - y) / 10),2), v / 10, pow((v/10),2), pow(((400 - y) / 10),3),pow((v/10),3)])
    weights_df = df.iloc[reps]['w1':'w6']
    thrust = np.dot(state, weights_df)
    #print(thrust)
    thrust = 2 / (1 + np.exp(-thrust))
    engine_force = thrust

    # clock.tick(60)
    if seeing:
        screen.fill((0,0,0))

    # Waits for key presses or the escape
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
                    df.loc[reps] = [newWeight(SF, repset, seed_1, advanced),
                                    0.1 * newWeight(SF, repset, seed_2, advanced),
                                    newWeight(SF, repset, seed_3, advanced),
                                    0.1 * newWeight(SF, repset, seed_4, advanced),
                                    0.01 * newWeight(SF, repset, seed_5, advanced),
                                    0.01 * newWeight(SF, repset, seed_6, advanced),
                                    None, None, None]
                else:
                    df.loc[reps] = [random.randrange(-100, 100) / 100, random.randrange(-100, 100) / 100,
                                    random.randrange(-100, 100) / 100, random.randrange(-100, 100) / 100,
                                    random.randrange(-100, 100) / 100, random.randrange(-100, 100) / 100,
                                    None, None, None]
                # time.sleep(0.5)

                # User Input Section
            '''if event.key == pygame.K_UP:
                engine_force = 2
                print("up")
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                engine_force = 0
                print("off")
        '''

    # Determines the kinematics
    grav_force = 1
    a = grav_force - engine_force
    v += a
    y += v * 0.02

    # If using graphical interface
    # x,y = pygame.mouse.get_pos()
    if seeing:
        pygame.draw.rect(screen, (255, 0, 0), (x, int(y), 20, 20))
        pygame.draw.rect(screen, (255,255,255), (0,400,500,100))
        pygame.display.update()
    count += 1

    # Checks for impact
    if (y >= 380):
        score = 1000 - v * 25 * v_vs_t - count * (1 - v_vs_t)
        if v > max_v_allowed:
            score = v / 1000
        df.loc[reps, 'score'] = score
        df.loc[reps, 'v'] = v
        df.loc[reps, 'count'] = count
        # time.sleep(2)
        y = 100
        v = 0
        count = 0
        reps += 1
        score = v/1000
        if advanced:
            df.loc[reps] = [newWeight(SF, repset, seed_1, advanced), 0.1 * newWeight(SF, repset, seed_2, advanced),
                            newWeight(SF, repset, seed_3, advanced), 0.1 * newWeight(SF, repset, seed_4, advanced),
                            0.01 * newWeight(SF, repset, seed_5, advanced),
                            0.01 * newWeight(SF, repset, seed_6, advanced),
                            None, None, None]
        else:
            df.loc[reps] = [random.randrange(-100, 100) / 100, random.randrange(-100, 100) / 100,
                            random.randrange(-100, 100) / 100, random.randrange(-100, 100) / 100,
                            random.randrange(-100, 100) / 100, random.randrange(-100, 100) / 100,
                            None, None, None]
        print(reps)

    if (y <= 0 or count > 2000):
        # time.sleep(2)
        y = 100
        v = 0
        count = 0
        df.loc[reps, 'score'] = score
        df.loc[reps, 'v'] = v
        df.loc[reps, 'count'] = count
        reps += 1
        if advanced:
            df.loc[reps] = [newWeight(SF, repset, seed_1, advanced), 0.1 * newWeight(SF, repset, seed_2, advanced),
                            newWeight(SF, repset, seed_3, advanced), 0.1 * newWeight(SF, repset, seed_4, advanced),
                            0.01 * newWeight(SF, repset, seed_5, advanced), 0.01 * newWeight(SF, repset, seed_6, advanced),
                            None, None, None]
        else:
            df.loc[reps] = [random.randrange(-100, 100) / 100, random.randrange(-100, 100) / 100,
                            random.randrange(-100, 100) / 100, random.randrange(-100, 100) / 100,
                            random.randrange(-100, 100) / 100, random.randrange(-100, 100) / 100,
                            None, None, None]
        print(reps)

    # Adjusts the seed settings after the first generation
    if (reps > (how_many_per_gen * repset)):
        advanced = True
        mask = df['score'] == df.score.max()
        best = df[mask]
        print("best")
        print(best)
        print("there is it")
        seed_1 = float(best['w1'])
        seed_2 = float(best['w2'])
        seed_3 = float(best['w3'])
        seed_4 = float(best['w4'])
        seed_5 = float(best['w5'])
        seed_6 = float(best['w6'])
        repset += 1

# Prints outputs when finished
print(df)
mask = df['score'] == df.score.max()
best = df[mask]
seed_1 = float(best['w1'])
seed_2 = float(best['w2'])
seed_3 = float(best['w3'])
seed_4 = float(best['w4'])
seed_5 = float(best['w5'])
seed_6 = float(best['w6'])
print(best)
print(seed_1)
print(seed_2)
print(seed_3)
print(seed_4)
print(seed_5)
print(seed_6)
seeds = [seed_1,seed_2,seed_3,seed_4,seed_5,seed_6]
print(seeds)