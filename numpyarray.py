import numpy as np
import pandas as pd


df = pd.DataFrame({
    'w1':[None],
    'w2':[None],
    'score':[None],
    'v':[None]
})
df.loc[0] = [1,2,4,5]
df.loc[1] = [14,233,24,445]
df.loc[2] = [81,273,664,55]
#print(np.max(df.score))
#print(df)
#print()
df.loc[0,'w2'] = 4
#print(df)
#print()
mask = df['score'] == df.score.max()
#print(df[mask])
#print()
#print()
best = df[mask]
#print(int(best['w1']))
weights_df = df.iloc[0]['w1':'w2']
print(weights_df)
state = np.array([1,2])
print(np.dot(state,weights_df))
