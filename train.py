# Training script

import argparse
import torch
from pathlib import Path
from ultralytics import YOLO
from types import SimpleNamespace
from ultralytics.yolo.utils import yaml_load

# Loading configuration from train-config.yaml
def cfg2dict(cfg):
    if isinstance(cfg, (str, Path)):
        cfg = yaml_load(cfg)  # load dict
    elif isinstance(cfg, SimpleNamespace):
        cfg = vars(cfg)  # convert to dict
    return cfg

def train(ckpt, cfg="config/train-config.yaml"):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Running on: {device}")

    # Loading pretrained model
    model = YOLO(ckpt)
    model.to(device)
    args = cfg2dict(cfg)

    model.train( # the checkpoint will be stored in the `runs` directory
        **args
    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-m", "--ckpt")
    args = parser.parse_args()
    train(
        ckpt=args.ckpt
    )
