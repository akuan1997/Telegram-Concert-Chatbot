import os


def get_filenames(directory):
    # 檢查目錄是否存在
    if not os.path.exists(directory):
        print(f"目錄 '{directory}' 不存在。")
        return

    # 獲取目錄中的所有檔案名稱
    filenames = os.listdir(directory)

    # 顯示所有檔案名稱
    for filename in filenames:
        print(filename)


# 輸入要查看的目錄路徑
directory_path = r"C:\Users\pfii1\akuan\git-repos\2024_Concert_Chatbot\concert_jsons"
get_filenames(directory_path)
