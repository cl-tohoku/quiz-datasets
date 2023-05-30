import argparse
import csv
import gzip
import json

from tqdm import tqdm


HEADER_COLS = ["id", "text", "title"]


def main(args: argparse.Namespace):
    with gzip.open(args.passages_file, "rt") as f, gzip.open(args.output_file, "wt", newline="") as fo:
        tsv_writer = csv.writer(fo, delimiter="\t")
        tsv_writer.writerow(HEADER_COLS)
        for line in tqdm(f):
            passage_item = json.loads(line)

            passage_id = passage_item["id"]

            title = passage_item["title"]
            assert "\t" not in title

            text = passage_item["text"]
            assert "\t" not in text

            tsv_writer.writerow([passage_id, text, title])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--passages_file", type=str, required=True)
    parser.add_argument("--output_file", type=str, required=True)
    args = parser.parse_args()
    main(args)
