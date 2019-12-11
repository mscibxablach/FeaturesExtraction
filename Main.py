import cv2
import numpy as np
import math
from enum import Enum


class MaskPosition(Enum):
    BOTTOM = 1
    TOP = 2


class X:
    def get_shape(self, image):
        height, width = image.shape
        return height, width

    def read_image(self, filename):
        return cv2.imread(filename, cv2.IMREAD_GRAYSCALE)

    def morph_image(self, image):
        kernel = np.ones((5, 5), np.uint8)
        ret, mask = cv2.threshold(image, 107, 255, cv2.THRESH_BINARY_INV)

        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.erode(mask, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        return mask

    def get_ox_coordinates(self, image):
        morphed_image = self.morph_image(image)
        edges = cv2.Canny(morphed_image, 100, 200)
        lines = cv2.HoughLines(edges, 1, math.pi / 180, 1)

        x1 = 0
        x2 = 0
        y1 = 0
        y2 = 0
        for rho, theta in lines[0]:
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            x1 = int(x0 + 1000 * (-b))
            y1 = int(y0 + 1000 * (a))
            x2 = int(x0 - 1000 * (-b))
            y2 = int(y0 - 1000 * (a))
            # cv2.line(morphed_image, (x1, y1), (x2, y2), (0, 0, 255), 10)

        return x1, x2, y1, y2

    def mask_image(self, image, maskOrientation):
        morphed_image = self.morph_image(image)
        x1, x2, y1, y2 = self.get_ox_coordinates(morphed_image)
        height, width = self.get_shape(morphed_image)

        if maskOrientation is MaskPosition.TOP:
            mask = np.zeros((height, width), np.uint8)
            mask = cv2.rectangle(mask, (x1, y1), (width, height), (255, 255, 255), cv2.FILLED)
            return cv2.bitwise_and(morphed_image, morphed_image, mask=mask)
        else:
            mask = np.zeros((height, width), np.uint8)
            mask = cv2.rectangle(mask, (x2, y2), (0, 0), (255, 255, 255), cv2.FILLED)
            return cv2.bitwise_and(morphed_image, morphed_image, mask=mask)

x = X()
image = x.read_image('morphology_test.png')
result = x.mask_image(image, MaskPosition.BOTTOM)
cv2.imshow('result', result)
cv2.waitKey()