import cv2
import numpy as np
import pytesseract

def draw_rectangles(image, contours):
    # For each contour found, draw a rectangle around it on the original image
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

def find_nearest_rectangle(finger_position, contours):
    min_distance = float('inf')
    nearest_rectangle = None

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        center = (x + w // 2, y + h // 2)

        # Explicitly convert to float to avoid type mismatch
        distance = float(np.linalg.norm(np.array(finger_position, dtype=float) - np.array(center, dtype=float)))

        if distance < min_distance:
            min_distance = distance
            nearest_rectangle = contour

    return nearest_rectangle

def recognize_text(image, contour):
    x, y, w, h = cv2.boundingRect(contour)

    # Ensure the bounding box coordinates are within the valid range
    x = max(0, min(x, image.shape[1]))
    y = max(0, min(y, image.shape[0]))
    w = max(0, min(w, image.shape[1] - x))
    h = max(0, min(h, image.shape[0] - y))

    # Check if the bounding box is valid
    if w > 0 and h > 0:
        cropped_image = image[y:y+h, x:x+w]

        # Perform OCR on the cropped image
        text = pytesseract.image_to_string(cropped_image, config='--psm 6')

        return text
    else:
        return ""


# Load the camera
cap = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Convert the image to HSV color space
    hsv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define the 'lower_skin' and 'upper_skin' color ranges
    lower_skin = np.array([0, 48, 80], dtype=np.uint8)
    upper_skin = np.array([20, 255, 255], dtype=np.uint8)

    # Threshold the HSV image to obtain a binary image that only contains pixels within the defined color range
    mask = cv2.inRange(hsv_image, lower_skin, upper_skin)

    # Apply a series of morphological operations to remove noise and separate connected components of interest
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))

    # Find contours in the binary image
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw rectangles around the contours found
    draw_rectangles(frame, contours)

    # Detect the person's finger and get its position
    # TODO: Implement finger detection
    finger_position = (50, 50)

    # Find the nearest rectangle to the finger
    nearest_rectangle = find_nearest_rectangle(finger_position, contours)

    # Recognize the text inside the nearest rectangle
    recognized_text = recognize_text(frame, nearest_rectangle)

    # Print the recognized text
    print(recognized_text)

    # Display the output image
    cv2.imshow('Output', frame)

    # Exit the loop when the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()