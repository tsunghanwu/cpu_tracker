'''
Objective: This is the script for generating test job for cpu usage tracking

'''

import numpy as np
from sklearn.ensemble import GradientBoostingRegressor

X = np.random.random(size=1000)
X = 100 * X * np.sin(X)
X = X.reshape(1000,1)

y = np.random.random(size=1000)
y = 1000 * y
y = y.reshape(1000,)


for i in range(100):
    print('='*30)
    print('This is fitting iteration {}/100'.format(i+1))
    model = GradientBoostingRegressor(n_estimators=10000, tol=1e-14, n_iter_no_change=10000)
    model.fit(X,y)
    print(model.score(X,y))
    print('='*30)

