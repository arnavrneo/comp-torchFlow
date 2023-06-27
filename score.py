from sahi.scripts.coco_evaluation import evaluate
import argparse

def score(test_json, pred_json):
    evaluate(
        dataset_json_path=test_json,
        result_json_path=pred_json
    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-t", "--test_json")
    parser.add_argument("-p", "--pred_json")
    args = parser.parse_args()
    test_json = args.test_json
    pred_json = args.pred_json

    score(test_json, pred_json)