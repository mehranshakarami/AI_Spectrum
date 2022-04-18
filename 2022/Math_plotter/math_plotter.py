from turtle import width

from matplotlib.pyplot import axis
from mathreader.api import *
from mathreader.config import Configuration
from mathreader.helpers.exceptions import *
import base64
import numpy as np
import cv2
import sys
from PIL import ImageGrab
from time import sleep
from mathplotter.readEquations import find_equations, frame_change
from mathplotter.click_and_crop import image_crop, add_text
import matplotlib.pyplot as plt
from mathplotter.latexPlotter import plot_eq
import mathplotter.utils as utils
import imutils


# import colors for plot
colors = utils.plotColors()
cv2_color = colors[0]
plt_color = colors[1]


def hmp(cam=0, width=500, new_back=True):

    # plots inits
    # plt.ion()
    fig = plt.figure(figsize=(8, 5), tight_layout=True)
    ax = fig.gca()
    plt.pause(0.0001)

    configs = Configuration()
    hme_recognizer = HME_Recognizer()

    cap = cv2.VideoCapture(cam)

    if not cap.isOpened():
        raise IOError("Cannot open webcam")

    # figs preparations
    if new_back:
        back, crop_box = image_crop(cam=cam, wind_name="background", width=width)
        cv2.imwrite("frame_background.jpg", back)
        with open("crop_box.txt", "w") as f:
            for line in crop_box:
                f.write(str(line))
                f.write("\n")

    else:
        back = cv2.imread("frame_background.jpg")
        crop_box = []
        with open("crop_box.txt", "r") as f:
            lines = f.readlines()

        for line in lines:
            crop_box.append(int(line))

    x0, x1, y0, y1 = crop_box


    frame_old = back.copy()

    # inits
    eq_old = None

    utils.initializeTrackbars()
    ocrVal = False
    # main loop
    while True:
        equations = []
        # equations_parser = []
        gotNewEquation = False
        
        if utils.valTrackbars()[-1] == 0: 
            ocrVal = False 
        
        _, frame = cap.read()
        frame = imutils.resize(frame, width=width)
        frame = frame[x0:x1, y0:y1]

        frameBW, equations_imgs, bboxes = find_equations(frame, back)

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
            else:
                cv2.imshow("pic", frameBW_BGR)
        except:
            cv2.imshow("pic", frameBW_BGR)

        if cv2.waitKey(1) & 0xFF == 27:
            break  # esc to quit

        if ( ocrVal == False and
            utils.valTrackbars()[-1] == 1
        ):  # if OCR == 1

            ocrVal = True
            
            for idx, eq in enumerate(equations_imgs):

                cv2.imwrite("eq.png", eq)
                hme_recognizer.load_image("eq.png", data_type="path")

                try:
                    
                    proc_img = frameBW_BGR.copy()
                    add_text(proc_img, "Detecting")
                    cv2.imshow("pic", proc_img)
                    print("Detecting")
                    expression, img = hme_recognizer.recognize()
                    # expression_parsed = hme_recognizer.expression_after_parser
                    print("Latex: ", expression)
                    if "=" in expression:

                        equations.append(expression)
                        # equations_parser.append(expression_parsed)
                        eq_old = frameBW.copy()
                        gotNewEquation = True
                    
                except:
                    pass

            if gotNewEquation:

                try:
                    print(equations)
                    ax, fig = plot_eq(equations, ax, fig)
                    plt.pause(0.0001)
                except Exception as e:
                    print(e)
            # if new_eq is None:

        frame_old = frame.copy()
        sleep(0.1)
        
    cap.release()
    cv2.destroyAllWindows()



if __name__ == "__main__":
    hmp(cam=1, width=None, new_back=False)

    