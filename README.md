
Project Name
Overview

This repository contains a collection of Python scripts developed for processing, analyzing, and finetuning models on a large dataset. The original dataset comprised over 25 million items, which was reduced and utilized for training a model with specific characteristics.
Files Description
Data Processing Scripts

    accuracy_tested_modal_tcp.py: Script for testing the accuracy of the model on TCP data.
    accuracy_tested_modal_udp.py: Script for testing the accuracy of the model on UDP data.
    big_json2csv2.py: Converts large JSON files into CSV format.
    count_datasets.py: Counts the number of datasets in a given directory.
    create_dataset.py: A utility for creating datasets from raw data.
    divide_dataset.py: Divides a large dataset into smaller, manageable chunks.
    finetuning_script.py: Script used for finetuning models on specific datasets.
    fix_testing_json.py: Repairs issues in JSON files used for testing.
    json2csv.py: Converts JSON files to CSV format.
    merge_adapters.py: Merges different data adapters.
    test_finetuning2.py: Tests the finetuning process on a given model.

Research Results Summary

    The original dataset had 25,048,044 items. This was reduced to 2,976,476 items by filtering unique source/destination pairs.
    A 50k item dataset was created for training, resulting in 60 JSON files.
    The model was trained using distlgpt2 over 10 epochs.
    Testing was conducted with 3,274 questions on the finetuned model.

Model Testing Accuracy

    srcport: 0.0000%
    dstport: 0.0000%
    length: 0.0000%
    checksum: 0.0000%
    status: 100.0000%
    stream: 100.0000%
    time_relative: 0.0000%
    time_delta: 0.0305%
    Source consistency (question vs. answer): 100.0000%
    Time accuracy (relative to delta and time in Q/A): 0.0000%

Conclusion

The results indicate specific areas where the model performs well and areas where improvement is needed, particularly in accurately predicting various network parameters like srcport, dstport, length, and time-related metrics.
