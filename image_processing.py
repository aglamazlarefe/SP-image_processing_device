import cv2
import numpy as np

# Kitaptan bir sayfa tarayın veya fotoğrafını çekin
image = cv2.imread("deneme3.jpg")

# Görüntüyü gri tonlamaya dönüştürün
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Kenar algılama işlemi yapın
edges = cv2.Canny(gray_image, 50, 150)

# Daireleri algılayın
circles = cv2.HoughCircles(edges, cv2.HOUGH_GRADIENT, dp=1, minDist=20, param1=50, param2=30, minRadius=0, maxRadius=0)

if circles is not None:
    circles = np.uint16(np.around(circles)) # type: ignore
    for circle in circles[0, :]: # type: ignore
        x, y, r = circle[0], circle[1], circle[2]
        cv2.circle(image, (x, y), r, (0, 255, 0), 2)  # Algılanan daireyi yeşil bir çizgi ile işaretle

# Sonucu göster
cv2.imshow("Algılama Sonucu", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
