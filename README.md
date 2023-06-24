- Steps

    - `git clone https://github.com/arnavrneo/comp-torchFlow.git`

    - `pip install -r requirements.txt`

    - Create `dataset` directory in the format:
        - ```
            dataset/
                images/
                labels/
          ```
        - or download by running:
            `./get-dataset.sh`.
            For permission, first do `chmod u+x ./get-dataset.sh`.

- Train
    - For training, do:
        - `python train.py -m <model-name/or-model-path>`
    - For changing params, edit `train-config.yaml`.
    - Ckpts will be saved in `runs` directory.

- Val
    - For validation, do:
        - `python val.py -m <model-checkpoint-path>`
    - For changing params, edit `val-config.yaml`.

- Inference
    - WIP
