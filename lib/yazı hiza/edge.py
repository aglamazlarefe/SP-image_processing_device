import cv2
import numpy as np

def show_images(images, titles):
    for i in range(len(images)):
        cv2.imshow(titles[i], images[i])
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def process_image(image_path):
    image = cv2.imread(image_path)
    
    # Görüntüyü gri tonlamaya çevir
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Beyaz alanları algılamak için eşikleme işlemi uygula
    _, thresholded = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

    # Canny Edge Detection
    edges = cv2.Canny(thresholded, 50, 150, apertureSize=3)

    # Hough Line Detection
    lines = cv2.HoughLinesP(edges, rho, theta, threshold, np.array([]), minLineLength=min_line_length, maxLineGap=max_line_gap)

    # Algılanan çizgileri orijinal görüntü üzerine çiz
    result_image = image.copy()
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(result_image, (x1, y1), (x2, y2), (0, 255, 0), 2)

    return result_image, edges

rho = 1
theta = np.pi / 180
threshold = 50
min_line_length = 50
max_line_gap = 5
image_path = "foto/alignment2.jpg"
image, edges = process_image(image_path)

show_images([image, edges], ['Original Image', 'Edge Image'])
