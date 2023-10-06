import cv2
import numpy as np


def on_change(*args):
    pass


# Load your image
img = cv2.imread('red.png')
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Create windows
cv2.namedWindow('image')

# Create trackbars for color change
cv2.createTrackbar('LowH', 'image', 0, 180, on_change)
cv2.createTrackbar('HighH', 'image', 180, 180, on_change)
cv2.createTrackbar('LowS', 'image', 0, 255, on_change)
cv2.createTrackbar('HighS', 'image', 255, 255, on_change)
cv2.createTrackbar('LowV', 'image', 0, 255, on_change)
cv2.createTrackbar('HighV', 'image', 255, 255, on_change)

while (1):
    # Get current positions of the trackbars
    low_h = cv2.getTrackbarPos('LowH', 'image')
    high_h = cv2.getTrackbarPos('HighH', 'image')
    low_s = cv2.getTrackbarPos('LowS', 'image')
    high_s = cv2.getTrackbarPos('HighS', 'image')
    low_v = cv2.getTrackbarPos('LowV', 'image')
    high_v = cv2.getTrackbarPos('HighV', 'image')

    # Set the HSV values based on the positions of the trackbars
    lower_bound = np.array([low_h, low_s, low_v])
    upper_bound = np.array([high_h, high_s, high_v])

    # Threshold the image
    mask = cv2.inRange(hsv, lower_bound, upper_bound)
    result = cv2.bitwise_and(img, img, mask=mask)

    # Show the images
    cv2.imshow('image', result)

    # Exit when 'ESC' is pressed
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()