# Validation script

from ultralytics import YOLO
from ultralytics.yolo.utils import yaml_load
from pathlib import Path
from types import SimpleNamespace
import argparse
import torch


def cfg2dict(cfg):
    if isinstance(cfg, (str, Path)):
        cfg = yaml_load(cfg)  # load dict
    elif isinstance(cfg, SimpleNamespace):
        cfg = vars(cfg)  # convert to dict
    return cfg

def val(ckpt, cfg="config/val-config.yaml"):
    # Loading pretrained model
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Running on: {device}")
    model = YOLO(ckpt)
    model.to(device)
    args = cfg2dict(cfg)

    # Training on custom config.yaml file
    model.val(
        **args
    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-m", "--ckpt")
    args = parser.parse_args()
    ckpt = args.ckpt

    val(
        ckpt=ckpt
    )


# python val.py -m <model-ckpt.pt> -i <img-dir> -d <coco-annot-for-set.json> -c 0.3