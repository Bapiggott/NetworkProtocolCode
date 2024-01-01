import os
import ijson


def count(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            with open(f'{directory}/{filename}', 'rb') as file:

                jsonobj = ijson.items(file, 'item', use_float=True)
                total_datasets = sum(1 for _ in jsonobj)
                print(f'File: {filename}\nTotal number of entries: {total_datasets}\n---------------------')


if __name__ == "__main__":
    input_directory = '/home/px4/bala/old/datasets'
    count(input_directory)
