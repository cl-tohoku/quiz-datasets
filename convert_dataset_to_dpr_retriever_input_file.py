import argparse
import gzip
import json

from tqdm import tqdm


def main(args: argparse.Namespace):
    with gzip.open(args.input_file, "rt") as f, gzip.open(args.output_file, "wt") as fo:
        if not args.write_jsonl:
            fo.write("[")

        for i, line in tqdm(enumerate(f)):
            qa_item = json.loads(line)

            passages = qa_item["passages"]
            positive_passages = [passages[i] for i in qa_item["positive_passage_indices"]]
            negative_passages = [passages[i] for i in qa_item["negative_passage_indices"]]

            output_item = {
                "qid": qa_item["qid"],
                "timestamp": qa_item["timestamp"],
                "question": qa_item["question"],
                "answers": qa_item["answers"],
                "positive_ctxs": positive_passages,
                "negative_ctxs": [],
                "hard_negative_ctxs": negative_passages
            }
            if args.write_jsonl:
                print(json.dumps(output_item, ensure_ascii=False), file=fo)
            else:
                if i > 0:
                    fo.write(",")
                for line in json.dumps(output_item, ensure_ascii=False, indent=4).split("\n"):
                    fo.write("\n    " + line)

        if not args.write_jsonl:
            fo.write("\n]")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_file", type=str, required=True)
    parser.add_argument("--output_file", type=str, required=True)
    parser.add_argument("--write_jsonl", action="store_true")
    args = parser.parse_args()
    main(args)
