import pandas as pd
import random
import numpy as np

df = pd.DataFrame(columns=['h1','h2','h3','h4'])

#print(df)
df.loc[1] = [0,0,0,0]
#print(df)
df.iloc[0,0] = 2
df.iloc[0,1] = 3
#print(df)


#a is inputs, h is middle layers, z is outputs
a = 4
h = 3
z = 2
state = [2,1,3,2]
h_list = []
z_list = []

def seed_weights(h,rows):
    seeds = []
    for i in range(rows):
        seeds.append(random.randrange(-100,100)/100)
    return(seeds)

inter_weights = pd.DataFrame()

for i in range(h):
    seeds = seed_weights(h,a)
    inter_weights[i] = seeds
#print(inter_weights.iloc[:][0])
#print()

for i in range(h):
    h_list.append(np.dot(state,inter_weights.iloc[:][i]))
print("h_list")
print(h_list)
print()
#print()

inter_weights.columns=["h1","h2","h3"]
#print(inter_weights)
#print()

final_weights = pd.DataFrame()

for i in range(z):
    seeds = seed_weights(z,h)
    final_weights[i] = seeds

for i in range(z):
    z_list.append(np.dot(h_list,final_weights.iloc[:][i]))


print("z_list")
print(z_list)
print()
#print(final_weights.iloc[:][0])
final_weights.iloc[:,0] = [2,3,4] #changes a whole column to new values
final_weights.iloc[1,1] = 5 #changes a single value
#print(final_weights)
final_weights.columns = ["z1","z2"]
final_weights.index = ["h1", "h2", "h3"]
print("final_weights")
print(final_weights)
print()
inter_weights.columns = ["h1","h2","h3"]
inter_weights.index = ["a1", "a2", "a3","a4"]
print("inter_weights")
print(inter_weights)
print()
print(inter_weights.loc["a1"])
print(inter_weights.loc["a1"]["h1"])