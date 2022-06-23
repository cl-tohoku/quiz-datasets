import argparse
import gzip
import json

from tqdm import tqdm


def main(args: argparse.Namespace):
    n_output_questions = 0
    n_skipped_questions = 0
    with gzip.open(args.input_file, "rt") as f, gzip.open(args.output_file, "wt") as fo:
        if not args.write_jsonl:
            fo.write("[")

        for i, line in tqdm(enumerate(f)):
            qa_item = json.loads(line)

            passages = qa_item["passages"]
            positive_passages = [passages[i] for i in qa_item["positive_passage_indices"]]
            negative_passages = [passages[i] for i in qa_item["negative_passage_indices"]]

            if args.skip_no_positive and len(positive_passages) == 0:
                n_skipped_questions += 1
                continue

            output_item = {
                "qid": qa_item["qid"],
                "timestamp": qa_item["timestamp"],
                "dataset": args.dataset_label,
                "question": qa_item["question"],
                "answers": qa_item["answers"],
                "positive_ctxs": positive_passages,
                "negative_ctxs": [],
                "hard_negative_ctxs": negative_passages
            }
            if args.write_jsonl:
                print(json.dumps(output_item, ensure_ascii=False), file=fo)
            else:
                if n_output_questions > 0:
                    fo.write(",")
                for line in json.dumps(output_item, ensure_ascii=False, indent=4).split("\n"):
                    fo.write("\n    " + line)

            n_output_questions += 1

        if not args.write_jsonl:
            fo.write("\n]")

    print("The number of output questions:", n_output_questions)
    if args.skip_no_positive:
        print("The number of skipped questions:", n_skipped_questions)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_file", type=str, required=True)
    parser.add_argument("--output_file", type=str, required=True)
    parser.add_argument("--dataset_label", type=str)
    parser.add_argument("--write_jsonl", action="store_true")
    parser.add_argument("--skip_no_positive", action="store_true")
    args = parser.parse_args()
    main(args)
