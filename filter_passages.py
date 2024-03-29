import argparse
import gzip
import json

from tqdm import tqdm


HEADER_COLS = ["id", "text", "title"]


def main(args: argparse.Namespace):
    page_info = dict()
    with open(args.page_ids_file) as f:
        for line in tqdm(f):
            pageid_item = json.loads(line)
            pageid = pageid_item.pop("pageid")
            page_info[pageid] = pageid_item

    titles = set()
    n_passages = 0
    with gzip.open(args.passages_file, "rt") as f, gzip.open(args.output_file, "wt") as fo:
        for line in tqdm(f):
            passage_item = json.loads(line)
            pageid = passage_item["pageid"]
            title = passage_item["title"]

            if args.min_inlinks is not None and page_info[pageid]["num_inlinks"] < args.min_inlinks:
                continue
            if args.exclude_disambiguation_pages and page_info[pageid]["is_disambiguation_page"]:
                continue
            if args.exclude_sexual_pages and page_info[pageid]["is_sexual_page"]:
                continue
            if args.exclude_violent_pages and page_info[pageid]["is_violent_page"]:
                continue

            fo.write(line)

            titles.add(title)
            n_passages += 1

    print("The number of output page titles:", len(titles))
    print("The number of output passages:", n_passages)


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
