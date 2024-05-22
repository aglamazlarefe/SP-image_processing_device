import cv2
import pytesseract
import numpy as np

# Image path
image_path = "captured_image.jpg"  # Replace with the path to your image file

# Initialize variables
img = cv2.imread(image_path)
width, height = 1080, 1920

# List to store OCR results
ocr_results_2d = []

def find_large_rectangles_contour(img, area_threshold=5000):
    """
    Finds rectangles with areas larger than the specified threshold in the image.

    Args:
        img: The input image
        area_threshold: The minimum area threshold for rectangles

    Returns:
        large_rectangles: List of arrays containing four corner points of large rectangles
    """
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    global thresh

    thresh = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 21, 10
    )
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    large_rectangles = []

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > area_threshold:
            epsilon = 0.02 * cv2.arcLength(contour, True)
            rectangle = cv2.approxPolyDP(contour, epsilon, True)
            large_rectangles.append(rectangle)

    return large_rectangles


def find_rectangles_within_image(img, area_threshold=5000):
    """
    Finds rectangles within the specified area threshold in the image.

    Args:
        img: The input image
        area_threshold: The minimum area threshold for rectangles

    Returns:
        rectangles: List of arrays containing four corner points of rectangles
    """
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    global thresh

    thresh = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 21, 10
    )
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    rectangles = []

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > area_threshold:
            epsilon = 0.02 * cv2.arcLength(contour, True)
            rectangle = cv2.approxPolyDP(contour, epsilon, True)
            rectangles.append(rectangle)

    return rectangles


def warp_image(img, points):
    # Explicitly convert the points to type numpy.float32
    points = points.astype(np.float32)

    # Compute the perspective transform matrix
    M = cv2.getPerspectiveTransform(
        points,
        np.array([[0, 0], [width, 0], [width, height], [0, height]], dtype=np.float32),
    )

    # Apply the perspective transform
    result = cv2.warpPerspective(img, M, (width, height))

    return result


# Find rectangles with areas larger than the specified threshold
large_rectangles = find_large_rectangles_contour(img, area_threshold=5000)

for rect in large_rectangles:
    points = rect.reshape(4, 2)
    question_box = warp_image(img, points)

    # Find rectangles within the transformed image
    rectangles_within_question_box = find_rectangles_within_image(
        question_box, area_threshold=1000
    )

    # List to store OCR results for each rectangle
    ocr_results = []

    # Display the found rectangles within the transformed image
    for rect_within_question_box in rectangles_within_question_box:
        cv2.polylines(
            question_box, [rect_within_question_box], True, (0, 255, 0), 2
        )
        for point in rect_within_question_box:
            cv2.circle(
                question_box, tuple(point[0]), 5, (255, 0, 0), -1
            )  # -1 fills the circle

        # Extract text using Tesseract OCR
        x, y, w, h = cv2.boundingRect(rect_within_question_box)
        roi = question_box[y:y + h, x:x + w]
        text = pytesseract.image_to_string(thresh, config='--psm 9') 
        
        # Append OCR result to the list
        ocr_results.append(text)

    # Append OCR results for the current rectangle to the 2D list
    ocr_results_2d.append(ocr_results)

# Display the original image with rectangles and points
cv2.imshow("Original Image", img)

# Print and display OCR results
for i, results in enumerate(ocr_results_2d):
    print(f"Rectangle {i + 1} OCR Results:")
    for j, result in enumerate(results):
        print(f"  OCR Result {j + 1}: {result}")

cv2.waitKey(0)
cv2.destroyAllWindows()
