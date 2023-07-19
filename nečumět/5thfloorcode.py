import random
import numpy as np

max_x = 1000
max_y = int((max_x**2 - (max_x/2)**2)**0.5)
a = np.zeros((max_y, max_x), dtype = np.uint8)
vertices = (np.array([0, max_x//2]), np.array([max_y - 1]), np.array([max_y - 1, max_x - 1]))
p = random.choice(vertices)
for _ in range(max_x * max_y//2):
    p = (p + random.choice(vertices))//2
    a[tuple(p)] = 255