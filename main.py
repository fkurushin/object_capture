import cv2
import numpy as np

# load the COCO class labels and corresponding bounding box colors
labels_path = "archive/coco.names"
LABELS = open(labels_path).read().strip().split("\n")
COLORS = np.random.randint(0, 255, size=(len(LABELS), 3), dtype="uint8")

# load the pre-trained YOLOv3 object detector
weights_path = "archive/yolov3.weights"
config_path = "archive/yolov3.cfg"
net = cv2.dnn.readNetFromDarknet(config_path, weights_path)

# get the output layer names for the YOLOv3 model
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in [net.getUnconnectedOutLayers()] if len(i) > 0]

# create a VideoCapture object to read from the camera
cap = cv2.VideoCapture(0)

while True:
    # read a frame from the video stream
    ret, frame = cap.read()

    # construct an input blob for the YOLOv3 object detector
    blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416), swapRB=True, crop=False)

    # set the input blob for the YOLOv3 object detector and perform a forward pass
    net.setInput(blob)
    outputs = net.forward(output_layers)

    # initialize lists to store detected object classes, confidences, and bounding boxes
    class_ids = []
    confidences = []
    boxes = []

    # loop over each of the YOLOv3 model's outputs
    for output in outputs:
        # loop over each of the detections in the output
        for detection in output:
            # extract the class ID and confidence of the current detection
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            # filter out weak detections by ensuring the confidence is greater than the minimum confidence threshold
            if confidence > 0.3:
                # scale the bounding box coordinates back relative to the size of the image, and convert them to integers
                box = detection[0:4] * np.array([frame.shape[1],
                                                 frame.shape[0],
                                                 frame.shape[1],
                                                 frame.shape[0]])
                (x, y, w, h) = box.astype("int")

                # add the bounding box coordinates, class ID, and confidence to their respective lists
                boxes.append([x, y, w, h])
                class_ids.append(class_id)
                confidences.append(float(confidence))

    # apply non-max suppression to suppress weak, overlapping bounding boxes
    # indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.3)
    indices = cv2.dnn.NMSBoxes(boxes,
                               confidences,
                               score_threshold=0.7,
                               nms_threshold=0.4)


    # loop over the remaining bounding box indices and draw the corresponding bounding box and label
    if len(indices) > 0:
        for i in indices.flatten():
            (x, y) = (boxes[i][0], boxes[i][1])
            (w, h) = (boxes[i][2], boxes[i][3])
            color = [int(c) for c in COLORS[class_ids[i]]]
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            text = "{}: {:.4f}".format(LABELS[class_ids[i]], confidences[i])
            cv2.putText(frame, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    # display the original frame with bounding boxes and labels around the detected objects
    cv2.imshow('frame', frame)

    # press 'q' to exit the program
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# release the VideoCapture object and close all windows
cap.release()
cv2.destroyAllWindows()
