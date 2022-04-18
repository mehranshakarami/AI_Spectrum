# import the necessary packages
import argparse
import cv2
import imutils

# initialize the list of reference points and boolean indicating
# whether cropping is being performed or not
refPt = []
cropping = False
sel_rect_endpoint = []
image = []
Lclick = False
Rclick = False


def add_text(img, text):
    font = cv2.FONT_HERSHEY_TRIPLEX
    font_size = 0.7
    font_color = (130, 3, 3)
    font_thickness = 1
    x, y = 15, 105

    return cv2.putText(
        img,
        text,
        (x, y),
        font,
        font_size,
        font_color,
        font_thickness,
        cv2.LINE_AA,
    )


def click_and_crop(event, x, y, flags, param):
    # grab references to the global variables
    global refPt, cropping, sel_rect_endpoint, image, Lclick, Rclick
    wind_name = param
    # image = param
    # if the left mouse button was clicked, record the starting
    # (x, y) coordinates and indicate that cropping is being
    # performed
    if event == cv2.EVENT_LBUTTONDOWN:
        refPt = [[x, y]]
        Lclick = True
        # refPt = (min(ix,x), min(iy,y), abs(ix-x), abs(iy-y)) #set bounding box by mouse move
        cropping = True
    elif event == cv2.EVENT_MOUSEMOVE and cropping:
        sel_rect_endpoint = [[x, y]]
    # check to see if the left mouse button was released
    elif event == cv2.EVENT_LBUTTONUP:
        # record the ending (x, y) coordinates and indicate that
        # the cropping operation is finished
        refPt.append([x, y])
        cropping = False
        Rclick = True
        # draw a rectangle around the region of interest
        cv2.rectangle(image, refPt[0], refPt[1], (0, 255, 0), 2)
        cv2.imshow(wind_name, image)


def image_crop(cam=0, wind_name="image", width=500):
    captured = False
    cap = cv2.VideoCapture(cam)
    global refPt, cropping, sel_rect_endpoint, image

    while True:
        _, image = cap.read()
        image = imutils.resize(image, width=width)
        text = '"c": Capture, "Esc": Quit'
        image_text = image.copy()
        image_text = add_text(image_text, text)
        cv2.imshow(wind_name, image_text)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("c"):
            captured = True
            break

        elif key == 27:
            break  # esc to quit

    clone = image.copy()
    cv2.namedWindow(wind_name)
    cv2.setMouseCallback(wind_name, click_and_crop, (wind_name))

    # keep looping until the 'q' key is pressed
    while captured:
        # display the image and wait for a keypress
        # cv2.imshow(wind_name, image)

        if not cropping and not Rclick and not Lclick:

            text = 'Draw a Box with Mouse, or "Esc": Quit'
            image_text = image.copy()
            image_text = add_text(image_text, text)
            cv2.imshow(wind_name, image_text)
            key = cv2.waitKey(1) & 0xFF

            if key == 27:
                return None  # esc to quit

        elif cropping and sel_rect_endpoint:

            rect_cpy = image.copy()
            cv2.rectangle(rect_cpy, refPt[0], sel_rect_endpoint[0], (0, 255, 0), 1)
            cv2.imshow(wind_name, rect_cpy)

        elif Rclick and Lclick:
            text = '"c": Crop, "r": Reset Box, "Esc": Quit'
            image_text = image.copy()
            image_text = add_text(image_text, text)
            cv2.imshow(wind_name, image_text)

        key = cv2.waitKey(1) & 0xFF
        # if the 'r' key is pressed, reset the cropping region
        if key == ord("r"):

            image = clone.copy()
            cv2.imshow(wind_name, image)
            refPt = []
            cropping = False
            sel_rect_endpoint = []

        # if the 'c' key is pressed, break from the loop
        elif key == ord("c"):
            break

        elif key == 27:
            return None
    # if there are two reference points, then crop the region of interest
    # crop the image

    if len(refPt) == 2:
        crop_box = [
            min(refPt[0][1], refPt[1][1]),
            max(refPt[0][1], refPt[1][1]),
            min(refPt[0][0], refPt[1][0]),
            max(refPt[0][0], refPt[1][0]),
        ]
        roi = clone[crop_box[0] : crop_box[1], crop_box[2] : crop_box[3]]

        # close all open windows
        # cv2.destroyAllWindows()
        cv2.destroyWindow(wind_name)
        return roi, crop_box


if __name__ == "__main__":
    cam = 0
    img_cropped, crop_box = image_crop(cam=cam, wind_name="background")
    cv2.imshow("background", img_cropped)
    cv2.waitKey(0)
    # cv2.imwrite("background.jpg", img_cropped)
    cap = cv2.VideoCapture(cam)
    _, frame = cap.read()
    x0, x1, y0, y1 = crop_box
    frame_cropped = frame[x0:x1, y0:y1]
    cv2.imshow("frame", frame_cropped)
    cv2.waitKey(0)
    # cv2.imwrite("frame.jpg", frame_cropped)
