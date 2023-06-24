from ultralytics import YOLO
from ultralytics.yolo.utils import yaml_load
from pathlib import Path
from types import SimpleNamespace
import argparse
import torch

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-m", "--ckpt")
ckpt = vars(parser.parse_args())

def cfg2dict(cfg):
    if isinstance(cfg, (str, Path)):
        cfg = yaml_load(cfg)  # load dict
    elif isinstance(cfg, SimpleNamespace):
        cfg = vars(cfg)  # convert to dict
    return cfg

def train(ckpt=ckpt, cfg="config/train-config.yaml"):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Running on: {device}")
    # Loading pretrained model
    model = YOLO(ckpt["ckpt"])
    model.to(device)
    args = cfg2dict(cfg)

    # Training on custom config.yaml file
    model.train(
        **args
    )

if __name__ == "__main__":
    train()