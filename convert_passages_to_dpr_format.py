import argparse
import gzip
import json

from logzero import logger
from tqdm import tqdm


HEADER_COLS = ["id", "text", "title"]


def main(args):
    page_info = dict()
    logger.info("Loading page ids file")
    with open(args.page_ids_file) as f:
        for line in tqdm(f):
            pageid_item = json.loads(line)
            pageid = pageid_item.pop("pageid")
            page_info[pageid] = pageid_item

    logger.info("Processing input file")
    with gzip.open(args.passages_file, "rt") as f, gzip.open(args.output_file, "wt") as fo:
        print(*HEADER_COLS, sep="\t", file=fo)
        for line in tqdm(f):
            passage_item = json.loads(line)
            pageid = passage_item["pageid"]

            if args.min_inlinks is not None and page_info[pageid]["num_inlinks"] < args.min_inlinks:
                continue
            if args.exclude_disambiguation_pages and page_info[pageid]["is_disambiguation_page"]:
                continue
            if args.exclude_sexual_pages and page_info[pageid]["is_sexual_page"]:
                continue
            if args.exclude_violent_pages and page_info[pageid]["is_violent_page"]:
                continue

            passage_id = passage_item["id"]

            title = passage_item["title"]
            assert "\t" not in title

            text = passage_item["text"]
            text = json.dumps(text, ensure_ascii=False)
            assert "\t" not in text

            print(passage_id, text, title, sep="\t", file=fo)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--passages_file", type=str, required=True)
    parser.add_argument("--page_ids_file", type=str, required=True)
    parser.add_argument("--output_file", type=str, required=True)
    parser.add_argument("--min_inlinks", type=int)
    parser.add_argument("--exclude_disambiguation_pages", action="store_true")
    parser.add_argument("--exclude_sexual_pages", action="store_true")
    parser.add_argument("--exclude_violent_pages", action="store_true")
    args = parser.parse_args()
    main(args)
