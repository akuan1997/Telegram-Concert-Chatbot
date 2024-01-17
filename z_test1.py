import os

folder_path = r'G:\我的雲端硬碟\論文\文獻閱讀\網頁備份\新增資料夾'

# 使用os模块列出文件夹中的所有文件
for filename in os.listdir(folder_path):
    if os.path.isfile(os.path.join(folder_path, filename)):
        print(filename.replace('.mhtml', ''))
        print()

#

#

#