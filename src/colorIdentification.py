import numpy as np
import argparse
import cv2
import time
import json
import utils
# function to combine images


def combineImages(imgArray):
    comboimg = np.zeros((h, w, 3), np.uint8)
    for img in imgArray:
        comboimg = cv2.add(comboimg, img)
    return comboimg


def makeArray(image, colors):
    print("Array building started...")
    start = time.time()
    result = []
    rows, cols, channels = image.shape
    for i in range(rows):
        layer = []
        for j in range(cols):
            layer.append(colors.index(tuple(image[i, j])))
        result.append(layer)
    print("Array building ended!")
    end = time.time()
    print("Time taken: ", end-start)
    return np.array(result)


def print_to_file(image):
    lists = image.tolist()
    json_str = json.dumps(lists)
    outputfile = open("image.json", "w")
    print(json_str, file=outputfile)
    outputfile.close()


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

# initialising color images for each boundary in BGR
# TODO: can simplify this with a loop
red = np.zeros((h, w, 3), np.uint8)
red[:, 0:w] = utils.single_colors[0]
yellow = np.zeros((h, w, 3), np.uint8)
yellow[:, 0:w] = utils.single_colors[1]
green = np.zeros((h, w, 3), np.uint8)
green[:, 0:w] = utils.single_colors[2]
blue = np.zeros((h, w, 3), np.uint8)
blue[:, 0:w] = utils.single_colors[3]
pink = np.zeros((h, w, 3), np.uint8)
pink[:, 0:w] = utils.single_colors[4]
single_color_images = [red, yellow, green, blue, pink]

combo = []
# loop over the boundaries
i = 0
for (lower, upper) in utils.hsv_bounds:
    # create NumPy arrays from the boundaries
    lower = np.array(lower)
    upper = np.array(upper)

    # find the colors within the specified boundaries and apply the mask
    mask = cv2.inRange(hsv, lower, upper)
    output = cv2.bitwise_and(
        single_color_images[i], utils.single_colors[i], mask=mask)

    # # comment/uncomment this block to enable/disable output during process
    # # resize the image output window
    # scale = 0.7
    # width = int(w*scale)
    # height = int(h*scale)
    # cv2.namedWindow("images", cv2.WINDOW_NORMAL)
    # cv2.resizeWindow("images", 2*width, height)

    # # show the images
    # cv2.imshow("images", np.hstack([image, output]))
    # cv2.waitKey(0)
    # print("HSV Bound ", i+1, " (upper limit) = ", upper, " (click 'ENTER')")

    combo.append(output)
    i = i+1

# resize the image output window
comboimg = combineImages(combo)
result = makeArray(comboimg, utils.single_colors)
print(result)

print_to_file(result)

scale = 0.7
width = int(w*scale)
height = int(h*scale)
cv2.namedWindow("combo image", cv2.WINDOW_NORMAL)
cv2.resizeWindow("combo image", width, height)
cv2.imshow("combo image", comboimg)
cv2.waitKey(0)
cv2.destroyAllWindows()
