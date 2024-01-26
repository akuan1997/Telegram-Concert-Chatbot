# import json
#
# with open('concert_test.json', 'r', encoding='utf-8') as f:
#     data = json.load(f)
#
# for i in range(len(data)):
#     data[i]['cit'] = '123'
#     with open('concert_test.json', 'w', encoding='utf-8') as f:
#         json.dump(data, f, indent=4, ensure_ascii=False)

new_data = [
    {
    'a': [],
    'b': [""]
    }
]

print('hello', new_data[0]['a'])
print('hello', new_data[0]['b'])
if new_data[0]['b']:
    print('11')
elif not new_data[0]['a']:
    print('33')
else:
    print('22')