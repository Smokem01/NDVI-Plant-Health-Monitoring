import cv2
import numpy as np
from enum import Enum

class HealthLevel(Enum):
    LEVEL_0 = 0 
    LEVEL_1 = 1  
    LEVEL_2 = 2  
    LEVEL_3 = 3  
    LEVEL_4 = 4 
    OTHER = 5    

class NDVIAnalyzer:
    def __init__(self):
   
        self.color_ranges = {
                                HealthLevel.LEVEL_4: 
                                (
                                    np.array([14, 0, 255], dtype=np.uint8),
                                    np.array([239, 0, 255], dtype=np.uint8)
                                ),
                                HealthLevel.LEVEL_3: 
                                (
                                    np.array([0, 0, 255], dtype=np.uint8),
                                    np.array([0, 249, 255], dtype=np.uint8)
                                ),
                                HealthLevel.LEVEL_2: 
                                (
                                    np.array([0, 255, 7], dtype=np.uint8),
                                    np.array([0, 255, 255], dtype=np.uint8)
                                ),
                                HealthLevel.LEVEL_1: 
                                (
                                    np.array([0, 175, 0], dtype=np.uint8),
                                    np.array([60, 255, 30], dtype=np.uint8)
                                ),
                            }
        
        self.thresholds =   {
                                HealthLevel.LEVEL_4: 0.10,
                                HealthLevel.LEVEL_3: 0.20,
                                HealthLevel.LEVEL_2: 0.30,
                                HealthLevel.LEVEL_1: 0.25,
                            }
        self.dead_range =   (
                                np.array([255, 255, 255], dtype=np.uint8),
                                np.array([55, 55, 55], dtype=np.uint8)
                            )

    def identify_plant_area(self, image):
        shape = np.zeros(image.shape[:2], dtype=np.uint8)
        for _, (lower, upper) in self.color_ranges.items():
            lvl_pixels = cv2.inRange(image, lower, upper)
            shape = cv2.bitwise_or(shape, lvl_pixels)
        mask = np.array([[0,0,1,0,0],[0,1,1,1,0],[1,1,1,1,1],[0,1,1,1,0],[0,0,1,0,0]])
        shape = cv2.morphologyEx(shape, cv2.MORPH_CLOSE, mask)
        shape = cv2.morphologyEx(shape, cv2.MORPH_OPEN, mask)
        #TLDR: this function returns a small image containing the shape of the tree or plant the camera is observing
        #it creates an all-black img and colors all ndvi-containing pixels with white
        #it applies a CLOSE operation to cover dead pixels inside a tree and then an OPEN operation to eliminate random pixels in the img
        #there are many ways of doing this but I found this to be the most convenient
        return shape

    def calculate_color_percentages(self, image, shape):
        area = cv2.countNonZero(shape)
        if area == 0:
            return None, {}
        
        percentages = {}
        for level, (lower, upper) in self.color_ranges.items():
            lvl_mask = cv2.inRange(image, lower, upper)
            lvl_mask = cv2.bitwise_and(lvl_mask, shape)
            lvl_area = cv2.countNonZero(lvl_mask)
            percentages[level] = lvl_area / area
            
        return area, percentages

    def analyze_health(self, ndvi_image):
        shape = self.identify_plant_area(ndvi_image)
        area, percentages = self.calculate_color_percentages(ndvi_image, shape)
        
        if not percentages:
            return  {
                        "status": "NO DETECTION",
                        "plant_pixel_area": 0,
                        "health_score": 0,
                        "analysis": "No living vegetation found in the image."
                    }
        
        score = 0
        analysis = []
        img_size = ndvi_image.shape[0] * ndvi_image.shape[1]
        plant_percentage = (area / img_size) * 100
        
        for level, percentage in percentages.items():
                threshold = self.thresholds[level]
                curr = min(percentage/threshold, 1.0) * level.value
                score += curr
                analysis.append (
                                    f"{level.name}: {percentage*100:.1f}% "
                                )
        
        max_score = sum(level.value for level in self.thresholds.keys())
        final_score = (score / max_score)*100
        
        return  {
                    "status": "COMPLETE",
                    "plant_percentage": plant_percentage,
                    "health_score": final_score,
                    "color_percentages": {level.name: pct*100 for level, pct in percentages.items()},
                    "analysis": "\n".join(analysis)
                }

    def visualize_analysis(self, ndvi_image, image):
        shape = self.identify_plant_area(ndvi_image)
        contours, _ = cv2.findContours(shape, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        visualization = image.copy()
        cv2.drawContours(image, contours, -1, (0, 255, 0), 2)
        #this function is soon to be changed again (until I learn more on how to better visualize analyzed area as this almost returns the same image)
        return visualization