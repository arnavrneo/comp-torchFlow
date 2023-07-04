# Inference script for YOLOv8 ONNX model

import numpy as np
import pandas as pd
from pathlib import Path
from exif import Image
import matplotlib.pyplot as plt
import cv2
import onnxruntime
from utils import nms, xywh2xyxy, load_img
import argparse
import os
import time

class ONNXInference():
    def __init__(self, model_path, img_path, conf_thres, iou_thres, save_path='./'):
        self.model_path = model_path
        self.img_path = img_path
        self.conf_thres = 0.15 # confidence threshold for onnx model
        self.iou_thres = 0.3 # intersection-over-union threshold for onnx model
        self.save_path = './'

    def run(self):
        opt_session = onnxruntime.SessionOptions()
        opt_session.enable_mem_pattern = True # True: memory efficient
        opt_session.enable_cpu_mem_arena = True # True: memory efficient
        opt_session.graph_optimization_level = onnxruntime.GraphOptimizationLevel.ORT_ENABLE_ALL # ALL: for optimization

        EP_list = ['CUDAExecutionProvider', 'CPUExecutionProvider'] # providers list
        ort_session = onnxruntime.InferenceSession(self.model_path, providers=EP_list)

        model_inputs = ort_session.get_inputs() # List of input nodes for loaded ONNX model
        input_names = [model_inputs[i].name for i in range(len(model_inputs))] # names of the input nodes
        input_shape = model_inputs[0].shape # shape of input

        model_output = ort_session.get_outputs() # list of output nodes for loaded ONNX model
        output_names = [model_output[i].name for i in range(len(model_output))] # list of output names

        # Loading images
        image, image_height, image_width, input_height, input_width, input_tensor = load_img(self.img_path, input_shape)

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

        # preds
        boxes = boxes[indices]
        scores = scores[indices]

        return {
            "pred_ct": len(scores)
        }

        # For viz predictions
        # image_draw = image.copy()
        # for (bbox, score, label) in zip(xywh2xyxy(boxes[indices]), scores[indices], class_ids[indices]):
        #     bbox = bbox.round().astype(np.int32).tolist()
        #     cls_id = int(label)
        #     CLASSES = ["plastic"]
        #     cls = CLASSES[cls_id]
        #     color = (0,255,0)
        #     cv2.rectangle(image_draw, tuple(bbox[:2]), tuple(bbox[2:]), color, 2)
        #     cv2.putText(image_draw,
        #                 f'{cls}:{int(score*100)}', (bbox[0], bbox[1] - 2),
        #                 cv2.FONT_HERSHEY_SIMPLEX,
        #                 0.60, [225, 255, 255],
        #                 thickness=1)
        # cv2.imwrite(Path(self.save_path, "result.jpg").as_posix(), image_draw)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-m", "--model_path")
    parser.add_argument("-p", "--img_pth")
    parser.add_argument("-c", "--conf_thres", type=float)
    parser.add_argument("-i", "--iou_thres", type=float)
    args = parser.parse_args()


    ONNXInference(
        model_path=args.model_path,
        img_path=args.img_pth,
        conf_thres=args.conf_thres,
        iou_thres=args.iou_thres
    ).run()


# # Visualizing inference
# def denormalize_bbox(box, image_width, image_height):
#     x, y, w, h = box
#     denorm_x = int((x - w/2) * image_width)
#     denorm_y = int((y - h/2) * image_height)
#     denorm_w = int(w * image_width)
#     denorm_h = int(h * image_height)
#     return denorm_x, denorm_y, denorm_w, denorm_h

# def visualize_image_with_annotations(image_path, annotations):
#     image = Image.open(image_path)
#     image_width, image_height = image.size

#     fig, ax = plt.subplots(1)
#     ax.imshow(image)

#     for annotation in annotations:
#         yolo_annot = pbx.convert_bbox(annotation, from_type="albumentations", to_type="yolo", image_size=(image_width,image_height))
#         x, y, w, h = yolo_annot

#         denorm_x, denorm_y, denorm_w, denorm_h = denormalize_bbox(
#             (x, y, w, h), image_width, image_height)

#         rect = plt.Rectangle(
#             (denorm_x, denorm_y), denorm_w, denorm_h, fill=False, edgecolor='red')

#         ax.add_patch(rect)

#         class_label = f"Class: 0"
#         ax.text(denorm_x, denorm_y - 5, class_label, color='red')

#     plt.show()

# visualize_image_with_annotations(
#     "dataset/images/predict/DJI_0023.jpg",
#     boxes
# )
