import pyautogui
import time
import random
# import pyautogui
# import random
# import numpy as np
# import time
# from scipy import interpolate
# import math

# def point_dist(x1,y1,x2,y2):
#     return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

# cp = random.randint(3, 5)  # Number of control points. Must be at least 2.
# x1, y1 = pyautogui.position()  # Starting position
# x2, y2 = [300, 300]  # Starting position

# # Distribute control points between start and destination evenly.
# x = np.linspace(x1, x2, num=cp, dtype='int')
# y = np.linspace(y1, y2, num=cp, dtype='int')

# # Randomise inner points a bit (+-RND at most).
# RND = 10
# xr = [random.randint(-RND, RND) for k in range(cp)]
# yr = [random.randint(-RND, RND) for k in range(cp)]
# xr[0] = yr[0] = xr[-1] = yr[-1] = 0
# x += xr
# y += yr

# # Approximate using Bezier spline.
# degree = 3 if cp > 3 else cp - 1  # Degree of b-spline. 3 is recommended.
#                                   # Must be less than number of control points.
# tck, u = interpolate.splprep([x, y], k=degree)
# # Move upto a certain number of points
# u = np.linspace(0, 1, num=2+int(point_dist(x1,y1,x2,y2)/50.0))
# points = interpolate.splev(u, tck)

# # Move mouse.
# duration = 0.1
# timeout = duration / len(points[0])
# point_list=zip(*(i.astype(int) for i in points))
# for point in point_list:
#     pyautogui.moveTo(*point)
#     time.sleep(timeout)

def move(destx, desty):
        x, y = pyautogui.position() # Current Position
        moves = random.randint(2,4)
        pixelsx = destx-x
        pixelsy = desty-y
        if moves >= 4:
                moves = random.randint(2,4)
        avgpixelsx = pixelsx/moves
        avgpixelsy = pixelsy/moves

        while moves > 0:
                offsetx = (avgpixelsx+random.randint(-8, random.randint(5,10)));
                offsety = (avgpixelsy+random.randint(-8, random.randint(5,10)));
                pyautogui.moveTo(x + offsetx, y + offsety, duration=0.2)
                moves = moves-1
                if moves <= 0:
                        break
                avgpixelsx = pixelsx / moves
                avgpixelsy = pixelsy / moves

        x, y = pyautogui.position() # Current Position
        if x != destx or y != desty:
                pyautogui.moveTo(destx, desty, duration=0.2)
        # print('x', x, 'y: ', y)

# move(300, 300)