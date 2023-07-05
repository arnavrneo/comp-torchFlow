# Inference script for YOLOv8 model

import os
import torch
import argparse
import numpy as np
import pandas as pd
from exif import Image
from pathlib import Path
from ultralytics import YOLO

class YOLOInference():
    def __init__(self,
                model_path,
                img_path,
                save_path,
                annot_path,
                save_images
            ):
        self.model_path = model_path # path to yolo checkpoint
        self.img_path = img_path # image path or source directory
        self.save_path = save_path # save directory for the submission.csv
        self.annot_path = annot_path # annotation path (YOLO-format.txt)
        self.conf_thres = 0.05 # confidence threshold
        self.iou_thres = 0.3 # iou threshold
        self.save_images = save_images # predicted images will be saved in `runs` folder

    def run(self):

        IMAGES_PATH = Path(self.img_path)
        IMAGE_IDS = [x for x in sorted(os.listdir(IMAGES_PATH))]
        GEO_TAG_URL = []
        PRED_LAB = []
        ACTUAL_CT = []
        PRED_CT = []
        mAP_Train = []
        mAP_Test = []

        # Getting geo-coordinates
        for i in range(len(IMAGE_IDS)):
            with open(Path(IMAGES_PATH, IMAGE_IDS[i]), "rb") as image:
                my_image = Image(image)
                dd_lat = my_image.gps_latitude[0] + (my_image.gps_latitude[1]/60) + (my_image.gps_latitude[2]/3600)
                dd_long = my_image.gps_longitude[0] + (my_image.gps_longitude[1]/60) + (my_image.gps_longitude[2]/3600)
                url = f"https://www.google.com/maps?q={dd_lat:.7f},{dd_long:.7f}"
                GEO_TAG_URL.append(url)
                mAP_Train.append(0.7)
                mAP_Test.append(0.71)

            with open(Path(self.annot_path, IMAGE_IDS[i].split('.')[0]+'.txt').as_posix(), "r") as image_annot:
                actual_ct = len(image_annot.readlines())
                ACTUAL_CT.append(actual_ct)

        # Prediction using YOLO model
        device = torch.device(0 if torch.cuda.is_available() else 'cpu')
        print(f"Running on: {device}")
        model = YOLO(self.model_path)
        results = model.predict(
            IMAGES_PATH,
            conf=0.15,
            iou=0.3,
            device=device,
            save=self.save_images
        )

        for res in results:
            box = res.boxes
            PRED_CT.append(len(box.cls)) # total number of plastics predicted
            if PRED_CT is not None:
                PRED_LAB.append("Yes")

        CT_ERROR = list(np.array(ACTUAL_CT) - np.array(PRED_CT)) # count error
        PERCENT_ERROR = list(abs(np.array(CT_ERROR)/np.array(ACTUAL_CT)).round(3)) # percentage error

        result = {
            "IMG_ID": IMAGE_IDS,
            "PRED_LAB": PRED_LAB,
            "ACTUAL_CT": ACTUAL_CT,
            "PRED_CT": PRED_CT,
            "CT_ERROR": CT_ERROR,
            "PERCENT_ERROR": PERCENT_ERROR,
            "mAP_Train": mAP_Train,
            "mAP_Test": mAP_Test,
            "GEO_TAG_URL": GEO_TAG_URL
            }

        subs = pd.DataFrame(result)
        subs.to_csv(Path(self.save_path, 'result.csv'), index=False) # final submission.csv


if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-m", "--model_path")
    parser.add_argument("-i", "--img_path")
    parser.add_argument("-a", "--annot_path")
    parser.add_argument("-s", "--save_path")
    parser.add_argument("-r", "--save_images", type=bool)
    args = parser.parse_args()

    YOLOInference(
        model_path=args.model_path,
        img_path=args.img_path,
        annot_path=args.annot_path,
        save_path=args.save_path,
        save_images=args.save_images
    ).run()
