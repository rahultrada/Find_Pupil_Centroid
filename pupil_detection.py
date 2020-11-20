import time
import cv2

def process_frame(frame):
    """
    Processes a video frame by converting it to greyscale, applying Gaussian blurring to denoise,
    and applying thresholding to isolate the pupil as much as possible
    :param frame: the video frame to be processed
    :return: the processed frame
    """

    # convert to greyscale for thresholding
    processed_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # gaussian blurring to reduce noise
    processed_frame = cv2.GaussianBlur(processed_frame, (11, 11), 0)

    # thresholding to isolate the pupil as much as possible
    _, processed_frame = cv2.threshold(processed_frame, 75, 255, cv2.THRESH_BINARY_INV)

    return processed_frame

def draw_pupil(processed_frame, output_frame):
    """
    Identifies the largest contour (by area) on the processed_frame, and draws its center and fitted ellipse,
    (which is the estimation of the pupil centroid and pupil outline respectively) on the output_frame
    :param processed_frame: Processed frame used to identify the largest contour by area
    :param output_frame: Frame on which to draw the estimated pupil outline and centroid,
    identified using the largest contour
    :return: None
    """
    # after thresholding, the largest contour by area should be the pupil, so we draw that.
    contours, _ = cv2.findContours(processed_frame, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)

    if len(contours) > 0:
        # retrieve the largest contour
        contour = contours[0]

        # apply the convex hull operation to smoothen the contour
        contour = cv2.convexHull(contour)

        # retrieve the center of the contour using the moments function,
        # and draw a dot to signify the centroid of the pupil
        moment = cv2.moments(contour)
        if moment['m00'] != 0:
            centroid = (int(moment['m10'] / moment['m00']), int(moment['m01'] / moment['m00']))
            cv2.circle(output_frame, centroid, 3, (0, 255, 0), -1)

        # draw an ellipse to outline the pupil
        try:
            ellipse = cv2.fitEllipse(contour)
            cv2.ellipse(output_frame, box=ellipse, color=(0, 255, 0))
        except:
            pass

def annotate_frame(output_frame):
    """
    Displays information on the output frame. Currently, it writes out the frame number and fps value.
    :param output_frame: The frame on which to write out any useful information
    :return: None
    """
    global prev_frame_time
    current_frame_time = time.time()

    #calcualte fps
    fps = 1 / (current_frame_time - prev_frame_time)

    #update prev_frame_time variable for the next frame's computation
    prev_frame_time = current_frame_time

    #annotate output image with fps and frame count
    fps_string = 'fps: {}'.format(int(fps))
    framecount_string = 'frame: {}/{}'.format(int(frame_count), int(total_frame_count))
    cv2.putText(output_frame, fps_string, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(output_frame, framecount_string, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)



if __name__ == "__main__":
    # read in video
    cap = cv2.VideoCapture('sample.mkv')

    # variables to calculate fps which will be displayed in the output frame
    prev_frame_time = time.time()
    current_frame_time = 0

    # variables to keep track of frame count which will be displayed in the output frame
    frame_count = 0
    total_frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)

    while (cap.isOpened()):
        ret, frame = cap.read()

        # if we are at the end of the video, leave the while loop
        if not ret:
            break

        # increment the frame_count variable. This will be displayed in the output frame
        frame_count += 1

        # Obtain the region of interest
        # Roughly the outer 10% of the input frame consists of a dark circular border that is constant.
        # It doesn't aid pupil detection and potentially results in false detections, so
        # we crop it out and the remaining portion of the frame will be our 'region of interest (roi)'.
        h, w, _ = frame.shape
        roi = frame[int(h / 5):int(h * 9 / 10), int(w / 5):int(w * 8.5 / 10)]

        # process the image to help distinguish the pupil
        processed_roi = process_frame(roi)

        # generate contours to identify pupil, and draw the pupil and its centre on the output frame
        draw_pupil(processed_roi, roi)

        # calculate fps between frame computations, and display it on the output frame
        annotate_frame(roi)

        # display the output frame
        cv2.imshow('Roi', roi)

        # user can press key 'p' to pause and resume the frames, or key 'q' to quit
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
        if key == ord('p'):
            cv2.waitKey(-1)

    cap.release()
    cv2.destroyAllWindows()
