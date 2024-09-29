import cv2
import numpy as np
from color_map import map

class NDVIProcessor:
    def __init__(self):
        pass

    def contrast(self, im):
        in_min = np.percentile(im, 2)
        in_max = np.percentile(im, 98)
        out_min = 0.0
        out_max = 255.0
        out = im - in_min
        out *= ((out_min - out_max) / (in_min - in_max))
        out += in_min
        return out

    def calc_ndvi(self, image):
        b, g, r = cv2.split(image)
        bottom = (r.astype(float) + b.astype(float))
        bottom[bottom==0] = 0.01
        ndvi = (b.astype(float) - r) / bottom
        return ndvi

    def process_image(self, image):
        contrasted = self.contrast(image)
        ndvi = self.calc_ndvi(contrasted)
        better_ndvi = self.contrast(ndvi)
        color_mapped_prep = better_ndvi.astype(np.uint8)
        color_mapped_image = cv2.applyColorMap(color_mapped_prep, map)
        return color_mapped_image

    @staticmethod
    def show(image, image_name):
        image = np.array(image, dtype=float)/float(255)
        shape = image.shape
        height = int(shape[0] / 2)
        width = int(shape[1] / 2)
        image = cv2.resize(image, (width, height))
        cv2.namedWindow(image_name)
        cv2.imshow(image_name, image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()