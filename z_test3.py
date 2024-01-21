import json

with open('artists.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for i in range(len(data)):
    if data[i]['image_name'] == '-':
        print(data[i]['names'])
        print(data[i]['article_url'])