import math
import numpy as np

def inverse_kinematics_2d(x, y, L1, L2, elevation=0):
   

    # Adjust y to remove elevation offset
    y_eff = y - elevation

    # Step 1: Compute cos(theta2)
    r2 = x**2 + y_eff**2
    C2 = (r2 - L1**2 - L2**2) / (2 * L1 * L2)

    # Step 2: Check reachability
    if abs(C2) > 1:
        print("Target is outside reachable workspace.")
        return []

    # Step 3: Two possible values of sin(theta2)
    S2_pos = math.sqrt(max(0.0, 1 - C2**2))
    S2_neg = -S2_pos

    solutions = []

    for S2 in [S2_pos, S2_neg]:
        theta2 = math.atan2(S2, C2)
        k1 = L1 + L2 * C2
        k2 = L2 * S2
        theta1 = math.atan2(y_eff, x) - math.atan2(k2, k1)

        # Normalize angles to [0, 2*pi)
        theta1 = theta1 % (2 * math.pi)
        theta2 = theta2 % (2 * math.pi)

        solutions.append((theta1, theta2))

    return solutions


# Example usage:
if __name__ == "__main__":
    L1, L2 = 362, 290
    elevation = 262.25
    x= float(input("Enter x coordinate: "))
    y= float(input("Enter y coordinate: "))
    z = float(input("Enter z coordinate: "))

    l= math.sqrt(x**2 + y**2)
    if z < elevation:
        print("Target z is below the elevation level.")
    elif l > (L1 + L2):
        print("Target is outside reachable workspace.")
        exit()
    
    sols = inverse_kinematics_2d(l, z, L1, L2, elevation)
    sol_1, sol_2 = np.degrees(sols[0]), np.degrees(sols[1])
    print("sol1: ", sol_1)
    print("sol2: ", sol_2)
    base_theta = np.degrees(np.arctan2(y, x))
    print("base theta: ", base_theta)
