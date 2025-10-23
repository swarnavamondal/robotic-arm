import numpy as np

class FK_3dof:
    """Forward kinematics for a 3-DOF arm (lengths in mm)."""

    def __init__(self,
                 link1: float = 362.0,
                 link2: float = 290.0,
                 elevation: float = 262.25):
        self.link1 = link1
        self.link2 = link2
        self.elevation = elevation

    def compute_fk(self,
                   base_theta: float = 0.0,
                   theta1: float = 0.0,
                   theta2: float = 0.0,
                   theta3: float = 0.0):
        """
        Compute forward kinematics.

        Args:
            base_theta: base rotation around vertical axis (degrees)
            theta1: first link angle in plane (degrees)
            theta2: second link angle in plane (degrees)
            theta3: end-effector orientation in plane (degrees)

        Returns:
            tuple: (x, y, z) coordinates in mm
        """
        # convert planar joint angles to radians
        t1 = np.radians(theta1)
        t2 = np.radians(theta2)
        t3 = np.radians(theta3)

        # planar homogeneous transform (XY plane)
        T = np.array([
            [np.cos(t1 + t2 + t3), -np.sin(t1 + t2 + t3),
             self.link1 * np.cos(t1) + self.link2 * np.cos(t1 + t2)],
            [np.sin(t1 + t2 + t3),  np.cos(t1 + t2 + t3),
             self.elevation + self.link1 * np.sin(t1) + self.link2 * np.sin(t1 + t2)],
            [0.0, 0.0, 1.0]
        ])

        out = T @ np.array([[0.0], [0.0], [1.0]])
        l_xy = float(out[0, 0])   # planar distance from base axis
        z = float(out[1, 0])      # height

        # rotate planar distance by base_theta to get X,Y in world frame
        base_rad = np.radians(base_theta)
        x = l_xy * np.cos(base_rad)
        y = l_xy * np.sin(base_rad)

        return x, y, z

if __name__ == "__main__":
    # simple test: instantiate with defaults and pass angles to compute_fk
    fk = FK_3dof()
    x, y, z = fk.compute_fk(base_theta=30, theta1=45, theta2=-20)
    print(f"FK -> x={x:.2f} mm, y={y:.2f} mm, z={z:.2f} mm")