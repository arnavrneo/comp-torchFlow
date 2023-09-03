import os
import torch
import numpy as np
import pandas as pd
from exif import Image
from ultralytics import YOLO
from pathlib import Path

class YOLOInference():
    def __init__(self,
                model_path,
                files,
                save_path,
                save_images
            ):
        self.model_path = model_path # path to yolo checkpoint
        self.files = files
        self.save_path = save_path # save directory for the submission.csv
        self.conf_thres = 0.2 # confidence threshold
        self.iou_thres = 0.7 # iou threshold
        self.save_images = save_images # predicted images will be saved in `runs` folder

    def run(self):

        res = []

        for i in self.files:

          # VARS
          IMG_ID = ''
          PRED_LAB = ''
          GEO_TAG_URL = ''
          PRED_CT = ''

          # The following code checks the availability of gpu. CUDA - Compute Unified Device Architecture
          device = torch.device(0 if torch.cuda.is_available() else 'cpu')
          print(f"Running on: {device}")

          model = YOLO(self.model_path)
          results = model.predict(
              i,
              conf=0.2,
              iou=0.7,
              imgsz=3584,
              device=device,
              save=self.save_images
          )

          for r in results:
            box = r.boxes
            PRED_CT = len(box.cls) # total number of plastics predicted
            if PRED_CT is not None:
                PRED_LAB = "Yes"
            else:
              PRED_LAB = "No"

          # Getting geo-coordinates
          with open(i, "rb") as image:
              my_image = Image(image)
              dd_lat = my_image.gps_latitude[0] + (my_image.gps_latitude[1]/60) + (my_image.gps_latitude[2]/3600)
              dd_long = my_image.gps_longitude[0] + (my_image.gps_longitude[1]/60) + (my_image.gps_longitude[2]/3600)
              url = f"https://www.google.com/maps?q={dd_lat:.7f}%2C{dd_long:.7f}"
              GEO_TAG_URL = url

          IMG_ID = str(i)

          res_dict = {
                "IMG_ID": IMG_ID,
                "PRED_LAB": PRED_LAB,
                "PRED_CT": PRED_CT,
                "GEO_TAG_URL": GEO_TAG_URL
          }

          res.append(res_dict)

        return res


        
# LEGACY CODE
# import os
# import cv2
# import base64
# import numpy as np
# import onnxruntime
# import pandas as pd
# from exif import Image
# from pathlib import Path
# from utils import load_img, nms, xywh2xyxy

# class ONNXInference():
#     def __init__(self, model_path, files, save_image, save_path='./'):
#         self.model_path = model_path
#         self.files = files
#         self.conf_thres = 0.2 # confidence threshold for onnx model
#         self.iou_thres = 0.7 # intersection-over-union threshold for onnx model
#         self.save_image = save_image
#         self.save_path = save_path

#     def run(self):
#         opt_session = onnxruntime.SessionOptions()
#         opt_session.enable_mem_pattern = True # True: memory efficient
#         opt_session.enable_cpu_mem_arena = True # True: memory efficient
#         opt_session.graph_optimization_level = onnxruntime.GraphOptimizationLevel.ORT_ENABLE_ALL # ALL: for optimization

#         EP_list = ['CUDAExecutionProvider', 'CPUExecutionProvider'] # providers list
#         ort_session = onnxruntime.InferenceSession(self.model_path, sess_options=opt_session, providers=EP_list)

#         model_inputs = ort_session.get_inputs() # List of input nodes for loaded ONNX model
#         input_names = [model_inputs[i].name for i in range(len(model_inputs))] # names of the input nodes
#         input_shape = model_inputs[0].shape # shape of input
#         print(input_shape)
#         model_output = ort_session.get_outputs() # list of output nodes for loaded ONNX model
#         output_names = [model_output[i].name for i in range(len(model_output))] # list of output names

#         res = []

#         for i in self.files:

#           # VARS
#           IMG_ID = ''
#           PRED_LAB = ''
#           GEO_TAG_URL = ''
#           PRED_CT = ''

#           # Loading images
#           image, image_height, image_width, input_height, input_width, input_tensor = load_img(
#                                                                           Path(i).as_posix(),
#                                                                           input_shape
#                                                                       )

#           # Run
#           outputs = ort_session.run(output_names, {input_names[0]: input_tensor})[0] # ONNX output as numpy array

#           predictions = np.squeeze(outputs).T
#           CONF_THRESHOLD = self.conf_thres
#           scores = np.max(predictions[:, 4:], axis=1)
#           predictions = predictions[scores > CONF_THRESHOLD, :] # Filter out object confidence scores below threshold
#           scores = scores[scores > CONF_THRESHOLD]
#           class_ids = np.argmax(predictions[:, 4:], axis=1)
#           boxes = predictions[:, :4] # (x,y,w,h)

#           #rescale box
#           input_shape = np.array([input_width, input_height, input_width, input_height])
#           boxes = np.divide(boxes, input_shape, dtype=np.float32)
#           boxes *= np.array([image_width, image_height, image_width, image_height])
#           boxes = boxes.astype(np.int32)


#           # Apply NMS to suppress weak, overlapping bounding boxes
#           IOU_THRESHOLD = self.iou_thres
#           indices = nms(xywh2xyxy(boxes), scores, IOU_THRESHOLD)

#           if self.save_image:
#             image_draw = image.copy()
#             for (bbox, score, label) in zip(xywh2xyxy(boxes[indices]), scores[indices], class_ids[indices]):
#                 bbox = bbox.round().astype(np.int32).tolist()
#                 cls_id = int(label)
#                 CLASSES = ["plastic"]
#                 cls = CLASSES[cls_id]
#                 color = (0,255,0)
#                 cv2.rectangle(image_draw, tuple(bbox[:2]), tuple(bbox[2:]), color, 2)
#                 cv2.putText(image_draw,
#                             f'{cls}:{int(score*100)}', (bbox[0], bbox[1] - 2),
#                             cv2.FONT_HERSHEY_SIMPLEX,
#                             0.60, [225, 255, 255],
#                             thickness=1)
#             cv2.imwrite(f"result_[0].jpg", image_draw)

#           # preds
#           boxes = boxes[indices]
#           scores = scores[indices]
#           pred_ct = len(scores)
#           PRED_CT = pred_ct

#           # Getting geo-coordinates
#           with open(i, "rb") as image_geo:

#             my_image = Image(image_geo)

#             dd_lat = my_image.gps_latitude[0] + (my_image.gps_latitude[1]/60) + (my_image.gps_latitude[2]/3600)
#             dd_long = my_image.gps_longitude[0] + (my_image.gps_longitude[1]/60) + (my_image.gps_longitude[2]/3600)
#             url = f"https://www.google.com/maps?q={dd_lat:.7f}%2C{dd_long:.7f}"
#             GEO_TAG_URL = url

#           if pred_ct is not None:
#             PRED_LAB = "Yes"
#           else:
#             PRED_LAB = "No"
  
#           IMG_ID = str(i)

#           res_dict = {
#                 "IMG_ID": IMG_ID,
#                 "PRED_LAB": PRED_LAB,
#                 "PRED_CT": PRED_CT,
#                 "GEO_TAG_URL": GEO_TAG_URL
#           }

#           res.append(res_dict)

#         return res
