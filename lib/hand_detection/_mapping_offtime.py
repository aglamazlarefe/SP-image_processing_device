from email.mime import image
import pickle
import cv2
import numpy as np

# Image path
#image_path = "captured_image.jpg"  # Replace with the path to your image file
image_path = "foto/foto_qr_2.jpg"


# Initialize variables
img = cv2.imread(image_path)
width, height = 1080, 1920
# img.shape[1], img.shape[0]  # Get image resolution

counter = 0  # Counter to track the number of clicked pointska


def find_largest_rectangle_contour(img):
    """
    Finds the largest rectangle contour in the image.

    Args:
        img: The input image

    Returns:
        largest_rect: Array containing four corner points of the largest rectangle
    """
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    global thresh

    thresh = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 21, 10
    )
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    largest_rect = None
    max_area = 0

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > max_area:
            epsilon = 0.02 * cv2.arcLength(contour, True)
            largest_rect = cv2.approxPolyDP(contour, epsilon, True)
            max_area = area

    return largest_rect


def warp_image(img):
    # Get the points
    fileObj = open("lib/hand_detection/map.p", "rb")
    points = pickle.load(fileObj)
    fileObj.close()

    # Explicitly convert the points to type numpy.float32
    points = points.astype(np.float32)

    # Compute the perspective transform matrix
    M = cv2.getPerspectiveTransform(
        points,
        np.array([[0, 0], [width, 0], [width, height], [0, height]], dtype=np.float32),
    )

    # Apply the perspective transform
    result = cv2.warpPerspective(img, M, (width, height))

    # Rotate the result to the right
    # result = cv2.rotate(result, cv2.ROTATE_90_CLOCKWISE)
    # mirrored_result = cv2.flip(result, 1)

    # Display the result

    
    return result


# Wait for a key press to close the window

# Find the largest rectangle contour in the image
largest_rect = find_largest_rectangle_contour(img)

if largest_rect is not None and len(largest_rect) == 4:
    # Display the largest rectangle
    cv2.polylines(img, [largest_rect], True, (0, 255, 0), 2)

    # Draw circles at the corner points
    for point in largest_rect:
        cv2.circle(img, tuple(point[0]), 5, (255, 0, 0), -1)  # -1 fills the circle

    # Save selected points to file
    
    points = largest_rect.reshape(4, 2)
    fileObj = open("lib/hand_detection/map.p", "wb")
    pickle.dump(points, fileObj)
    fileObj.close()
    print("Points saved to file: map.p")

mirrored_result = warp_image(img)
cv2.imshow("sonuç", cv2.resize(mirrored_result, (800,900)))
cv2.imwrite("duzunli_foto.jpg", mirrored_result)
cv2.waitKey(0)
# Wait for a key press to close the window
cv2.destroyAllWindows()




