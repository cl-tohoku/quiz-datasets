---
dataset_info:
- config_name: datasets.jawiki-20220404-c400-small.aio_02
  features:
  - name: qid
    dtype: string
  - name: competition
    dtype: string
  - name: timestamp
    dtype: string
  - name: section
    dtype: string
  - name: number
    dtype: string
  - name: original_question
    dtype: string
  - name: original_answer
    dtype: string
  - name: original_additional_info
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence: string
  - name: passages
    sequence:
    - name: passage_id
      dtype: int32
    - name: title
      dtype: string
    - name: text
      dtype: string
  - name: positive_passage_indices
    sequence: int32
  - name: negative_passage_indices
    sequence: int32
  splits:
  - name: train
    num_bytes: 2041349194
    num_examples: 22335
  - name: validation
    num_bytes: 91754993
    num_examples: 1000
  download_size: 805138940
  dataset_size: 2133104187
- config_name: datasets.jawiki-20220404-c400-medium.aio_02
  features:
  - name: qid
    dtype: string
  - name: competition
    dtype: string
  - name: timestamp
    dtype: string
  - name: section
    dtype: string
  - name: number
    dtype: string
  - name: original_question
    dtype: string
  - name: original_answer
    dtype: string
  - name: original_additional_info
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence: string
  - name: passages
    sequence:
    - name: passage_id
      dtype: int32
    - name: title
      dtype: string
    - name: text
      dtype: string
  - name: positive_passage_indices
    sequence: int32
  - name: negative_passage_indices
    sequence: int32
  splits:
  - name: train
    num_bytes: 1875144339
    num_examples: 22335
  - name: validation
    num_bytes: 84499229
    num_examples: 1000
  download_size: 723119604
  dataset_size: 1959643568
- config_name: datasets.jawiki-20220404-c400-large.aio_02
  features:
  - name: qid
    dtype: string
  - name: competition
    dtype: string
  - name: timestamp
    dtype: string
  - name: section
    dtype: string
  - name: number
    dtype: string
  - name: original_question
    dtype: string
  - name: original_answer
    dtype: string
  - name: original_additional_info
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence: string
  - name: passages
    sequence:
    - name: passage_id
      dtype: int32
    - name: title
      dtype: string
    - name: text
      dtype: string
  - name: positive_passage_indices
    sequence: int32
  - name: negative_passage_indices
    sequence: int32
  splits:
  - name: train
    num_bytes: 1743060319
    num_examples: 22335
  - name: validation
    num_bytes: 78679502
    num_examples: 1000
  download_size: 665253451
  dataset_size: 1821739821
- config_name: passages.jawiki-20220404-c400-small
  features:
  - name: id
    dtype: int32
  - name: pageid
    dtype: int32
  - name: revid
    dtype: int32
  - name: text
    dtype: string
  - name: section
    dtype: string
  - name: title
    dtype: string
  splits:
  - name: train
    num_bytes: 348002946
    num_examples: 394124
  download_size: 121809648
  dataset_size: 348002946
- config_name: passages.jawiki-20220404-c400-medium
  features:
  - name: id
    dtype: int32
  - name: pageid
    dtype: int32
  - name: revid
    dtype: int32
  - name: text
    dtype: string
  - name: section
    dtype: string
  - name: title
    dtype: string
  splits:
  - name: train
    num_bytes: 1322478989
    num_examples: 1678986
  download_size: 469426075
  dataset_size: 1322478989
- config_name: passages.jawiki-20220404-c400-large
  features:
  - name: id
    dtype: int32
  - name: pageid
    dtype: int32
  - name: revid
    dtype: int32
  - name: text
    dtype: string
  - name: section
    dtype: string
  - name: title
    dtype: string
  splits:
  - name: train
    num_bytes: 3054493919
    num_examples: 4288198
  download_size: 1110830651
  dataset_size: 3054493919
- config_name: datasets.no_passages.aio_02
  features:
  - name: qid
    dtype: string
  - name: competition
    dtype: string
  - name: timestamp
    dtype: string
  - name: section
    dtype: string
  - name: number
    dtype: string
  - name: original_question
    dtype: string
  - name: original_answer
    dtype: string
  - name: original_additional_info
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence: string
  splits:
  - name: train
    num_bytes: 9464003
    num_examples: 22335
  - name: validation
    num_bytes: 409779
    num_examples: 1000
  download_size: 2267163
  dataset_size: 9873782
---

# Quiz Datasets for NLP

Question answering (QA) datasets created from Japanese quiz (trivia) questions.

Please refer to [cl-tohoku/quiz-datasets](https://github.com/cl-tohoku/quiz-datasets) for details, as well as the licenses of the question data.