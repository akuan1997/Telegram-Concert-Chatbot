import json

with open('concert_data_old.json', 'r', encoding='utf-8') as old_file:
    old_data = json.load(old_file)

with open('concert_data_new.json', 'r', encoding='utf-8') as new_file:
    new_data = json.load(new_file)

with open('concert_data_old.json', 'w', encoding='utf-8') as old_file:
    json.dump(new_data, old_file, indent=4, ensure_ascii=False)