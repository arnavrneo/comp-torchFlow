from ultralytics import YOLO
from ultralytics.yolo.utils import yaml_load
from pathlib import Path
from types import SimpleNamespace
import argparse
import torch
from sahi import AutoDetectionModel
from sahi.utils.cv import read_image
from sahi.predict import get_sliced_prediction, predict
from sahi.scripts.coco_evaluation import evaluate

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-m", "--ckpt")
parser.add_argument("-i", "--img_dir")
parser.add_argument("-d", "--dataset_json")
args = parser.parse_args()
ckpt = args.ckpt
img_dir = args.img_dir
dataset_json = args.dataset_json

def cfg2dict(cfg):
    if isinstance(cfg, (str, Path)):
        cfg = yaml_load(cfg)  # load dict
    elif isinstance(cfg, SimpleNamespace):
        cfg = vars(cfg)  # convert to dict
    return cfg

def val(img_dir=img_dir, ckpt=ckpt, dataset_json=dataset_json, cfg="config/val-config.yaml"):
    # Loading pretrained model
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Running on: {device}")
    # model = YOLO(ckpt["ckpt"])
    # model.to(device)
    # args = cfg2dict(cfg)

    # # Training on custom config.yaml file
    # model.val(
    #     **args
    # )
    model_type = "yolov8"
    model_path = ckpt
    model_device = "cuda:0" # or 'cuda:0'
    model_confidence_threshold = 0.4

    slice_height = 512
    slice_width = 512
    overlap_height_ratio = 0.2
    overlap_width_ratio = 0.2

    source_image_dir = img_dir

    predict(
        model_type=model_type,
        model_path=model_path,
        model_device=model_device,
        model_confidence_threshold=model_confidence_threshold,
        source=source_image_dir,
        slice_height=slice_height,
        slice_width=slice_width,
        overlap_height_ratio=overlap_height_ratio,
        overlap_width_ratio=overlap_width_ratio,
        dataset_json_path=dataset_json
    )


if __name__ == "__main__":
    val()