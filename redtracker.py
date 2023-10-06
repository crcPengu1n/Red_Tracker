import cv2
import numpy as np
from slopes import Slope

# Read your binary image (where red stakes are white)
img_original = cv2.imread('red.png')

img_hsv = cv2.cvtColor(img_original, cv2.COLOR_BGR2HSV)

# Setting parameter values
lower_red = np.array([0, 164, 151])
upper_red = np.array([180, 255, 255])

img_red = cv2.inRange(img_hsv, lower_red, upper_red)

# Find Canny edges
edged = cv2.Canny(img_red, 30, 200)

# Find contours in the binary image
contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Set area threshold, keep only contours larger than this threshold
area_threshold = 3  # Adjust threshold according to your needs

# Filter contours and draw them
filtered_contours = []
for contour in contours:
    area = cv2.contourArea(contour)
    if area > area_threshold:
        filtered_contours.append(contour)
        cv2.drawContours(img_original, filtered_contours, -1, (0, 255, 255), 5)

# Initialize an empty list to store center coordinates
center_coordinates = []

for contour in filtered_contours:
    # Calculate the bounding rectangle of the contour
    x, y, w, h = cv2.boundingRect(contour)

    # Calculate the center coordinates of the bounding rectangle
    center_x = x + w // 2
    center_y = y + h // 2

    # Add the center coordinates to the list
    center_coordinates.append((center_x, center_y))

# Create an empty list to store all slope objects
slopes = []

# Calculate the slope and related parameters for each pair of coordinates and store them in the slopes list
for i in range(len(center_coordinates) - 1):
    for j in range(i + 1, len(center_coordinates) - 1):
        point1 = center_coordinates[i]
        point2 = center_coordinates[j]
        x1, y1 = point1
        x2, y2 = point2
        slope_value = (y2 - y1) / (x2 - x1)
        slope_instance = Slope(slope_value, point1, point2)
        slopes.append(slope_instance)

# Filter groups of slopes that meet certain criteria
filtered_groups = []
current_group = []

for i in range(len(slopes) - 1):
    current_group.append(slopes[i])
    for j in range(i + 1, len(slopes)):
        if abs(slopes[i].slope - slopes[j].slope) < 0.1 and slopes[i].calculate_distance() > 100 and slopes[
            j].calculate_distance() > 100 and slopes[j].calculate_distance() < 700:
            current_group.append(slopes[j])

    if len(current_group) >= 6:
        filtered_groups.append(current_group.copy())
    current_group.clear()

# Calculate the average slope value for each group and store it in a new array
average_slopes = []

for group in filtered_groups:
    slopes_values = [slope.slope for slope in group]
    average_slope = sum(slopes_values) / len(slopes_values)
    average_slopes.append(average_slope)

def remove_close_numbers(numbers, tolerance=0.15):
    result = [numbers[0]]
    kept_indices = [0]  # Store indices of the kept numbers
    for i in range(1, len(numbers)):
        num = numbers[i]
        if abs(num - result[-1]) >= tolerance:
            result.append(num)
            kept_indices.append(i)  # Add index of the kept number

    return result, kept_indices

# Use the function to remove similar slopes and get the kept slopes and their indices
filtered_average_slopes, kept_indices = remove_close_numbers(average_slopes)

# Remove corresponding slope groups from filtered_groups
filtered_groups = [filtered_groups[i] for i in kept_indices]

# Print the average slope values
print(filtered_average_slopes)
print(filtered_groups)

# Iterate through filtered_groups and draw lines for the desired slopes
for group, slope in zip(filtered_groups, filtered_average_slopes):
    # Get starting coordinates (filtered_groups[i][0].point1)
    x1, y1 = group[4].point1
    x2 = int(x1 - y1 / slope)
    y2 = 0
    x3 = int(x1 + (img_original.shape[0] - y1) / slope)
    y3 = img_original.shape[0]
    # Draw lines on a blank image
    cv2.line(img_original, (x2, y2), (x3, y3), (0, 255, 0), 2)  # Green lines

# Display the marked original image
cv2.imshow('Marked Image', img_original)
cv2.waitKey(0)
cv2.destroyAllWindows()
