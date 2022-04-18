import cv2
import numpy as np
from PIL import Image
import mathplotter.utils as utils


colors = utils.plotColors()
cv2_color = colors[0]
plt_color = colors[1]


def to_bw(img):
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # img_blur = cv2.GaussianBlur(img, (21, 21), 0)
    (thresh, img_bw) = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    setThersh = utils.valTrackbars()[3]

    if thresh < setThersh:
        _, img_bw = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)
    kernel_size = utils.valTrackbars()[0]
    kernel_dilate = np.ones((kernel_size, kernel_size))
    img_dilate = cv2.dilate(img_bw, kernel_dilate, iterations=1)

    return img_dilate


def find_equations(img, back_img):

    subtracted_img = cv2.subtract(back_img, img)
    img_bw = to_bw(subtracted_img)
    img_clean = cv2.bitwise_not(img_bw)

    ker_morph_x, ker_morph_y = utils.valTrackbars()[1:3]
    if ker_morph_x == 0:
        ker_morph_x = 1
    if ker_morph_y == 0:
        ker_morph_y = 1

    kernel_morph = cv2.getStructuringElement(cv2.MORPH_RECT, (ker_morph_x, ker_morph_y))
    img_morph = cv2.morphologyEx(img_bw, cv2.MORPH_DILATE, kernel_morph)

    # ---Finding contours ---
    contours, hierarchy = cv2.findContours(
        img_morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE
    )

    equations = []
    box_coords = []

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)

        box_coords.append([x, y, w, h])
        img_cropped = img_clean[y : y + h, x : x + w]

        equations.append(img_cropped)

    return img_clean, equations, box_coords


def frame_change(new_frame, old_frame):
    delta = cv2.subtract(old_frame, new_frame)
    # check for rgb image
    if len(delta.shape) == 3:
        delta = to_bw(delta)

    return np.linalg.norm(delta) != 0


if __name__ == "__main__":
    from click_and_crop import image_crop
    from time import sleep

    utils.initializeTrackbars()

    back = cv2.imread("background1.jpg")
    frame = cv2.imread("frame1.jpg")
    while True:

        if cv2.waitKey(1) & 0xFF == 27:
            break  # esc to quit

        frameBW, equations, bboxes = find_equations(frame, back)
        frameBW_BGR = cv2.cvtColor(
            frameBW,
            cv2.COLOR_GRAY2BGR,
        )

        try:
            if bboxes:
                for idx, bbox in enumerate(bboxes):
                    x, y, w, h = bbox

                    cv2.rectangle(
                        frameBW_BGR, (x, y), (x + w, y + h), cv2_color[idx], 4
                    )

                    cv2.imshow("pic", frameBW_BGR)
        except:
            cv2.imshow("pic", frameBW_BGR)
