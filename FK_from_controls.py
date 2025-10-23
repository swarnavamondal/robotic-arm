import numpy as np
import sys
import pygame
import angles as angles
from fk_class import FK_3dof

if __name__ == "__main__":
    slider_ui = angles.AngleSliders()
    fk = FK_3dof()

    while True:
        try:
            for angles in slider_ui.run():
                print(f"Angles: base={angles[0]:.1f}, link1={angles[1]:.1f}, link2={angles[2]:.1f}")
                x, y, z = fk.compute_fk(base_theta=angles[0],
                                        theta1=angles[1],
                                        theta2=angles[2])
                print(f"FK -> x={x:.2f} mm, y={y:.2f} mm, z={z:.2f} mm")
        except KeyboardInterrupt:
            pass
        finally:
            pygame.quit()
            sys.exit()