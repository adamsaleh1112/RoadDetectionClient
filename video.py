import numpy as np # importing numpy a library that allows large data collection and manipulation
import cv2 # importing open CV, a computer vision library

vid = cv2.VideoCapture("Road.mov") # setting the video as Road.mov
turns = [] # list for storing left right values
turns_list = [] # slicing turn list

def road_overlay_stream():

    global vid

    while (True):
        turn_list = turns[-250:]  # last 250 values of turns

        ret, img = vid.read() # reading the video

        # CROPPING IMAGE
        cropped_img = img[840:1920, 0:1080]
        cropped_for_haar = img[840:1520, 270:810]

        # MAKING YELLOW BRIGHTER
        lowyellow = np.array([50, 100, 150]) # low yellow RGB threshold
        lightyellow = np.array([120, 215, 240]) # high yellow RGB threshold
        yellow = cv2.inRange(img, lowyellow, lightyellow)

        # HIGHLIGHTING YELLOW
        highlighted = cv2.cvtColor(yellow, cv2.COLOR_GRAY2BGR)  # converting it to color so arrays are same size
        highlighted_img = cv2.add(img, highlighted)

        # PERSPECTIVE TRANSFORM
        pts1 = np.float32([[480, 1250], [620, 1250], [150, 1550], [950, 1550]])
        pts2 = np.float32([[0, 0], [475, 0], [0, 640], [475, 640]])

        # PERSPECTIVE WARP
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        result = cv2.warpPerspective(highlighted_img, matrix, (475, 640))
        result_for_adding = cv2.warpPerspective(highlighted_img, matrix, (475, 640))  # black background for adding
        gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 25, 175)

        # MAKING BLACK FRAME FOR LINE OVERLAY
        cv2.circle(result_for_adding, (200, 400), 250, (0, 0, 0), 500)

        # CRUDE LINE DETECTION
        lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi / 180, threshold=30, minLineLength=5, maxLineGap=300)

        if lines is not None: # if no lines detected

            right_lines = [] # lists for data storage 
            left_lines = []
            slopes_left = []
            slopes_right = []
            valid_lines = []
            xs_left = []
            xs_right = []

            for line in lines:
                x1, y1, x2, y2 = line[0]

                slope = (y2 - y1) / ((x2 - x1) + 1)  # +1 prevents denominator from being 0
                abs_slope = abs(slope) + 0.01  # +.01 to prevent slope from being inf
                slope_degrees = np.rad2deg(np.arctan(slope))

                if slope_degrees > 75 or slope_degrees < -75: # filtering lines that are not remotely veritcal
                    valid_lines.append(line)

            for line in valid_lines:
                x1, y1, x2, y2 = line[0]
                if x1 > 0 and x1 < 150: # filtering lines into left and right
                    left_lines.append(line)
                if x1 > 325 and x1 < 475:
                    right_lines.append(line)

            for line in right_lines: # iterating through left lines, finding x and slope and appending
                x1, y1, x2, y2 = line[0]
                cv2.line(result, (x1, y1), (x2, y2), (0, 0, 255), 5)
                slope = (y2 - y1) / ((x2 - x1) + 1)
                slopes_right.append(slope)
                xs_right.append(x2)
                cv2.circle(result, (int(x2), 500), 4, (255, 0, 255), 10)

            for line in left_lines:  # iterating through right lines, finding x and slope and appending
                x1, y1, x2, y2 = line[0]
                cv2.line(result, (x1, y1), (x2, y2), (255, 0, 0), 5)
                slope = (y2 - y1) / ((x2 - x1) + 1)
                slopes_left.append(slope)
                xs_left.append(x2)
                cv2.circle(result, (int(x2), 500), 4, (255, 0, 255), 10)

            avg_slope_left = sum(slopes_left) / (len(slopes_left) + 0.001) # getting average slope and x of left and right lines 
            avg_slope_right = sum(slopes_right) / (len(slopes_right) + 0.001)
            avg_x_left = sum(xs_left) / (len(xs_left) + .001)
            avg_x_right = sum(xs_right) / (len(xs_right) + .001)

            cv2.circle(result, (int(avg_x_left), 500), 4, (255, 255, 255), 10)
            cv2.circle(result, (int(avg_x_right), 500), 4, (255, 255, 255), 10)

            cv2.line(result_for_adding, (int(avg_x_left), 640),
                     (int(avg_x_left + (1 / (avg_slope_left + 0.01) * -640)), 0), (255, 255, 0), 20)
            cv2.line(result_for_adding, (int(avg_x_right), 640),
                     (int(avg_x_right + (1 / (avg_slope_right + 0.01) * -640)), 0), (255, 255, 0), 20)

            midline_x1 = (avg_x_left + avg_x_right) / 2
            midline_y1 = 640
            midline_x2 = ((avg_x_left + (1 / (avg_slope_left + 0.01) * -640)) + (
                        avg_x_right + (1 / (avg_slope_right + 0.01) * -640)) / 2)
            midline_y2 = 0

            cv2.line(result_for_adding, (int(midline_x1), int(midline_y1)), (int(midline_x2), int(midline_y2)),
                     (0, 0, 255), 15)

            # TURN PREDICTION
            if midline_x1 < 180 and midline_x1 > 100:
                turns.append("l")
            elif midline_x1 < 380 and midline_x1 > 300:
                turns.append("r")
            else:
                turns.append(" ")

            print(turn_list)

            with_turn = cv2.add(cropped_img, cv2.imread("straight.jpg"))

            if "l" in turn_list:
                with_turn = cv2.add(cropped_img, cv2.imread("left.jpg"))
            if "r" in turn_list:
                with_turn = cv2.add(cropped_img, cv2.imread("right.jpg"))

            # UN-PERSPECTIVE TRANSFORM
            matrix_reverse = cv2.getPerspectiveTransform(pts2, pts1)
            result_reverse = cv2.warpPerspective(result_for_adding, matrix_reverse, (1080, 1920))

            # CROPPING RESULT
            cropped_result_reverse = result_reverse[840:1920, 0:1080]

            # ADDING IMAGES
            added_overlay = cv2.add(with_turn, cropped_result_reverse) # adding turn signal image with video  
            gray_added_images = cv2.cvtColor(added_overlay, cv2.COLOR_BGR2GRAY)
            final = cv2.resize(added_overlay, (400, 400))

        else:
            added_overlay = cv2.add(cropped_img, cv2.imread("straight.jpg"))
            final = cv2.resize(added_overlay, (400, 400))

        yield ret, final
    vid.release()

def road_stream():

    global vid

    while True:

        ret, img = vid.read()

        if not ret:
            break

        cropped_img = img[840:1920, 0:1080]

        final = cv2.resize(cropped_img, (400, 400))

        yield ret, final
    vid.release()

# PROGRAMMING WORKS CITED

# Video capture and video display https://docs.opencv.org/4.x/dd/d43/tutorial_py_video_display.html
# OpenCV rectangle https://www.geeksforgeeks.org/python-opencv-cv2-rectangle-method/
# Contour area https://docs.opencv.org/4.x/dd/d49/tutorial_py_contour_features.html
# Perspective transform https://www.geeksforgeeks.org/perspective-transformation-python-opencv/
# Color masking for yellow lane highlight https://www.tutorialspoint.com/how-to-mask-an-image-in-opencv-python


