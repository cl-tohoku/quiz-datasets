import argparse
import gzip
import json

from tqdm import tqdm


def main(args: argparse.Namespace):
    with gzip.open(args.input_file, "rt") as f, open(args.output_file, "w") as fo:
        for line in tqdm(f):
            qa_item = json.loads(line)

            question = qa_item["question"]
            answers = qa_item["answers"]

            print(question, json.dumps(answers, ensure_ascii=False), sep="\t", file=fo)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_file", type=str, required=True)
    parser.add_argument("--output_file", type=str, required=True)
    args = parser.parse_args()
    main(args)
