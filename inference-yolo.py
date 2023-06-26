import numpy as np
import pandas as pd
from pathlib import Path
from exif import Image
from ultralytics import YOLO
from ensemble_boxes import *
import matplotlib.pyplot as plt
import cv2
import argparse
import os

# ONNX test

class YOLOInference():
    def __init__(self, model_path, img_path, subs_file, conf_thres=0.05, iou_thres=0.3, save_path='./'):
        self.model_path = model_path
        self.img_path = img_path
        self.subs_file = subs_file
        self.conf_thres = conf_thres
        self.iou_thres = iou_thres
        self.save_path = save_path

    def run(self):
        # CSV
        IMAGES_PATH = Path(self.img_path)
        image_ids = [x for x in sorted(os.listdir(IMAGES_PATH))]
        subs = pd.read_csv(self.subs_file)
        pred_ct = []
        ct_error = []
        per_error = []
        GEO_TAG_URL = []

        # GEO TAG URL
        geo_tags = [
            "gps_longitude",
            "gps_longitude_ref",
            "gps_latitude",
            "gps_latitude_ref"
        ]

        for i in range(len(image_ids)):
            with open(Path(IMAGES_PATH, image_ids[i]), "rb") as image:
                my_image = Image(image)
                dd_lat = my_image.gps_latitude[0] + (my_image.gps_latitude[1]/60) + (my_image.gps_latitude[2]/3600)
                dd_long = my_image.gps_longitude[0] + (my_image.gps_longitude[1]/60) + (my_image.gps_longitude[2]/3600)
                url = f"https://www.google.com/maps?q={dd_lat:.7f},{dd_long:.7f}"
                GEO_TAG_URL.append(url)

        # YOLO Inference
        model = YOLO(self.model_path)
        outputs = model.predict(
            source=IMAGES_PATH,
            conf=self.conf_thres,
            iou=self.iou_thres
        )

        # if self.device == 'cpu':
        #     outputs = outputs.cpu()
        # else:
        #     outputs = outputs.cuda()

        for i, res in enumerate(outputs):
            boxes = res.boxes
            class_ids = boxes.cls
            pred_ct.append(len(class_ids)) # no of predicted classes
            ct_error.append(int(subs["ACTUAL_CT"][i]) - len(class_ids))
            per_error.append(round(abs(ct_error[i]/int(subs["ACTUAL_CT"][i])), 3))
            image = cv2.imread(self.img_path)
            plotted = res.plot(
                line_width=4,
                font_size=4
            )
            cv2.imwrite(Path(self.save_path, f"res_{i}.jpg").as_posix(), plotted)

        subs["PRED_CT"] = pred_ct
        subs["CT_Error"] = ct_error
        subs["PERCENT_Error"] = per_error
        subs["GEO_Tag_URL"] = GEO_TAG_URL
        subs.to_csv("submission.csv", index=False)




if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-m", "--model_path")
    parser.add_argument("-p", "--img_pth")
    parser.add_argument("-f", "--subs_file")
    parser.add_argument("-c", "--conf_thres", type=float)
    parser.add_argument("-i", "--iou_thres", type=float)
    parser.add_argument("-s", "--save_path")
    # parser.add_argument("-d", "--device")
    args = parser.parse_args()

    YOLOInference(
        model_path=args.model_path,
        img_path=args.img_pth,
        subs_file=args.subs_file,
        conf_thres=args.conf_thres,
        iou_thres=args.iou_thres,
        save_path=args.save_path
    ).run()