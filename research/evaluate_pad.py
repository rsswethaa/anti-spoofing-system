"""Evaluate liveness prediction scores with PAD metrics.

Input CSV columns:
  label,score,attack_type
where label is BONA_FIDE or ATTACK and score is the bona-fide probability.
"""
import argparse
import csv
import json

from src.pad_metrics import evaluate_pad


def load_csv(path):
    with open(path,newline='',encoding='utf-8') as handle:
        return list(csv.DictReader(handle))


def main():
    parser=argparse.ArgumentParser(); parser.add_argument('csv'); parser.add_argument('--threshold',type=float,default=.5); args=parser.parse_args()
    print(json.dumps(evaluate_pad(load_csv(args.csv),args.threshold),indent=2))


if __name__=='__main__':
    main()
