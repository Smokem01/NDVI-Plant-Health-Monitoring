import time
import cv2
from ndvi_processor import NDVIProcessor
from collections import deque

process = NDVIProcessor()

img = cv2.imread('test.png')
processed =process.process_image(img) 
cv2.imshow("result" ,processed)
cv2.waitKey(0)
