import os

folder_path = r'./web_scraping'

# 使用os模块列出文件夹中的所有文件
for filename in os.listdir(folder_path):
    if os.path.isfile(os.path.join(folder_path, filename)):
        print(filename.replace('.mhtml', ''))
        print()
