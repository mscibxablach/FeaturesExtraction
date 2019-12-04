import cv2
import numpy as np
import math


class X:
    filename = ""
    image = None
    masked_data_top = None
    masked_data_bottom = None
    height = None
    width = None
    mask_top = None
    mask_bottom = None

    def __init__(self,filename):
        self.filename = filename
        self.read_image()

    def get_shape(self):
        width, height = self.image.shape
        self.width = width
        self.height = height

    def read_image(self):
        self.image = cv2.imread(self.filename, cv2.IMREAD_GRAYSCALE)

    def morth_image(self):
        kernel = np.ones((5, 5), np.uint8)
        ret, mask = cv2.threshold(self.image, 107, 255, cv2.THRESH_BINARY_INV)

        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.erode(mask, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        self.image = mask

    def recognize_x_line(self):

        edges = cv2.Canny(self.image, 80, 120)
        lines = cv2.HoughLinesP(edges, 1, math.pi / 2, 2, None, 50, 1);

        for line in lines[0]:
            pt1 = (line[0], line[1])
            pt2 = (line[2], line[3])
            cv2.line(self.image, pt1, pt2, (255, 0, 10), 3)
        cv2.imwrite("morph_with_lines.png", self.image)

        return self.image

    def get_ox(self):

        edges = cv2.Canny(self.image, 80, 120)
        lines = cv2.HoughLines(edges, 1, np.pi / 180, 100)
        x1 = 0
        x2 = 0
        y1 = 0
        y2 = 0
        for rho, theta in lines[0]:
            a = np.cos(theta)
            print('a', a)
            b = np.sin(theta)
            print('b', b)
            x0 = a * rho
            y0 = b * rho
            print('x0', x0)
            print('y0', y0)
            x1 = int(x0 + 1000 * (-b))
            y1 = int(y0 + 1000 * (a))
            x2 = int(x0 - 1000 * (-b))
            y2 = int(y0 - 1000 * (a))

        return x1, x2, y1, y2

    def mask(self):
        x1, x2, y1, y2 = self.get_ox()
        mask, mask2 = np.zeros((self.height, self.width), np.uint8)
        mask2 = np.zeros((self.height, self.width), np.uint8)
        mask = cv2.rectangle(mask, (x1, y1), (self.width, self.height), (255, 255, 255), cv2.FILLED)
        masked_data_top = cv2.bitwise_and(self.image, self.image, mask=mask)
        mask2 = cv2.rectangle(mask2, (x2, y2), (0, 0), (255, 255, 255), cv2.FILLED)
        masked_data_bottom = cv2.bitwise_and(self.image, self.image, mask=mask2)



x = X('morphology_test.png')
x.read_image()
x.morth_image()




cv2.imshow('mask',mask2)
cv2.imshow('okno', masked_data_top)
cv2.imshow('okno2', masked_data_bottom)

cv2.waitKey()