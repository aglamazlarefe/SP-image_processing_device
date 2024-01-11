import pickle
import cv2
import pytesseract

image = cv2.imread("aligned_photo.jpg")
image = cv2.flip(image,1)
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
texts= []
for i, rectangle in enumerate(rectangles):
    x, y, w, h = cv2.boundingRect(rectangle)
    roi = image[y:y+h, x:x+w]
    roi_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    

    # Image preprocessing (e.g., contrast stretching, thresholding)
    _, thresh = cv2.threshold(roi_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU,)
    
    text = pytesseract.image_to_string(thresh, lang="tur", config='--psm 9')  # 9, 3, 4, 1 en iyisi

    
    texts.append(text)
    print(f"metin {i+1}: {texts[i]} ")

    cv2.putText(rectangles_image, str(i+1), (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    # Draw bounding box
    cv2.rectangle(rectangles_image, (x, y), (x+w, y+h), (0, 255, 0), 2)

rectangle_name= []

for i in range(min(len(rectangles), len(texts))):
    combined_element = [rectangles[i], texts[i]]
    rectangle_name.append(combined_element)


fileObj = open("lib/hand_detection/rectangles.p", "wb")
pickle.dump(rectangle_name, fileObj)
fileObj.close()


cv2.imshow("Dikdörtgenler", rectangles_image ) #cv2.resize(rectangles_image, (600, 900))
cv2.waitKey(0)
cv2.destroyAllWindows()
#241
#180-170
#175-165



