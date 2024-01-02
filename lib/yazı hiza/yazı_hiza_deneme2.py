import cv2
import numpy as np

image = cv2.imread('foto/231211-204603.jpg')

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
_, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    arc = cv2.arcLength(contour, True)
    orientation = np.degrees(np.arctan(h / w))
    print(f"Orientation: {orientation}")


for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
    cv2.drawContours(image, [contour], -1, (0, 0, 255), 1)

cv2.imshow("Result", image)
cv2.waitKey(0)
cv2.destroyAllWindows()