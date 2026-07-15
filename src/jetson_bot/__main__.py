import cv2 as cv
from cv2.typing import MatLike
import matplotlib.pyplot as plt
import numpy as np

def display_image(image, title='Image', cmap=None):
    plt.figure(figsize=(10, 8))
    if len(image.shape) == 3:  
        # Color image
        plt.imshow(cv.cvtColor(image, cv.COLOR_BGR2RGB))
    else:  
        # Grayscale image
        plt.imshow(image, cmap='gray')
    plt.title(title)
    plt.axis('off')
    plt.show()

def Image_Pre_Processing(image) -> MatLike:
    # Cutting the horizon
    h, _ = image.shape[:2]
    image = image[int(h * 0.2):, :]
    
    # Gaussian Blur to reduce sensor noise
    blur = cv.GaussianBlur(image, (5, 5), 0)  
    
    # Convert to grayscale
    gray = cv.cvtColor(blur, cv.COLOR_RGB2GRAY)
    
    # Sharpen the blurred image
    kernel = np.array([
        [0, -1, 0],
        [-1, 5, -1],
        [0, -1, 0]
    ])
    sharpen = cv.filter2D(gray, -1,  kernel)

    _, mask  = cv.threshold(sharpen, 150, 225, cv.THRESH_BINARY)

    return mask

def Edge_And_Line_Detection(finalImage: MatLike) -> tuple[MatLike, np.ndarray | None]:
    sigma = 0.33
    v = np.median(finalImage)
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edges = cv.Canny(finalImage, lower, upper)


    lines = cv.HoughLinesP(edges, 1, np.pi / 180, 50, minLineLength=50, maxLineGap=10)

    output = lines.copy()

    # Draw the lines on the original image
    if lines is not None:
        for line in output:
            x1, y1, x2, y2 = line
            cv.line(finalImage, (x1, y1), (x2, y2), (0, 0, 255), 2)

    cv.imwrite("solar_panel_plot.png", finalImage)

    return finalImage, lines

def Draw_Lines(lines: np.ndarray | None) -> None:
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line
            plt.plot(
                [x1, x2],      # x coordinates
                [y1, y2],      # y coordinates
                color="black",
                linewidth=1
            )
    
    plt.gca().invert_yaxis()   # OpenCV and matplotlib use opposite y directions
    plt.show()
    

def main():
    image = cv.imread("public/solar_panel_1.png")
    processed  = Image_Pre_Processing(image)
    edges, lines = Edge_And_Line_Detection(processed)

    Draw_Lines(lines)
    display_image(edges, 'Jetson Bot')
    

if __name__ == "__main__":
    main()