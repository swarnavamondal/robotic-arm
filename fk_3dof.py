import numpy as np
import math

# take input from user in degrees
base_theta = float(input("Enter base angle : "))  # angle of base to ground
theta1 = float(input("Enter theta1 : "))   # angle of L1 to base
theta2 = float(input("Enter theta2 : "))   # angle of L2 to L1
theta3 = 0  # angle of end vector wrt L2
L1 = 362   # length in mm
L2 = 290   # length in mm
elevation = 262.25  # height elevation in mm

# converting degrees to radians
theta1 = np.radians(theta1) 
theta2 = np.radians(theta2)
#theta3 = np.radians(theta3)

# transformation matrix 
T_array = np.array([
    [np.cos(theta1+theta2+theta3), -np.sin(theta1+theta2+theta3), L1*np.cos(theta1) + L2*np.cos(theta1+theta2)],
    [np.sin(theta1+theta2+theta3),  np.cos(theta1+theta2+theta3), elevation + L1*np.sin(theta1) + L2*np.sin(theta1+theta2)],
    [0, 0, 1]
])


# output coordinates
x_array = np.array([[0], 
                    [0],
                    [1]])
forward_kinematics = np.dot(T_array, x_array)

#calculating actual x,y,z from l_xy and base_theta
l_xy = forward_kinematics[0][0]

final_coordinates = []
x = l_xy * np.cos(np.radians(base_theta))
y = l_xy * np.sin(np.radians(base_theta))
z = forward_kinematics[1][0]
final_coordinates.append([x, y, z])
print(final_coordinates)