# Validation script

import argparse
import torch
from pathlib import Path
from ultralytics import YOLO
from types import SimpleNamespace
from ultralytics.yolo.utils import yaml_load

# Loading configuration from val-config.yaml
def cfg2dict(cfg):
    if isinstance(cfg, (str, Path)):
        cfg = yaml_load(cfg)  # load dict
    elif isinstance(cfg, SimpleNamespace):
        cfg = vars(cfg)  # convert to dict
    return cfg

def val(
        ckpt,
        imgsz,
        batch,
        conf,
        iou,
        cfg="config/val-config.yaml"
    ):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Running on: {device}")

    # Loading pretrained model
    model = YOLO(ckpt)
    model.to(device)
    args = cfg2dict(cfg)

    model.val(
        data="config/dataset.yaml",
        imgsz=imgsz, # [640, 480]
        batch=batch,
        save_json=True,
        save_hybrid=False,
        conf=conf,
        iou=iou,
        max_det=300,
        half=True,
        device=0,
        dnn=False,
        plots=False,
        rect=False,
        split="val"
    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-m", "--ckpt")
    parser.add_argument("-s", "--img_size", type=int)
    parser.add_argument("-b", "--batch_size", type=int)
    parser.add_argument("-c", "--conf", type=float)
    parser.add_argument("-i", "--iou", type=float)
    args = parser.parse_args()

    val(
        ckpt=args.ckpt,
        imgsz=args.img_size,
        batch=args.batch_size,
        conf=args.conf,
        iou=args.iou
    )
