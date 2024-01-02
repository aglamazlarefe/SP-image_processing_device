import cv2
import pytesseract

image = cv2.imread("aligned_photo.jpg")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

edges = cv2.Canny(gray, 50, 280)
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

rectangles = []

for contour in contours:
    perimeter = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
    
    if len(approx) == 4:
        rectangles.append(approx)

rectangles_image = image.copy()

for i, rectangle in enumerate(rectangles):
    x, y, w, h = cv2.boundingRect(rectangle)
    roi = image[y:y+h, x:x+w]
    roi_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    # Image preprocessing (e.g., contrast stretching, thresholding)
    _, thresh = cv2.threshold(roi_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU,)

    text = pytesseract.image_to_string(thresh, lang="tur", config='--psm 9') #9, 3,4, 1 en iyisi

    print(f"Dikdörtgen {i+1} - Metin: {text}")
    cv2.imshow(f"Dikdörtgen {i+1}", thresh)

    cv2.putText(rectangles_image, str(i+1), (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

cv2.imshow("Dikdörtgenler", cv2.resize(rectangles_image, (600, 900)))
cv2.waitKey(0)
cv2.destroyAllWindows()
