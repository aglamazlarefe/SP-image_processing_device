import cv2
from deskew import determine_skew
from skimage import transform

def detect_and_correct_skew(frame):
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Determine the skew angle
    angle = determine_skew(gray)

    # Check if the angle is successfully determined
    if angle is not None:
        # Rotate the frame to correct skew
        rotated = transform.rotate(frame, -angle, mode='edge')

        # Display the original and rotated frames
        cv2.imshow("Original Frame", frame)
        cv2.imshow("Rotated Frame", rotated)

        print("Eğri Düzeltildi")
    else:
        # Display the original frame without rotation
        cv2.imshow("Original Frame", frame)
        print("Eğri Tespit Edilemedi")

# Open the camera (you may need to change the index based on your setup)
cap = cv2.VideoCapture(0)

while True:
    # Read a frame from the camera
    ret, frame = cap.read()

    # Call the function to detect and correct skew
    detect_and_correct_skew(frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close windows
cap.release()
cv2.destroyAllWindows()
