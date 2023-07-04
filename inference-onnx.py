# Inference script for YOLOv8 ONNX model

import os
import cv2
import time
import argparse
import numpy as np
import onnxruntime
import pandas as pd
from exif import Image
from pathlib import Path
from utils import nms, xywh2xyxy, load_img

class ONNXInference():
    def __init__(self, model_path, img_path, save_path='./', save_image=False):
        self.model_path = model_path
        self.img_path = img_path
        self.conf_thres = 0.15 # confidence threshold for onnx model
        self.iou_thres = 0.3 # intersection-over-union threshold for onnx model
        self.save_path = save_path
        self.save_image=save_image

    def run(self):
        opt_session = onnxruntime.SessionOptions()
        opt_session.enable_mem_pattern = True # True: memory efficient
        opt_session.enable_cpu_mem_arena = True # True: memory efficient
        opt_session.graph_optimization_level = onnxruntime.GraphOptimizationLevel.ORT_ENABLE_ALL # ALL: for optimization

        EP_list = ['CUDAExecutionProvider', 'CPUExecutionProvider'] # providers list
        ort_session = onnxruntime.InferenceSession(self.model_path, sess_options=opt_session, providers=EP_list)

        model_inputs = ort_session.get_inputs() # List of input nodes for loaded ONNX model
        input_names = [model_inputs[i].name for i in range(len(model_inputs))] # names of the input nodes
        input_shape = model_inputs[0].shape # shape of input

        model_output = ort_session.get_outputs() # list of output nodes for loaded ONNX model
        output_names = [model_output[i].name for i in range(len(model_output))] # list of output names

        GEO_TAG_URL = []
        PRED_CT = []

        for i in os.listdir(self.img_path):
            # Loading images
            image, image_height, image_width, input_height, input_width, input_tensor = load_img(self.img_path + i, input_shape)

            # Run
            start = time.time()
            outputs = ort_session.run(output_names, {input_names[0]: input_tensor})[0] # ONNX output as numpy array
            end = time.time()
            print(f"Time for prediction: {end-start}")
            predictions = np.squeeze(outputs).T
            CONF_THRESHOLD = self.conf_thres
            scores = np.max(predictions[:, 4:], axis=1)
            predictions = predictions[scores > CONF_THRESHOLD, :] # Filter out object confidence scores below threshold
            scores = scores[scores > CONF_THRESHOLD]
            class_ids = np.argmax(predictions[:, 4:], axis=1)
            boxes = predictions[:, :4] # (x,y,w,h)

            #rescale box
            input_shape = np.array([input_width, input_height, input_width, input_height])
            boxes = np.divide(boxes, input_shape, dtype=np.float32)
            boxes *= np.array([image_width, image_height, image_width, image_height])
            boxes = boxes.astype(np.int32)


            # Apply NMS to suppress weak, overlapping bounding boxes
            IOU_THRESHOLD = self.iou_thres
            indices = nms(xywh2xyxy(boxes), scores, IOU_THRESHOLD)

            if self.save_image:
                image_draw = image.copy()
                for (bbox, score, label) in zip(xywh2xyxy(boxes[indices]), scores[indices], class_ids[indices]):
                    bbox = bbox.round().astype(np.int32).tolist()
                    cls_id = int(label)
                    CLASSES = ["plastic"]
                    cls = CLASSES[cls_id]
                    color = (0,255,0)
                    cv2.rectangle(image_draw, tuple(bbox[:2]), tuple(bbox[2:]), color, 2)
                    cv2.putText(image_draw,
                                f'{cls}:{int(score*100)}', (bbox[0], bbox[1] - 2),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.60, [225, 255, 255],
                                thickness=1)
                cv2.imwrite(Path(self.save_path, f"result_{str(i)}.jpg").as_posix(), image_draw)

            # preds
            boxes = boxes[indices]
            scores = scores[indices]
            pred_ct = len(scores)

            # Getting geo-coordinates
            with open(self.img_path + i, "rb") as image_geo:
                my_image = Image(image_geo)
                dd_lat = my_image.gps_latitude[0] + (my_image.gps_latitude[1]/60) + (my_image.gps_latitude[2]/3600)
                dd_long = my_image.gps_longitude[0] + (my_image.gps_longitude[1]/60) + (my_image.gps_longitude[2]/3600)
                url = f"https://www.google.com/maps?q={dd_lat:.7f},{dd_long:.7f}"
                GEO_TAG_URL.append(url)
            PRED_CT.append(pred_ct)

        result = {"pred_ct": PRED_CT, "GEO_TAG_URL": GEO_TAG_URL}
        res_df = pd.DataFrame(result)
        res_df.to_csv(self.save_path + 'result.csv', index=False)
        print(f"Results saved successfully to at {self.save_path}!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-m", "--model_path")
    parser.add_argument("-p", "--img_pth")
    parser.add_argument("-s", "--save_path")
    parser.add_argument("-i", "--save_image", type=bool)
    args = parser.parse_args()


    ONNXInference(
        model_path=args.model_path,
        img_path=args.img_pth,
        save_path=args.save_path,
        save_image=args.save_image
    ).run()
