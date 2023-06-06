import torch
import cv2
from definitions import V5_PATH

# Load YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'custom', path=V5_PATH, source='local')


# Load the names of classes
classes = model.module.names if hasattr(model, 'module') else model.names

# Initialize the video capture
cap = cv2.VideoCapture(0)

while True:
    # Read a frame from the webcam
    ret, img = cap.read()

    # Detect objects in the image
    results = model(img)

    # Get the detected object info
    boxes = results.xyxy[0]
    confs = results.xyxyn[0][:, -1]
    classes_idx = results.xyxyn[0][:, -2].int()

    # Draw the bounding boxes and class labels of the detected objects
    for i, box in enumerate(boxes):
        x1, y1, x2, y2 = box.int().tolist()
        cls_idx = classes_idx[i]
        cls_conf = confs[i].item()
        cls_name = classes[cls_idx]

        cv2.rectangle(img, (x1, y1), (x2, y2), color=(0, 255, 0), thickness=2)
        cv2.putText(img, f"{cls_name} {cls_conf:.2f}", (x1 + 5, y1 + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # Show the image
    cv2.imshow('YOLOv5 Object Detection', img)

    # Exit if 'q' is pressed
    if cv2.waitKey(1) == ord('q'):
        break

# Release the video capture and close the windows
cap.release()
cv2.destroyAllWindows()
