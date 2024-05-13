import json
def merge_json_data(json_filenames, final_json_file):
    merged_data = []

    for file in json_filenames:
        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            merged_data.extend(data)

        with open(final_json_file, 'w', encoding='utf-8') as f:
            json.dump(merged_data, f, indent=4, ensure_ascii=False)

# concert_json_filenames = ['era.json', 'indievox.json', 'kktix.json', 'livenation.json', 'ticketplus.json']
# merge_json_data(concert_json_filenames, "concert_5_13_3.json")  # combine all the website json file into the second argument
with open('../concert_jsons/concert_5_13_3.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
print(len(data))