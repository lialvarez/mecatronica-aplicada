# -*- coding: utf-8 -*-
"""
Created on Sat Sep  5 20:34:05 2020

@author: lisan
"""


from imageai.Detection.Custom import CustomObjectDetection

images =    ["barbijo/detection_test_samples/image (1).jpg",
            "barbijo/detection_test_samples/image (2).jpg",
            "barbijo/detection_test_samples/image (3).jpg",
            "barbijo/detection_test_samples/image (4).jpg",
            "barbijo/detection_test_samples/image (5).jpg",
            "barbijo/detection_test_samples/image (6).jpg"]
i = 1
for input_path in images:
    detector = CustomObjectDetection()
    model_path = "barbijo/models/detection_model-ex-009--loss-0007.279.h5"
    json_path = "barbijo/json/detection_config.json"
    output_path = "barbijo/detection_test_samples/result-output_{}.jpg".format(i)

    detector.setModelTypeAsYOLOv3()
    detector.setModelPath(model_path)
    detector.setJsonPath(json_path)
    detector.loadModel()
    detection = detector.detectObjectsFromImage(input_image=input_path,
                                                    output_image_path=output_path)

    print('Results:')
    for eachItem in detection:
        print(eachItem["name"], " : ", eachItem["percentage_probability"])
    print(detection)
    i += 1