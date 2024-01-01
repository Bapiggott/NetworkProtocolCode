import pandas as pd
import json
import os
import concurrent.futures

def process_file(filename):
    try:
        # Read the JSON file
        with open(f'./datasets/{filename}', "r") as json_file:
            data = json.load(json_file)

        formatted_data = []

        # Loop through each record in the list
        for record in data:
            formatted_record = {
                "Context": record["Context"],
                "Question": record["Question"],
                "Answer": record["Answer"]
            }
            formatted_data.append(formatted_record)

        # Create a DataFrame from the formatted data
        df = pd.DataFrame(formatted_data)

        # Perform your operations on the DataFrame
        df = df.fillna("")

        text_col = []
        for _, row in df.iterrows():
            prompt = "Provided below is a question detailing key attributes of a UDP packet. Preceding this question is a series of UDP packets, which together form the context. Please continue the sequence by providing the subsequent UDP packet that follows the question, serving as the answer. \n\n"
            question = str(row["Question"])
            context = str(row["Context"])
            answer = str(row["Answer"])

            text = prompt + "### Context:\n" + context + "\n### Question\n" + question + "\n### Answer:\n" + answer

            text_col.append(text)

        df.loc[:, "text"] = text_col

        # Save the DataFrame as CSV
        df.to_csv(f"./csvs/{filename}.csv", index=False)
        print(f"Processed file: {filename}")

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON in file {filename}: {e}")

if __name__ == "__main__":
    directory = 'datasets'

    with concurrent.futures.ProcessPoolExecutor() as executor:
        # Process each file concurrently
        futures = [executor.submit(process_file, filename) for filename in os.listdir(directory) if filename.endswith(".json")]

        # Wait for all futures to complete
        concurrent.futures.wait(futures)

