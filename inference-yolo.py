# Inference script for YOLOv8 model

import os
import torch
import argparse
import pandas as pd
from exif import Image
from pathlib import Path
from ultralytics import YOLO

class YOLOInference():
    def __init__(self,
                model_path,
                img_path,
                subs_file,
                save_path,
                save_images=False
            ):
        self.model_path = model_path # path to yolo checkpoint
        self.img_path = img_path # image path or source directory
        self.subs_file = subs_file # submission.csv file
        self.save_path = save_path # save directory for the submission.csv

        self.conf_thres = 0.05 # confidence threshold
        self.iou_thres = 0.3 # iou threshold
        self.save_images = save_images # predicted images will be saved in `runs` folder

    def run(self):

        subs = pd.read_csv(self.subs_file)
        IMAGES_PATH = Path(self.img_path)
        IMAGE_IDS = [x for x in sorted(os.listdir(IMAGES_PATH))]
        GEO_TAG_URL = []

        # Getting geo-coordinates
        for i in range(len(IMAGE_IDS)):
            with open(Path(IMAGES_PATH, IMAGE_IDS[i]), "rb") as image:
                my_image = Image(image)
                dd_lat = my_image.gps_latitude[0] + (my_image.gps_latitude[1]/60) + (my_image.gps_latitude[2]/3600)
                dd_long = my_image.gps_longitude[0] + (my_image.gps_longitude[1]/60) + (my_image.gps_longitude[2]/3600)
                url = f"https://www.google.com/maps?q={dd_lat:.7f},{dd_long:.7f}"
                GEO_TAG_URL.append(url)

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

        pred_ct = []
        for res in results:
            box = res.boxes
            pred_ct.append(len(box.cls)) # total number of plastics predicted

        ct_error = [int(subs["ACTUAL_CT"][i]) - pred_ct[i] for i in range(len(subs["ACTUAL_CT"]))] # count error
        per_error = [round(abs(ct_error[i]/int(subs["ACTUAL_CT"][i])), 3) for i in range(len(subs["ACTUAL_CT"]))] # percentage error

        subs["PRED_CT"] = pred_ct
        subs["CT_Error"] = ct_error
        subs["PERCENT_Error"] = per_error
        subs["GEO_Tag_URL"] = GEO_TAG_URL
        subs.to_csv(self.save_path + 'submission.csv', index=False) # final submission.csv


if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-m", "--model_path")
    parser.add_argument("-p", "--img_pth")
    parser.add_argument("-f", "--subs_file")
    parser.add_argument("-s", "--save_path")
    parser.add_argument("-r", "--save_images", type=bool)
    args = parser.parse_args()

    YOLOInference(
        model_path=args.model_path,
        img_path=args.img_pth,
        subs_file=args.subs_file,
        save_path=args.save_path,
        save_images=args.save_images
    ).run()
