import cv2 as cv
from cv2.typing import MatLike
import matplotlib.pyplot as plt
import numpy as np


def display_image(image, title='Image', cmap=None):
    plt.figure(figsize=(10, 8))
    if len(image.shape) == 3:
        plt.imshow(cv.cvtColor(image, cv.COLOR_BGR2RGB))
    else:
        plt.imshow(image, cmap='gray')
    plt.title(title)
    plt.axis('off')
    plt.show()


def Image_Pre_Processing(image) -> MatLike:
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    # reduces noise
    clahe = cv.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    equalized = clahe.apply(gray)

    # bilateral filter to reduce noise while keeping edges sharp
    denoised = cv.bilateralFilter(equalized, d=9, sigmaColor=75, sigmaSpace=75)

    # Otsu thresholding to find edges
    otsu_val, _ = cv.threshold(denoised, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    lower = 0.5 * otsu_val
    upper = otsu_val
    edges = cv.Canny(denoised, lower, upper, L2gradient=True)

    # morphological closing to fill gaps in edges
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
    closed = cv.morphologyEx(edges, cv.MORPH_CLOSE, kernel, iterations=1)

    return closed


def Edge_And_Line_Detection(gray_image: MatLike):
    # Hough Line Transform to detect lines in the image
    lines = cv.HoughLinesP(
        gray_image,
        rho=1,
        theta=np.pi / 180,
        threshold=100,
        minLineLength=100,
        maxLineGap=20,
    )

    # draw lines on the image
    line_img = cv.cvtColor(gray_image, cv.COLOR_GRAY2BGR)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = np.squeeze(line)
            cv.line(line_img, (x1, y1), (x2, y2), (255, 255, 255), 2)

    return line_img, lines

def run_video(video):
    video = cv.VideoCapture(video)
    if not video.isOpened():
        print("Error opening the video file")
        return

    fps = video.get(cv.CAP_PROP_FPS)
    print('Frames per second : ', fps, 'FPS')

    frame_count = video.get(cv.CAP_PROP_FRAME_COUNT)
    print('Frame count : ', frame_count)

    while video.isOpened():
        ret, frame = video.read()
        if not ret:
            break

        processed = Image_Pre_Processing(frame) # result of just applying the image pre-processing pipeline
        final, lines = Edge_And_Line_Detection(processed)   # result of applying the edge and line detection pipeline

        # cv.imshow('Edges', processed)
        cv.imshow('Lines', final)

        key = cv.waitKey(20)
        if key == ord('q'):
            break

    video.release()
    cv.destroyAllWindows()  
    

def main():
    video = 'public_videos/VID20240702142205.mp4'
    run_video(video)



if __name__ == "__main__":
    main()