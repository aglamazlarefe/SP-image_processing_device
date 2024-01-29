import cv2
import numpy as np

def preprocess_image(image_path):
    # Read the image
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Apply Gaussian blur to reduce noise and improve line detection
    blurred = cv2.GaussianBlur(image, (5, 5), 0)

    # Use adaptive thresholding to create a binary image
    _, binary = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    return binary

def detect_lines(binary_image):
    # Use morphological operations to enhance text regions
    kernel = np.ones((5, 5), np.uint8)
    dilated = cv2.dilate(binary_image, kernel, iterations=2)

    # Find contours in the image
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter contours based on area to get potential text regions
    min_contour_area = 1000
    text_contours = [contour for contour in contours if cv2.contourArea(contour) > min_contour_area]

    return text_contours

def draw_lines(image, contours):
    # Draw the contours on a copy of the original image
    result = image.copy()
    cv2.drawContours(result, contours, -1, (0, 255, 0), 2)

    # Display the result
    cv2.imshow("Handwriting Lines", result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Replace 'your_image_path.jpg' with the path to your image
    image_path = 'your_image_path.jpg'

    binary_image = preprocess_image(image_path)
    text_contours = detect_lines(binary_image)
    draw_lines(cv2.imread(image_path), text_contours)
