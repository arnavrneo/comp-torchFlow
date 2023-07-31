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
        cfg="config/val-config.yaml"
    ):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Running on: {device}")

    # Loading pretrained model
    model = YOLO(ckpt)
    model.to(device)
    args = cfg2dict(cfg)

    model.val(
        **args
    )

if __name__ == "__main__":
    # run !python config.config.py to set data directories according to the system
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-m", "--ckpt")
    args = parser.parse_args()

    val(
        ckpt=args.ckpt
    )
