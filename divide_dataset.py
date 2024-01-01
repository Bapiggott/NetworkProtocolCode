import json
import math
import ijson


def divide(input_file_path):
        """with open(input_file_path, 'a') as file:
            file.write(']')
            print('added ] to file')"""
        with open(input_file_path, 'rb') as file:
            # print(input_file_path)
            first_items = []
            size = 50000
            total_datasets = 0
            jsonobj = ijson.items(file, 'item', use_float=True)
            total_datasets = sum(1 for _ in jsonobj)
            num_files = math.ceil(total_datasets / size)
            print(f'Total number of entries: {total_datasets}\nTotal number of files that\'ll be created: {num_files}')
            for _ in range(60): # total_datasets):
                # with open(f'sub_dataset_{index}.json', 'a') as output_file:
                # output_file.write('[\n')
                first_items.append(True)
            # num_files = 60
            jsonobj = ijson.items(file, 'item', use_float=True)
            counter = 0
            for item in jsonobj:
                counter += 1
                index = counter
                # for index, item in jsonobj:
                print(f'index: {index}')
                try:
                    file_index = index % num_files
                    with open(f'datasets/sub_dataset_{file_index}.json', 'a') as output_file:
                        if not first_items[file_index]:
                            output_file.write(",\n")
                        else: #  first_items[index]:
                            output_file.write('[\n')
                            first_items[file_index] = False
                        json_string = json.dumps(item, indent=4)
                        # json_string = json_string[1:-1]
                        output_file.write(json_string)
                except Exception as ex:
                    print(ex)
                    continue

            for index in range(num_files):
                with open(f'datasets/sub_dataset_{index}.json', 'a') as output_file:
                    output_file.write("\n]")


if __name__ == "__main__":
    input_filename = '/home/px4/bala/7slidding_window_testing.json'
    divide(input_filename)

    # for 2slidding_window_testing.json
    # Total number of entries: 25,548,044
    # Total number of files that'll be created: 511

    # for 7slidding_window_testing.json
    # Total number of entries: 2,976,476
    # Total number of files that'll be created: 60
