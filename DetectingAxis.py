import math
import cv2
import numpy as np
# import plantcv as pcv

img = cv2.imread("morphology_test.png")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 80, 120)
lines = cv2.HoughLinesP(edges, 1, math.pi/2, 2, None,10, 1);

height, width, channels = img.shape
mask = np.zeros((height, width), np.uint8)

for line in lines[0]:
    pt1 = (line[0],line[1])
    pt2 = (line[2],line[3])
    cv2.line(img, pt1, pt2, (0,0,255), 3)
cv2.imwrite("morph_with_lines.png", gray)

cv2.rectangle(mask, (line[0],line[1]), (height,width), (255, 255, 255), 5)
masked_data = cv2.bitwise_and(img, img, mask=mask)


# Makes a rectangle area that will be treated as a mask
# device, masked, binary, contours, hierarchy = pcv.rectangle_mask(img, (0,0), (75,252), device, debug="print", color="black")


# print(pt1,pt2)
# cv2.imshow("masked", masked_data)
print(line[0],line[1],width,height)
print(height,width)
cv2.imshow('heh',mask)
cv2.imshow('image',gray)
cv2.waitKey(0)