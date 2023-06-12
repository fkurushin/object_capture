# object_capture
course project for IOT

This implementation defines a class YOLOv5Detector that takes the path to 
the YOLOv5 weights file as a parameter in its constructor. The detect method 
opens a video stream from the webcam, passes each frame to the YOLOv5 model 
for detection, and displays the output in a window until the user presses the 
'q' key to quit.

In the main block, an instance of the class is created and its detect method 
is called to start object detection on the video stream.

By wrapping the code in a class, it becomes more modular and easier to reuse 
in other projects. You can easily modify this class to accept a different source 
of input or output (e.g. a video file instead of a webcam stream, or saving the 
output to a file instead of displaying it in real-time).