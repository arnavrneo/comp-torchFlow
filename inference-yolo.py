import pandas as pd
from pathlib import Path
from exif import Image
from ensemble_boxes import *
import argparse
import os
from sahi.predict import predict
from collections import Counter
import json

# YOLO Inference

class YOLOInference():
    def __init__(self,
                model_path,
                img_path,
                subs_file,
                dataset_json,
                conf_thres=0.05,
                iou_thres=0.3,
                save_path='./'
            ):
        self.model_path = model_path
        self.img_path = img_path
        self.subs_file = subs_file
        self.dataset_json = dataset_json
        self.conf_thres = conf_thres
        self.iou_thres = iou_thres
        self.save_path = save_path

    def run(self):
        # CSV
        IMAGES_PATH = Path(self.img_path)
        image_ids = [x for x in sorted(os.listdir(IMAGES_PATH))]
        subs = pd.read_csv(self.subs_file)
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

        model_type = "yolov8"
        model_path = self.model_path
        model_device = "cuda:0" # or 'cuda:0'
        model_confidence_threshold = self.conf_thres

        slice_height = 512
        slice_width = 512
        overlap_height_ratio = 0.2
        overlap_width_ratio = 0.2

        source_image_dir = IMAGES_PATH.as_posix()

        res = predict(
            model_type=model_type,
            model_path=model_path,
            model_device=model_device,
            model_confidence_threshold=model_confidence_threshold,
            source=source_image_dir,
            slice_height=slice_height,
            slice_width=slice_width,
            overlap_height_ratio=overlap_height_ratio,
            overlap_width_ratio=overlap_width_ratio,
            dataset_json_path=self.dataset_json,
            return_dict=True
        )
        res_path = res["export_dir"].as_posix() + "/result.json"
        result = json.load(open(res_path))
        counts = []
        for i in result:
            counts.append(i["image_id"])
        preds = Counter(counts)
        sorted_pred = sorted(preds.items(), key=lambda k: k[0])
        pred_ct = [x[1] for x in sorted_pred]

        ct_error = [int(subs["ACTUAL_CT"][i]) - pred_ct[i] for i in range(len(subs["ACTUAL_CT"]))]

        per_error = [round(abs(ct_error[i]/int(subs["ACTUAL_CT"][i])), 3) for i in range(len(subs["ACTUAL_CT"]))]

        subs["PRED_CT"] = pred_ct
        subs["CT_Error"] = ct_error
        subs["PERCENT_Error"] = per_error
        subs["GEO_Tag_URL"] = GEO_TAG_URL
        subs.to_csv(self.save_path + 'submission.csv', index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-m", "--model_path")
    parser.add_argument("-p", "--img_pth")
    parser.add_argument("-f", "--subs_file")
    parser.add_argument("-d", "--dataset_json")
    parser.add_argument("-c", "--conf_thres", type=float)
    parser.add_argument("-i", "--iou_thres", type=float)
    parser.add_argument("-s", "--save_path")
    # parser.add_argument("-d", "--device")
    args = parser.parse_args()

    YOLOInference(
        model_path=args.model_path,
        img_path=args.img_pth,
        subs_file=args.subs_file,
        dataset_json=args.dataset_json,
        conf_thres=args.conf_thres,
        iou_thres=args.iou_thres,
        save_path=args.save_path
    ).run()
