from math import cos, sin
from scipy.optimize import fsolve
import numpy as np


L1, L2 = 362, 290
x, y = 471, 575.75

def equations(vars):
    theta1, theta2 = vars
    eq1 = L1*cos(theta1) + L2*cos(theta1 + theta2) - x
    eq2 = L1*sin(theta1) + L2*sin(theta1 + theta2) - y
    return [eq1, eq2]

# Try two different initial guesses
sol1 = fsolve(equations, (0.5, 0.5))
sol2 = fsolve(equations, (1.5, -1.0))



sol1 = np.rad2deg(sol1)
sol2 = np.rad2deg(sol2)

print("Solution 1:", sol1)
print("Solution 2:", sol2)
