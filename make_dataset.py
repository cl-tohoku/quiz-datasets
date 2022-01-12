import argparse
import csv
import gzip
import json
from copy import copy
from typing import Optional

from elasticsearch import Elasticsearch
from tqdm import tqdm

from utils import normalize_question, normalize_answer


class ElasticsearchPassageRetriever():
    def __init__(self, index: str, host: str, port: int) -> None:
        self.es = Elasticsearch(hosts=[{"host": host, "port": port}], timeout=60)
        self.index = index

    def query(
        self,
        query_text: str,
        size: int = 10,
        min_inlinks: Optional[int] = None,
        exclude_disambiguation_pages: bool = False,
        exclude_sexual_pages: bool = False,
        exclude_violent_pages: bool = False,
    ):
        query = {
            "query": {
                "bool": {
                    "must": {
                        "match": {
                            "text": query_text
                        },
                    },
                },
            },
            "size": size
        }
        filter_settings = []
        if min_inlinks is not None:
            filter_settings.append({"range": {"num_inlinks": {"gte": min_inlinks}}})
        if exclude_disambiguation_pages:
            filter_settings.append({"term": {"is_disambiguation_page": False}})
        if exclude_sexual_pages:
            filter_settings.append({"term": {"is_sexual_page": False}})
        if exclude_violent_pages:
            filter_settings.append({"term": {"is_violent_page": False}})

        query["query"]["bool"]["filter"] = filter_settings

        response = self.es.search(index=self.index, body=query)
        passages = []
        for item in response["hits"]["hits"]:
            passage = {
                "passage_id": item["_source"]["id"],
                "title": item["_source"]["title"],
                "text": item["_source"]["text"]
            }
            passages.append(passage)

        return passages


def main(args: argparse.Namespace):
    passage_retriever = ElasticsearchPassageRetriever(
        index=args.es_index_name, host=args.es_hostname, port=args.es_port
    )

    num_positive_question = 0
    num_negative_question = 0
    num_output_question = 0

    with gzip.open(args.output_file, "wt") as fo:
        for input_file in args.input_files:
            with open(input_file) as f:
                reader = csv.DictReader(f, delimiter="\t")
                for row in tqdm(reader):
                    # Preprocess question
                    if "question" in row:
                        full_question = row["question"]
                    else:
                        full_question = normalize_question(row["original_question"])

                    # If specified, split the question into into variable lengths
                    if args.num_question_splits > 1:
                        n = args.num_question_splits
                        end_positions = [int(len(full_question) * (i + 1) / n) for i in range(n)]
                        questions = [full_question[:end] for end in end_positions]
                    else:
                        questions = [full_question]

                    # Preprocess the answers
                    if "answer" in row:
                        answers = row["answer"].split(";;")
                    else:
                        answers = [normalize_answer(answer) for answer in row["original_answer"].split(";;")]

                    for question in questions[::-1]:
                        # Prepare an output item
                        output_item = copy(row)
                        output_item["question"] = question
                        output_item["answers"] = answers
                        if args.num_question_splits > 1:
                            output_item["full_question"] = full_question

                        # If specified, retrieve passages relevant to the question
                        if args.num_passages_per_question is not None:
                            passages = passage_retriever.query(
                                question,
                                size=args.num_passages_per_question,
                                min_inlinks=args.min_inlinks,
                                exclude_disambiguation_pages=args.exclude_disambiguation_pages,
                                exclude_sexual_pages=args.exclude_sexual_pages,
                                exclude_violent_pages=args.exclude_violent_pages,
                            )

                            # Distant supervision by matching the passage (and its title) to the answers
                            positive_passage_indices = []
                            negative_passage_indices = []
                            for i, passage in enumerate(passages):
                                if any(answer in passage["text"] for answer in answers):
                                    positive_passage_indices.append(i)
                                elif args.match_to_title and any(answer in passage["title"] for answer in answers):
                                    positive_passage_indices.append(i)
                                else:
                                    negative_passage_indices.append(i)

                                if args.no_passage_text:
                                    del passage["text"]

                            if len(positive_passage_indices) > 0:
                                num_positive_question += 1
                            else:
                                num_negative_question += 1
                                if args.skip_no_positive:
                                    continue

                            output_item["passages"] = passages
                            output_item["positive_passage_indices"] = positive_passage_indices
                            output_item["negative_passage_indices"] = negative_passage_indices

                        print(json.dumps(output_item, ensure_ascii=False), file=fo)
                        num_output_question += 1

    if args.num_passages_per_question is not None:
        print("Questions with at least one positive passage:", num_positive_question)
        print("Questions with no positive passage:", num_negative_question)
        if args.skip_no_positive:
            print("    (these questions are skipped because --skip_no_positive is enabled)")

    print("Total output questions:", num_output_question)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_files", nargs='+', type=str, required=True)
    parser.add_argument("--output_file", type=str, required=True)
    parser.add_argument("--num_passages_per_question", type=int)
    parser.add_argument("--es_index_name", type=str)
    parser.add_argument("--es_hostname", type=str, default="localhost")
    parser.add_argument("--es_port", type=int, default=9200)
    parser.add_argument("--min_inlinks", type=int)
    parser.add_argument("--exclude_disambiguation_pages", action="store_true")
    parser.add_argument("--exclude_sexual_pages", action="store_true")
    parser.add_argument("--exclude_violent_pages", action="store_true")
    parser.add_argument("--skip_no_positive", action="store_true")
    parser.add_argument("--match_to_title", action="store_true")
    parser.add_argument("--num_question_splits", type=int, default=1)
    parser.add_argument("--no_passage_text", action="store_true")
    args = parser.parse_args()
    main(args)
