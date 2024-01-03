import cv2
import numpy as np
import pickle

# You should have the points list, you can modify this part to fit your own requirements
points = [(100, 100), (200, 100), (200, 200), (100, 200)]
names = ['Country1', 'Country2', 'Country3', 'Country4']

# Make sure the size list is defined with 2 integers
size = [1920, 1080]

# Warp the image
def warp_image(img, points, size):
    pts1 = np.float32(points)
    pts2 = np.float32([[0, 0], [size[0], 0], [0, size[1]], [size[0], size[1]]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    imgOutput = cv2.warpPerspective(img, matrix, (size[0], size[1]))
    return imgOutput, matrix


"""
def warp(img):
    # Get the points
    fileObj = open(r"C:\Users\aglam\Documents\python_projeleri\SP-image_processing_device\map.p", "rb")
    points = pickle.load(fileObj)
    fileObj.close()
    
    # Explicitly convert the points to type numpy.float32
    points = points.astype(np.float32)
    
    # Compute the perspective transform matrix
    M = cv2.getPerspectiveTransform(points, np.array([[0, 0], [width, 0], [width, height], [0, height]], dtype=np.float32))
    
    # Apply the perspective transform
    result = cv2.warpPerspective(img, M, (width, height))
    # Display the result
    cv2.imshow("Transformed Image", result)
"""




# Initialize the OpenCV video capture object
cap = cv2.VideoCapture(0)

# Save the polygons to a file
def save_polygons():
    with open('countries.pkl', 'wb') as file_obj:
        pickle.dump(polygons, file_obj)
    print(f"Saved {len(polygons)} countries")

polygons = []
for i in range(4):
    polygons.append([points[i], names[i]])

while True:
    success, img = cap.read()
    imgWarped, _ = warp_image(img, points, size)

    key = cv2.waitKey(1)

    if key == ord("s"):
        country_name = input("Enter the Country name: ")
        polygons.append([(100, 100), (200, 100), (200, 200), (100, 200), country_name])
        print("Number of countries saved: ", len(polygons))
    
    if key == ord("q"):
        save_polygons()
        break

    if key == ord("d") and len(polygons) > 0:
        polygons.pop()
    
    overlay = imgWarped.copy()
    for polygon, name in polygons:
        cv2.polylines(imgWarped, [np.array(polygon, dtype=np.int32)], isClosed=True, color=(0, 255, 0), thickness=2)
        cv2.fillPoly(overlay, [np.array(polygon, dtype=np.int32)], (0, 255, 0))

    cv2.addWeighted(overlay, 0.35, imgWarped, 0.65, 0, imgWarped)

    cv2.imshow("Warped Image", imgWarped)
    cv2.imshow("Original Image", img)

cv2.destroyAllWindows()