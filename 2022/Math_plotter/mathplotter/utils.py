# import opencv and numpy
import cv2
import numpy as np


def plotColors():
    cv2_color = [
        (130, 3, 3),
        (0, 37, 184),
        (2, 99, 15),
        (70, 2, 99),
        (1, 140, 117),
        (138, 145, 1),
        (1, 120, 106),
    ]
    plt_color = [
        "#0025b8",
        "#820303",
        "#02630f",
        "#460263",
        "#018c75",
        "#8a9101",
        "#01786a",
    ]
    return [cv2_color, plt_color]


# trackbar callback fucntion does nothing but required for trackbar
def nothing(x):
    pass


def initializeTrackbars(initVals=[1, 150, 50, 2]):
    # create a seperate window for trackbar
    cv2.namedWindow("trackbars")
    # create trackbars
    cv2.createTrackbar("Cut noise", "trackbars", initVals[3], 20, nothing)
    cv2.createTrackbar("Text width", "trackbars", initVals[0], 10, nothing)
    cv2.createTrackbar("Box width", "trackbars", initVals[1], 300, nothing)
    cv2.createTrackbar("Box hight", "trackbars", initVals[2], 300, nothing)
    cv2.createTrackbar("OCR", "trackbars", 0, 1, nothing)


def valTrackbars():
    textWidth = cv2.getTrackbarPos("Text width", "trackbars")
    boxWidth = cv2.getTrackbarPos("Box width", "trackbars")
    boxHeight = cv2.getTrackbarPos("Box hight", "trackbars")
    cutNoise = cv2.getTrackbarPos("Cut noise", "trackbars")
    ocr = cv2.getTrackbarPos("OCR", "trackbars")

    return [textWidth, boxWidth, boxHeight, cutNoise, ocr]
