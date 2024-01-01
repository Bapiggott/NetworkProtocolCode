# q.tr = a.tr + a.td
# "srcport": "18570",
#                 "dstport": "14550",
#                 "length": "71",
#                 "checksum": "0xfe5a",
#                 "status": "2",
#                 "stream": "0",
#                 "time_relative": "6.326299000",
#                 "time_delta": "0.000063000"
import json

input_vector = ['output_predictions_test_udp_small_distilgpt2_final_version.json']
name = ["distilgpt2-50k-10epoch"]

fields_vector = ["srcport", "dstport", "length", "checksum", "status", "stream", "time_relative", "time_delta"]
message_vectors = [[] for _ in range(9)]
message_vectors_shorten = [0, 0]
field_mesg_wrong = [[0.0 for _ in range(len(fields_vector))] for _ in range(len(input_vector))]
field_pct_right = [[0.0 for _ in range(len(fields_vector))] for _ in range(len(input_vector))]
stnd_dev, avg_time, entries_total,average_amnt_errors = [], [], [], []
file_count = 0


for input_file_path in input_vector:
    field_vector = fields_vector
    section_vector  = ["Question", "Predicted_TCP_Packet", "Correct_Answer"]
    entry_vector = ['Entry']
    field_data = {section: {field: [] for field in field_vector} for section in section_vector}
    field_correction_check = {field: [] for field in field_vector}
    time_list= []
    error_vector = [[] for _ in range(9)]

    same_source = 0
    time_right = 0

    def print_percentage(name, percentage):
        print(f"{name} is correct: {(percentage * 100) :.4f}%")


    with open(input_file_path, 'r') as f:
        data = json.load(f)
    context_data = {entry_num: [{field: [] for field in field_vector} for _ in range(len(entry['Context']))] for entry_num, entry in enumerate(data)}

    for entry_num, entry in enumerate(data):
        context_list = entry['Context']
        for context_num, context in enumerate(context_list):
            for field in field_vector:
                context_data[entry_num][context_num][field] = context[field]


    for entry in data:
        for field in field_vector:
            for section in section_vector:
                value = entry[section][field]
                field_data[section][field].append(value)
        time = entry["Time_Taken"]
        time_list.append(time)

    for index in range(len(field_data["Question"][field_vector[3]])):
        for field in field_vector:
            if field_data["Predicted_TCP_Packet"][field][index] != field_data["Correct_Answer"][field][index]:
                field_correction_check[field].append(1)
                # field_correction_check[field= 1
            elif field_data["Predicted_TCP_Packet"][field][index] == field_data["Correct_Answer"][field][index]:
                field_correction_check[field].append(0)
        if field_data[section_vector[0]][field_vector[0]][index] == field_data[section_vector[1]][field_vector[0]][index]:
            same_source += 1
            print(field_data[section_vector[1]][field_vector[6]][index])
        if field_data[section_vector[0]][field_vector[6]][index] == field_data[section_vector[1]][field_vector[6]][index] + field_data[section_vector[1]][field_vector[7]][index]:
            time_right += 1
    print(time_right)
    # print(field_correction_check[field_vector[0]])
    for field_count in range(len(field_vector)):
        print_percentage(field_vector[field_count], 1 - (sum(field_correction_check[field_vector[field_count]])) / len(field_data["Question"][field_vector[0]]))
        field_pct_right[file_count][field_count] = round((1 - (sum(field_correction_check[field_vector[field_count]])) / len(field_data["Question"][field_vector[0]])) * 100, 4)
    same_source_perc = ((same_source / len(field_data["Question"][field_vector[0]])) * 100)
    print(f"Source is the same for the question as it is for the answer: {same_source_perc :.4f}%")

    time_right_perc = ((time_right / len(field_data["Question"][field_vector[0]])) * 100)
    print(f"Times are right in comparison to time delta and time relative with the q/a: {time_right_perc :.4f}%")