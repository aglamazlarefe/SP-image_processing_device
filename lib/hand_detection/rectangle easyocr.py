import cv2
import easyocr
from sympy import true

image = cv2.imread("aligned_photo.jpg")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 21, 20)

edges = cv2.Canny(thresh, 50, 280)
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

rectangles = []

def is_within_bounds(rectangle, image_shape, padding=5):
    x, y, w, h = cv2.boundingRect(rectangle)
    return y > padding and x > padding and y + h < image_shape[0] - padding and x + w < image_shape[1] - padding

for contour in contours:
    perimeter = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
    
    if len(approx) == 4 and is_within_bounds(approx, image.shape):
        rectangles.append(approx)

rectangles_image = image.copy()
texts = []

reader = easyocr.Reader(['tr'], gpu=False)  # Set gpu=True if you have a GPU

for i, rectangle in enumerate(rectangles):
    x, y, w, h = cv2.boundingRect(rectangle) 
    roi = image[y:y+h, x:x+w]
    roi_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    _, thresh = cv2.threshold(roi_gray, 2, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    result = reader.readtext(thresh, detail=0, paragraph=True,  width_ths=0.5, text_threshold=0.8)
    if result:
        text = result[0]
        texts.append(text)
        print(f"Dikdörtgen {i+1} - Metin: {text}")

        cv2.putText(rectangles_image, str(i+1), (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Draw bounding box
        cv2.rectangle(rectangles_image, (x, y), (x+w, y+h), (0, 255, 0), 2)

print(rectangles_image, texts)

cv2.imshow("Dikdörtgenler", cv2.resize(rectangles_image, (600, 900)))
cv2.waitKey(0)
cv2.destroyAllWindows()
