# Copyright 2020 The HuggingFace Datasets Authors and the current dataset script contributor.
# Copyright 2023 Masatoshi Suzuki (@singletongue)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Quiz Datasets for NLP"""

import json
from typing import Any, Dict, Iterator, List, Tuple

import datasets


_DESCRIPTION = "Question answering (QA) datasets created from Japanese quiz (trivia) questions."

_HOMEPAGE = "https://github.com/cl-tohoku/quiz-datasets"

_LICENSE = """\
一部のクイズ問題の著作権は abc/EQIDEN 実行委員会 に帰属します。東北大学において研究目的での再配布許諾を得ています。
一部のクイズ問題は株式会社キュービック および クイズ法人カプリティオ に依頼し作成したものであり、\
これらのクイズ問題は Creative Commons Attribution-ShareAlike 4.0 International ライセンスの下に提供されています。
読解データセットにパッセージとして付与されている Wikipedia のコンテンツは、\
Attribution-ShareAlike 3.0 Unported ライセンスおよび GFDL ライセンスの下に配布されているものです。
"""

_URL_BASE = "https://github.com/cl-tohoku/quiz-datasets/releases/download"
_URLS = {
    "datasets.no_passages.aio_02": {
        "train": f"{_URL_BASE}/v1.0.0/datasets.no_passages.aio_02_train.jsonl.gz",
        "dev": f"{_URL_BASE}/v1.0.0/datasets.no_passages.aio_02_dev.jsonl.gz",
    },
    "datasets.jawiki-20220404-c400-small.aio_02": {
        "train": f"{_URL_BASE}/v1.0.0/datasets.jawiki-20220404-c400-small.aio_02_train.jsonl.gz",
        "dev": f"{_URL_BASE}/v1.0.0/datasets.jawiki-20220404-c400-small.aio_02_dev.jsonl.gz",
    },
    "datasets.jawiki-20220404-c400-medium.aio_02": {
        "train": f"{_URL_BASE}/v1.0.0/datasets.jawiki-20220404-c400-medium.aio_02_train.jsonl.gz",
        "dev": f"{_URL_BASE}/v1.0.0/datasets.jawiki-20220404-c400-medium.aio_02_dev.jsonl.gz",
    },
    "datasets.jawiki-20220404-c400-large.aio_02": {
        "train": f"{_URL_BASE}/v1.0.0/datasets.jawiki-20220404-c400-large.aio_02_train.jsonl.gz",
        "dev": f"{_URL_BASE}/v1.0.0/datasets.jawiki-20220404-c400-large.aio_02_dev.jsonl.gz",
    },
    "passages.jawiki-20220404-c400-small": {
        "train": f"{_URL_BASE}/v1.0.1/passages.jawiki-20220404-c400-small.jsonl.gz",
    },
    "passages.jawiki-20220404-c400-medium": {
        "train": f"{_URL_BASE}/v1.0.1/passages.jawiki-20220404-c400-medium.jsonl.gz",
    },
    "passages.jawiki-20220404-c400-large": {
        "train": f"{_URL_BASE}/v1.0.1/passages.jawiki-20220404-c400-large.jsonl.gz",
    },
}

_VERSION = datasets.Version("1.0.1")


class QuizDatasets(datasets.GeneratorBasedBuilder):
    """Datasets from cl-tohoku/quiz-datasets."""

    BUILDER_CONFIGS = [datasets.BuilderConfig(name=name, version=_VERSION) for name in _URLS.keys()]

    def _info(self) -> datasets.DatasetInfo:
        if self.config.name.startswith("datasets"):
            features = datasets.Features(
                {
                    "qid": datasets.Value("string"),
                    "competition": datasets.Value("string"),
                    "timestamp": datasets.Value("string"),
                    "section": datasets.Value("string"),
                    "number": datasets.Value("string"),
                    "original_question": datasets.Value("string"),
                    "original_answer": datasets.Value("string"),
                    "original_additional_info": datasets.Value("string"),
                    "question": datasets.Value("string"),
                    "answers": datasets.Sequence(datasets.Value("string")),
                }
            )
            if not self.config.name.startswith("datasets.no_passages"):
                features.update({
                    "passages": datasets.Sequence(
                        {
                            "passage_id": datasets.Value("int32"),
                            "title": datasets.Value("string"),
                            "text": datasets.Value("string"),
                        }
                    ),
                    "positive_passage_indices": datasets.Sequence(datasets.Value("int32")),
                    "negative_passage_indices": datasets.Sequence(datasets.Value("int32")),
                })
        elif self.config.name.startswith("passages"):
            features = datasets.Features(
                {
                    "id": datasets.Value("int32"),
                    "pageid": datasets.Value("int32"),
                    "revid": datasets.Value("int32"),
                    "text": datasets.Value("string"),
                    "section": datasets.Value("string"),
                    "title": datasets.Value("string"),
                }
            )
        else:
            raise ValueError("Invalid dataset config name is specified.")

        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            homepage=_HOMEPAGE,
            license=_LICENSE,
        )


    def _split_generators(self, dl_manager: datasets.DownloadManager) -> List[datasets.SplitGenerator]:
        urls = _URLS[self.config.name]
        filepaths = dl_manager.download_and_extract(urls)

        split_generators = [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": filepaths["train"]})
        ]
        if "dev" in filepaths:
            split_generators.append(
                datasets.SplitGenerator(name=datasets.Split.VALIDATION, gen_kwargs={"filepath": filepaths["dev"]})
            )

        return split_generators

    def _generate_examples(self, filepath: str) -> Iterator[Tuple[int, Dict[str, Any]]]:
        with open(filepath) as f:
            for i, line in enumerate(f):
                item = json.loads(line)
                yield i, item
