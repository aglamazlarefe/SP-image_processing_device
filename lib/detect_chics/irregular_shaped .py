import cv2
import numpy as np

def detect_irregular_circles(image):
    # Convert the image to grayscale
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    

    # Apply a Gaussian blur to the grayscale image
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    thresh2 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 199, 5) 
    # Use Canny edge detection
    canny = cv2.Canny(blurred, 50, 150)

    # Find contours in the edge-detected image
    contours, _ = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Approximate each contour as a circle
    for contour in contours:
        ((x, y), radius) = cv2.minEnclosingCircle(contour)
        if radius > 0:
            # Convert the radius to an integer
            radius = int(radius)

            # Draw the circle on the original image
            cv2.circle(image, (int(x), int(y)), radius, (0, 255, 0), 4)

    # Return the original image with circles drawn on it
    return thresh2

# Read the image from file
image = cv2.imread('can_shape_2.jpg')

# Detect irregularly shaped circles in the image
detected_image = detect_irregular_circles(image)

# Display the original image with circles drawn on it
cv2.imshow('Detected Circles', detected_image)
cv2.waitKey(0)
cv2.destroyAllWindows()


