import MachineLearning as ML
import numpy as np
import pygame

#What's next
#Reorder the functions so that they make sense
#Comment the heck out of them and add the docstrings so that they can be used
#Implement in the balancing game
#Implement in the car game




state = np.array([0,1,5]).astype(float)
a = 3
h1 = 3
h2 = 4
z = 2
(h1_weights,h2_weights,z_weights) = ML.getWeightedArrays(a,h1,h2,z)
#print(h1_weights)
#print(h2_weights)
#print(z_weights)
#print(z_weights.shape)

#h1_weights,h2_weights,z_weights = ML.add_names(h1_weights,h2_weights,z_weights)
#print(h1_weights)
#print(h2_weights)
#print(z_weights)
mainSurface = pygame.display.set_mode((500,500))
screen = ML.displayNetwork(a,h1,h2,z,h1_weights,h2_weights,z_weights)
mainSurface.blit(screen,(10,10))
pygame.display.update()
pygame.time.wait(10000)




output,h1_output,h2_output = ML.getDecision(state,h1_weights,h2_weights,z_weights)
print(output)

#print(h1_weights)
#print(state)
#print(h1_output)
#print(h2_weights)
#print(h2_output)
#print(z_weights)
#print(output)

#print(state)
#state = ML.normalizeState(state)
#print(state)

#print(h1_weights.loc[0])
#print(h1_weights.iloc[0])
#print(h1_weights[0])
'''counter = 0
std = 1.0
while counter < 1000:
    counter += 1
    #print(np.random.normal(loc=0.0, scale=std))
print(h1_weights)
print()
print(h2_weights)
print()
print(z_weights)
print()
h1_weights,h2_weights,z_weights = ML.returnUpdatedArrays(h1_weights,h2_weights,z_weights,sigma=std)
h1_weights,h2_weights,z_weights = ML.add_names(h1_weights,h2_weights,z_weights)
print(h1_weights)
print()
print(h2_weights)
print()
print(z_weights)
print()
'''
