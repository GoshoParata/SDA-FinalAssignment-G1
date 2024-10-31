import cv2
import numpy as np

class Camera:
    def __init__(self, camera_source=1, resolution=(640, 480)):
        """Initialize the Camera class with a camera source and optional resolution."""
        self.cap = cv2.VideoCapture(camera_source, cv2.CAP_DSHOW)

        # Check if the camera opened successfully
        if not self.cap.isOpened():
            raise ValueError("Error: Could not open camera.")

        # Set resolution if provided
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, resolution[0])
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution[1])

        # Offsets for region of interest
        self.offset_x = 100  # Horizontal offset from the left edge
        self.offset_y = 50   # Vertical offset from the top edge

        # Define HSV ranges for multiple colors
        self.color_ranges = {
            "red": [np.array([0, 100, 100]), np.array([10, 255, 255]), np.array([160, 100, 100]), np.array([180, 255, 255])],
            "green": [np.array([40, 50, 50]), np.array([90, 255, 255])],
            "blue": [np.array([100, 150, 50]), np.array([140, 255, 255])],
            "yellow": [np.array([10, 100, 100]), np.array([30, 255, 255])]
        }

    def getImage(self):
        """Captures frame, applies filters, and returns processed frame, grayscale, edge, and masked images for each color."""
        ret, frame = self.cap.read()
        if not ret:
            print("Failed to grab frame")
            return None, None, None, None
        
        #cropped_frame = 
        
        # Convert BGR to HSV for color segmentation
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # Apply a bilateral filter to reduce noise but preserve edges
        frame = cv2.bilateralFilter(frame, d=9, sigmaColor=75, sigmaSpace=75)

        # Apply additional filters like edge detection and color masks
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Turn frame into grayscale
        blur_frame = cv2.GaussianBlur(gray_frame, (7, 7), 0)  # Apply Gaussian Blur
        edges = cv2.Canny(blur_frame, threshold1=50, threshold2=150)  # Canny Edge detection
        kernel = np.ones((5, 5), np.uint8)
        edges = cv2.dilate(edges, kernel, iterations=1)  # Dilate the edges
        
        # Create masks for each color
        masks = {}
        for color, hsv_range in self.color_ranges.items():
            if color == "red":
                mask1 = cv2.inRange(hsv, hsv_range[0], hsv_range[1])
                mask2 = cv2.inRange(hsv, hsv_range[2], hsv_range[3])
                mask = mask1 | mask2
            else:
                mask = cv2.inRange(hsv, hsv_range[0], hsv_range[1])
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
            masks[color] = mask
        
        return frame, gray_frame, edges, masks  # Return the processed frame, grayscale, edge, and color masks

    def processImage(self, frame, masks):
        """Processes the masked frame, detects shapes, and returns a list of detected shapes with their attributes."""
        detected_shapes = []

        # Define area thresholds to filter out small or large unwanted shapes
        min_area = 900   # Minimum area of detected shapes
        max_area = 3000  # Maximum area of detected shapes

        for color, mask in masks.items():
            # Detect contours in the masked image
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            for contour in contours:
                area = cv2.contourArea(contour)
                if area < min_area or area > max_area:
                    continue  # Skip contours outside the defined area range

                # Approximate the shape of the contour
                approx = cv2.approxPolyDP(contour, 0.035 * cv2.arcLength(contour, True), True)
                num_vertices = len(approx)
                shape = "unidentified"

                # Determine the shape based on the number of vertices
                if num_vertices == 3:
                    shape = "triangle"
                elif num_vertices == 4 or num_vertices == 5:
                    shape = "square"
                elif num_vertices > 5:
                    shape = "circle"

                # Calculate the centroid of the shape
                M = cv2.moments(contour)
                if M["m00"] > 0:
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])

                    # Define the ROI with offset
                    h, w = frame.shape[:2]
                    roi_x_min = w * 0.1 + self.offset_x
                    roi_x_max = w * 0.9 + self.offset_x
                    roi_y_min = h * 0.1 + self.offset_y
                    roi_y_max = h * 0.8 + self.offset_y

                    # Skip shapes outside the ROI
                    if not (roi_x_min < cX < roi_x_max and roi_y_min < cY < roi_y_max):
                        continue
                    
                    # Draw the contour and centroid on the original image
                    cv2.drawContours(frame, [approx], -1, (0, 255, 0), 2)
                    cv2.circle(frame, (cX, cY), 7, (255, 0, 0), -1)

                    # Append detected information to the list
                    detected_shapes.append((shape, color, (cX, cY)))

                    # Display the detected shape and its attributes on the image
                    cv2.putText(frame, f"Centroid: ({cX}, {cY})", 
                                (cX - 50, cY - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                    cv2.putText(frame, f"Shape: {shape}", 
                                (cX - 50, cY - 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                    cv2.putText(frame, f"Color: {color}", 
                                (cX - 50, cY - 70), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        return detected_shapes, frame

    def release(self):
        """Releases the camera resource."""
        self.cap.release()