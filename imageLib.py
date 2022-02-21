import cv2 as cv
import numpy as np

def detectImage(haystack_img, iamge, threshold = 0.85):
    needle_img = cv.imread(iamge)
    result = cv.matchTemplate(haystack_img, needle_img, cv.TM_CCOEFF_NORMED)
    locations = np.where(result >= threshold)
    locations = list(zip(*locations[::-1]))

    needle_w = needle_img.shape[1]
    needle_h = needle_img.shape[0]

    rectangles = []
    for loc in locations:
        rect = [int(loc[0]), int(loc[1]), needle_w, needle_h]
        rectangles.append(rect)
        rectangles.append(rect)

    rectangles, weights = cv.groupRectangles(rectangles, groupThreshold=1, eps=0.5)

    result = dict()
    if len(rectangles):
        # print(rectangles)
        for (x, y, w, h) in rectangles:
            result['top'] = x
            result['left'] = y
            result['width'] = w
            result['height'] = h
            return result
    else:
        return None

    # points = []
    # if len(rectangles):
    #     line_color = (0, 0, 255)
    #     line_type = cv.LINE_8
    #     for (x, y, w, h) in rectangles:
    #         center_x = x + int(w/2)
    #         center_y = y + int(h/2)

    #         points.append((x, y, w, h))

    #         # Determine the box position
    #         top_left = (x, y)
    #         bottom_right = (x + w, y + h)
    #         # Draw the box
    #         cv.rectangle(haystack_img, top_left, bottom_right, color=line_color, lineType=line_type, thickness=2)
            

    #     cv.imshow('Matches', haystack_img)
    #     cv.waitKey()
