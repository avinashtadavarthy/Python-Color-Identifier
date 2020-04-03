import numpy as np
import argparse
import cv2

# function to combine images
def combineImages(imgArray):
    comboimg = np.zeros((h, w, 3), np.uint8)
    for img in imgArray:
        comboimg = cv2.add(comboimg, img)
    return comboimg


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help="path to the image")
args = vars(ap.parse_args())

# load the image
image = cv2.imread(args["image"])

# convert the image to hsv
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# save image dimensions
w = image.shape[1]
h = image.shape[0]

# define HSV boundaries (add more over here)
hsv_bounds = [
    ([0, 0, 0], [10, 255, 255]),  # red
    ([11, 0, 0], [35, 255, 255]),  # yellow
    ([36, 0, 0], [70, 255, 255]),  # green
    ([71, 0, 0], [140, 255, 255]),  # blue
    ([141, 0, 0], [179, 255, 255]),  # pink
]

# initialising color images for each boundary in BGR
# TODO: can simplify this with a loop
red = np.zeros((h, w, 3), np.uint8)
red[:, 0:w] = (0, 0, 255)
yellow = np.zeros((h, w, 3), np.uint8)
yellow[:, 0:w] = (0, 221, 255)
green = np.zeros((h, w, 3), np.uint8)
green[:, 0:w] = (0, 194, 0)
blue = np.zeros((h, w, 3), np.uint8)
blue[:, 0:w] = (255, 0, 0)
pink = np.zeros((h, w, 3), np.uint8)
pink[:, 0:w] = (255, 130, 220)
single_colors = [red, yellow, green, blue, pink]


combo = []
# loop over the boundaries
i = 0
for (lower, upper) in hsv_bounds:
    # create NumPy arrays from the boundaries
    lower = np.array(lower)
    upper = np.array(upper)
    print("HSV Bound ", i+1, " (upper limit) = ", upper, " (click 'ENTER')")

    # find the colors within the specified boundaries and apply the mask
    mask = cv2.inRange(hsv, lower, upper)
    output = cv2.bitwise_and(single_colors[i], single_colors[i], mask=mask)

    # resize the image output window
    scale = 0.7
    width = int(w*scale)
    height = int(h*scale)
    cv2.namedWindow("images", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("images", 2*width, height)

    # show the images
    cv2.imshow("images", np.hstack([image, output]))
    combo.append(output)
    cv2.waitKey(0)
    i = i+1

# resize the image output window
comboimg = combineImages(combo)
scale = 0.7
width = int(w*scale)
height = int(h*scale)
cv2.namedWindow("combo image", cv2.WINDOW_NORMAL)
cv2.resizeWindow("combo image", width, height)

cv2.imshow("combo image", comboimg)
cv2.waitKey(0)
cv2.destroyAllWindows()
