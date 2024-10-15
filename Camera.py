#Test change
import cv2
import numpy as np 
import pygame

class Camera:
    def __init__(self, resolution: int, range: float, position: list):
        # Private attributes
        self.resolution = resolution  # resolution in megapixels, for example
        self.range = range  # range in meters, for example
        self.position = position  # position as [x, y, z] coordinates
        
    # Public method to simulate getting an image
    def getImage(self):
        # Simulating image capture process
        print("Capturing image with resolution:", self.__resolution)
        # Returning a placeholder value representing the image
        return f"Image captured at position {self.__position} with range {self.__range}"
    
    # Public method to process the image with some filters
    def processImage(self, shape, color, position):
        # Placeholder for processing the image using the provided filters
        self.shape = shape
        self.color = color
        self.position = position
        return processed_image
    
# Example usage:
camera = Camera(1080, 500.0, [10, 20, 30])
image = camera.getImage()  # Capturing image
processed_image = camera.processImage(["filter1", "filter2"])  # Processing image with filters
