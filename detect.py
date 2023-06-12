import cv2
import numpy as np
from ultralytics import YOLO


class YOLOv5Detector:
    def __init__(self, weights_path):
        self.model = YOLO(weights_path)

    def detect(self):
        # Open video stream from webcam
        cap = cv2.VideoCapture(0)

        while True:
            # Read frame from webcam
            ret, frame = cap.read()

            # Make prediction on frame
            results = self.model.predict(source=frame)

            # Check if any objects were detected
            has_detections = False
            print(results)
            for result in results:
                if result.probs[0] is not None:
                    has_detections = True
                    break

            # Show output video frame with bounding boxes in a window if there are detections
            if has_detections:
                cv2.imshow('YOLOv5', results[-1].imgs[0])

            # Break if 'q' key is pressed
            if cv2.waitKey(1) == ord('q'):
                break

        # Release resources
        cap.release()
        cv2.destroyAllWindows()


class RedBoxDetector:
    MIN_AREA_THRESHOLD = 1_000  # Minimum area threshold in pixels

    def __init__(self):
        # Initialize video capture object
        self.cap = cv2.VideoCapture(0)

    def detect(self):
        while True:
            # Read frame from video stream
            ret, frame = self.cap.read()

            # Convert frame to HSV color space
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            # Define lower and upper bounds for red color
            # lower_red = np.array([0, 70, 50])
            # upper_red = np.array([10, 255, 255])
            # mask1 = cv2.inRange(hsv, lower_red, upper_red)
            #
            # lower_red = np.array([170, 70, 50])
            # upper_red = np.array([180, 255, 255])
            # mask2 = cv2.inRange(hsv, lower_red, upper_red)
            lower_red = np.array([0, 100, 100])
            upper_red = np.array([5, 255, 255])
            mask1 = cv2.inRange(hsv, lower_red, upper_red)

            lower_red = np.array([175, 100, 100])
            upper_red = np.array([180, 255, 255])
            mask2 = cv2.inRange(hsv, lower_red, upper_red)

            # Combine the masks
            mask = mask1 + mask2

            # Apply morphological opening to remove noise
            kernel = np.ones((5, 5), np.uint8)
            mask_opened = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

            # Find contours in the mask
            contours, hierarchy = cv2.findContours(mask_opened, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Draw bounding boxes around the detected objects
            for c in contours:
                area = cv2.contourArea(c)
                if area > self.MIN_AREA_THRESHOLD:
                    x, y, w, h = cv2.boundingRect(c)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    print("Object at ({}, {})-({},{})".format(x, y, x + w, y + h))

            # Show the output frame
            cv2.imshow('Red Box Detector', frame)

            # Add a close button to the window
            cv2.namedWindow('Red Box Detector')
            close_window_button_img = np.zeros((50, 150, 3), np.uint8)
            close_window_button_img.fill(255)
            cv2.putText(close_window_button_img, "Close Window", (10, 35), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
            cv2.imshow('Close Window', close_window_button_img)

            # Check if the close button is clicked
            if cv2.getWindowProperty('Close Window', cv2.WND_PROP_VISIBLE) < 1:
                cv2.destroyAllWindows()
                break

            # Quit if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break

            # Release the resources and close the window
        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    # detector = YOLOv5Detector('yolov8n.pt')
    # detector.detect()

    detector = RedBoxDetector()
    detector.detect()