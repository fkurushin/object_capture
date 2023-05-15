from imageai.Detection import ObjectDetection
import os

project_path = "/Users/fedorkurusin/Documents/HES/cv_project/"
path_model = project_path + "models/yolov3.pt"
# path_model = project_path + "models/retinanet_resnet50_fpn_coco-eeacb38b.pth"
path_input = project_path + "animation/frames/111.jpg"
path_output = project_path + "animation/output/new_" + path_input.split("/")[-1]

execution_path = os.getcwd()

detector = ObjectDetection()
detector.setModelTypeAsYOLOv3()
detector.setModelPath(path_model)
detector.loadModel()
detections = detector.detectObjectsFromImage(input_image=path_input,
                                             output_image_path=path_output,
                                             minimum_percentage_probability=30)

print(len(detections))
for eachObject in detections:
    print(eachObject["name"], " : ", eachObject["percentage_probability"], " : ", eachObject["box_points"])
    print("--------------------------------")