from imageai.Detection.Custom import DetectionModelTrainer

trainer = DetectionModelTrainer()
trainer.setModelTypeAsYOLOv3()
trainer.setDataDirectory(data_directory="barbijo")
trainer.evaluateModel(model_path="barbijo/models", json_path="barbijo/json/detection_config.json", iou_threshold=0.5, object_threshold=0.3, nms_threshold=0.5)
