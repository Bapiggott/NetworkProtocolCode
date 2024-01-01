import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import json
import time

# Load the finetuned Llama-2 model and tokenizer
model_name = 'udp_small_distilgpt2_1' # "udp_small_distilgpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name, local_files_only=True)
model = AutoModelForCausalLM.from_pretrained(model_name, local_files_only=True)
#CUDA_LAUNCH_BLOCKING=1 python3 test_finetuning.py

def generate_tcp_packet(context, question):
    # Format the input dialogues and context
    instruction = "### Prompt: Provided below is a question detailing key attributes of a UDP packet. Preceding this question is a series of UDP packets, which together form the context. Please continue the sequence by providing the subsequent TCP packet that follows the question, serving as the answer. \n\n"
    context_prompt = "### Context:\n" + str(context) + "\n"
    question_prompt = "### Question\n" + str(question) + "\n"

    # Generate the next TCP packet prediction
    prompt = instruction + context_prompt + question_prompt + "### Answer:\n"
    input_ids = tokenizer.encode(prompt, return_tensors="pt")
    with torch.no_grad():
        start_time = time.time()
        output = model.generate(input_ids, max_length=1000, num_return_sequences=1)
        end_time = time.time()

    # Decode the generated output to get the predicted TCP packet
    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
    time_taken = end_time - start_time
    return generated_text, time_taken
input_file = 'datasets/sub_dataset_59.json' # '/home/brett/dataset_check/Testing_dataset/testing_data_random_100.json'
# Load data from JSON file
with open(input_file, 'r') as file:
    data = json.load(file)

output_file = f'output_predictions_test_{model_name}_new.json'
output_data = []
count_value = 1

try:
    for entry in data:  # data is a list, iterate directly over it
        context = entry['Context']
        question = entry['Question']
        correct_answer = entry['Answer']

        # Generate the next predicted TCP packet and measure time taken
        next_tcp_packet, time_taken = generate_tcp_packet(context, question)

        # Store results in output_data
        output_data.append({
            'Context': context,
            'Question': question,
            'Predicted_TCP_Packet': next_tcp_packet,
            'Correct_Answer': correct_answer,
            'Time_Taken': time_taken
        })

        # Write results to the JSON file after processing each entry
        with open(output_file, 'w') as outfile:
            json.dump(output_data, outfile, indent=4)

        # print("Entry:", entry)
        print("Question:", question)
        print("Predicted Next TCP Packet:")
        print(next_tcp_packet)
        print("Correct Answer:")
        print(correct_answer)
        print("Time Taken:", time_taken, "seconds")
        print("Total q/a's done: ", count_value)
        print("=" * 30)
        count_value += 1

except KeyboardInterrupt:
    print("Execution interrupted. Saving progress to", output_file)
    with open(output_file, 'w') as outfile:
        json.dump(output_data, outfile, indent=4)

print("Predictions saved to:", output_file)