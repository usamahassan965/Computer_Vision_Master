import math
import cv2
import cvzone
from cvzone.ColorModule import ColorFinder
import numpy as np

# Initialize the Video
cap = cv2.VideoCapture('Videos/vid (4).mp4')

# Create the color Finder object
myColorFinder = ColorFinder(False)
hsvVals = {'hmin': 8, 'smin': 96, 'vmin': 115, 'hmax': 14, 'smax': 255, 'vmax': 255}

# Variables
posListX, posListY = [], []
xList = [item for item in range(0, 1300)]
prediction = False

# Get video properties
# frame_width = int(cap.get(3))  # Width
# frame_height = int(cap.get(4))  # Height
# fps = int(cap.get(cv2.CAP_PROP_FPS)/2.5)  # Frames per second

# # Define the codec and create VideoWriter object
# out = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc(*'XVID'), fps, (frame_width, frame_height))


while True:
    # Grab the image

    success, img = cap.read()
    # img = cv2.imread("Ball.png")
    img = img[0:900, :]

    # Find the Color Ball
    imgColor, mask = myColorFinder.update(img, hsvVals)
    # Find location of the Ball
    imgContours, contours = cvzone.findContours(img, mask, minArea=500)

    if contours:
        posListX.append(contours[0]['center'][0])
        posListY.append(contours[0]['center'][1])

    if posListX:
        # Polynomial Regression y = Ax^2 + Bx + C
        # Find the Coefficients
        A, B, C = np.polyfit(posListX, posListY, 2)

        for i, (posX, posY) in enumerate(zip(posListX, posListY)):
            pos = (posX, posY)
            cv2.circle(imgContours, pos, 10, (0, 255, 0), cv2.FILLED)
            if i == 0:
                cv2.line(imgContours, pos, pos, (0, 255, 0), 5)
            else:
                cv2.line(imgContours, pos, (posListX[i - 1], posListY[i - 1]), (0, 255, 0), 5)

        for x in xList:
            y = int(A * x ** 2 + B * x + C)
            cv2.circle(imgContours, (x, y), 2, (255, 0, 255), cv2.FILLED)

        if len(posListX) < 10:
            # Prediction
            # X values 330 to 430  Y 590
            a = A
            b = B
            c = C - 590

            x = int((-b - math.sqrt(b ** 2 - (4 * a * c))) / (2 * a))
            prediction = 330 < x < 430

        if prediction:
            cvzone.putTextRect(imgContours, "Basket", (50, 150),
                               scale=5, thickness=5, colorR=(0, 200, 0), offset=20)
        else:
            cvzone.putTextRect(imgContours, "No Basket", (50, 150),
                               scale=5, thickness=5, colorR=(0, 0, 200), offset=20)

    # Display
    imgContours = cv2.resize(imgContours, (0, 0), None, 0.7, 0.7)
    # imgContours = cv2.resize(imgContours, (frame_width, frame_height))  # Resize to match output video size

    # cv2.imshow("Image", img)
    cv2.imshow("ImageColor", imgContours)
    # Write the frame to the video
    # out.write(imgContours)
    if cv2.waitKey(100) & 0xFF == ord('q'):
        break  # Exit loop if 'q' is pressed

# Release resources
cap.release()
# out.release()
cv2.destroyAllWindows()

