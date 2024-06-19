import math
import numpy as np

# p_conf = [base , hombro, codo, muñeca1, muñeca2, muñeca3]
CONFS =    {'POS0' : [-1.62, -167.51, 54.63, -158.23, 90.24, 271.58],
            'POS1' : [144.46, -44.98, 44.25, -91.57, -89.00, 321.31],
            'POS2' : [156.15, -52.93, 58.20, -97.67, -89.45, 322.99],
            'POS3' : [146.85, -84.83, 103.36, -110.85, -89.08, 323.67],
            'POS4' : [132.77, -76.58, 93.41, -108.94, -88.56, 309.61],
            'POS5': [144.34, -44.44, 27.69, -75.81, -89.04, 321.14],
            'POS6': [147.41, -87.71, 92.78, -97.64, -89.16, 324.18]
                    }

CONFIGURACIONS = {}

def convert(x):
    return (x+math.pi)/(2*math.pi)

for p,lst in CONFS.items():
    rads = np.deg2rad(np.array(lst))
    CONFIGURACIONS[p] = [convert(x) for x in rads]

print(CONFIGURACIONS) 

