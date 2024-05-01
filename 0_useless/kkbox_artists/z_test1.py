import json

# with open('artist_korean1.json', 'r', encoding='utf-8') as f:
#     data = json.load(f)
#
# with open('korean_sorted.txt', 'r', encoding='utf-8') as f:
#     lines = f.readlines()
# lines = [line.replace('\n', '') for line in lines]


# for line in lines:
#     for i in range(len(data)):
#         if data[i]['singer_name'] in line:
#             if data[i]['singer_name'] == line:
#                 pass
#             elif '(' in line:
#                 print(line)
#                 print(data[i]['singer_name'])
#                 data[i]['singer_name'] = line
#                 with open('artist_korean1.json', "w", encoding="utf-8") as f:
#                     json.dump(data, f, indent=4, ensure_ascii=False)
#                 print('---')
from fuzzywuzzy import fuzz


def missing(all_artists, json_file):
    with open(all_artists, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    lines = [line.replace('\n', '') for line in lines]

    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for line in lines:
        found = False
        for i in range(len(data)):
            if data[i]['singer_name'] == line:
                found = True
                break
        if not found:
            print(line)


missing('korean_sorted.txt', 'artist_korean1.json')
# with open('korean_sorted.txt', 'r', encoding='utf-8') as f:
#     lines = f.readlines()
# lines = [line.replace('\n', '') for line in lines]
#
# with open('artist_korean1.json', 'r', encoding='utf-8') as f:
#     data = json.load(f)
#
# for line in lines:
#     for i in range(len(data)):
#         sim = fuzz.ratio(line, data[i]['singer_name'])
#         if sim > 70:
#             if line == data[i]["singer_name"]:
#                 pass
#             else:
#                 print(line)
#                 print(data[i]["singer_name"])
#                 print('---')
