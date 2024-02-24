import cv2


# Empty function
def doNothing(x):
    pass


# Creating a resizable window named Track Bars
cv2.namedWindow('Track Bars', cv2.WINDOW_NORMAL)

# Creating trackbars for gathering threshold values of hue, saturation, and value
cv2.createTrackbar('min_hue', 'Track Bars', 0, 179, doNothing)
cv2.createTrackbar('min_saturation', 'Track Bars', 0, 255, doNothing)
cv2.createTrackbar('min_value', 'Track Bars', 0, 255, doNothing)

cv2.createTrackbar('max_hue', 'Track Bars', 0, 179, doNothing)
cv2.createTrackbar('max_saturation', 'Track Bars', 0, 255, doNothing)
cv2.createTrackbar('max_value', 'Track Bars', 0, 255, doNothing)


# Reading the image
object_image = cv2.imread("C:/Users/user/Desktop/untitled.png")

# Converting into HSV color model
hsv_image = cv2.cvtColor(object_image, cv2.COLOR_BGR2HSV)

# Showing both resized and hsv image in named windows
cv2.imshow('Base Image', cv2.resize(object_image, (800, 600)))
cv2.imshow('HSV Image', cv2.resize(hsv_image, (800, 600)))

# Creating a loop to get the feedback of the changes in trackbars
while True:
    # Reading the trackbar values for thresholds
    min_hue = cv2.getTrackbarPos('min_hue', 'Track Bars')
    min_saturation = cv2.getTrackbarPos('min_saturation', 'Track Bars')
    min_value = cv2.getTrackbarPos('min_value', 'Track Bars')

    max_hue = cv2.getTrackbarPos('max_hue', 'Track Bars')
    max_saturation = cv2.getTrackbarPos('max_saturation', 'Track Bars')
    max_value = cv2.getTrackbarPos('max_value', 'Track Bars')

    # Using inrange function to turn on the image pixels where object threshold is matched
    mask = cv2.inRange(hsv_image, (min_hue, min_saturation, min_value), (max_hue, max_saturation, max_value))

    # Showing the mask image
    cv2.imshow('Mask Image', cv2.resize(mask, (800, 600)))

    # Checking if q key is pressed to break out of loop
    key = cv2.waitKey(25)
    if key == ord('q'):
        break

# Printing the threshold values for usage in detection application
print(f'min_hue {min_hue}  min_saturation {min_saturation} min_value {min_value}')
print(f'max_hue {max_hue}  max_saturation {max_saturation} max_value {max_value}')

# Destroying all windows
cv2.destroyAllWindows()
