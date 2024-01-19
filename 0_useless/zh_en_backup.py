from googletrans import Translator
import json
import shutil
import time
import re

# Copying the original file to a new file for translated content
shutil.copy('../concert_data_new_zh.json', 'concert_data_new_en.json')

translator = Translator()

# Open the copied file for reading and translation
with open('../concert_data_new_en.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

start_time = time.time()

# Iterate over each concert data entry
for i in range(len(data)):
    print(f'current progress {i}/{len(data)}')

    # Check if 'int' field is not None or empty
    if data[i]['int']:
        try:
            # 使用正則表達式移除非中文字符
            data[i]['int'] = re.sub(r'[^\u4e00-\u9fa5]+', '', data[i]['int'])
            # Translate the text and update the 'int' field
            translated_text = translator.translate(data[i]['int'], src="zh-TW", dest="en").text
            data[i]['int'] = translated_text
            print('Successful')
        except Exception as e:
            print(f'Error translating: {e}')
            print('Skipping this entry')
    else:
        print('None or empty, skip')

    print('------------------------------------')

# Write the translated data back to the file
with open('../concert_data_new_en.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

end_time = time.time()
print(f'Total time taken: {end_time - start_time} seconds')
