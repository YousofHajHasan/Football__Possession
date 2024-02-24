import cv2


def retrieve_color_values(color):
    color = str(color)
    if not isinstance(color, str):
        raise ValueError("Input must be a string")
    if color.lower() == "red":
        return 0, 125, 64, 21, 255, 255
    elif color.lower() == "yellow":
        return 24, 149, 120, 35, 255, 255
    elif color.lower() == "black":
        return 0, 0, 0, 179, 255, 42
    elif color.lower() == "green":
        return 34, 128, 163, 49, 255, 255
    elif color.lower() == "grey":
        return 0, 0, 110, 179, 56, 201
    elif color.lower() == "white":
        return 0, 0, 220, 179, 50, 255
    elif color.lower() == "blue":
        return 50, 104, 80, 88, 255, 241
    else:
        raise ValueError(f"Unrecognized color: {color}")


def classify_class(img, colors):
    """
    :param img: cv2 Image of a specific player to be classified
    :param colors: list of lists that contains specific match colors. Example: [["red", "green"], ["yellow", "grey"], ["black"]]
    :return: The class of the passed image
    """
    colors_list = [color for sublist in colors for color in sublist]
    masks = []
    # Getting the threshold values for each color
    colors_values = []
    for color in colors_list:

        min_blue, min_green, min_red, max_blue, max_green, max_red = retrieve_color_values(color)
        # Getting the mask image using threshold values
        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  # Since we have a HSV Color masking we need to convert the img to HSV format
        mask = cv2.inRange(img_hsv, (min_blue, min_green, min_red), (max_blue, max_green, max_red))
        # Non-zero = White, So the mask with the highest number of Non-zero is the correct class.
        colors_values.append(cv2.countNonZero(mask))
        masks.append(mask)

    maximum_index = colors_values.index(max(colors_values))
    return colors_list[maximum_index].lower()


def color(color, dictionary=False):
    colorMap = {
        "red": (0, 0, 255),
        "yellow": (0, 255, 255),
        "green": (0, 255, 0),
        "black": (0, 0, 0),
        "white": (255, 255, 255),
        "grey": (150, 150, 150),
        "gray": (150, 150, 150),
        "blue": (255, 0, 0)
    }
    if dictionary:
        return colorMap.keys()
    if color.lower() not in colorMap:
        raise ValueError("Invalid color name")
    return colorMap[color.lower()]
