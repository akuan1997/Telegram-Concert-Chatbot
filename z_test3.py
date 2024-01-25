import shutil
import os

concert_json_filenames = ['era.json', 'indievox.json', 'kktix.json', 'livenation.json', 'ticketplus.json']




move_concert_files(concert_json_filenames)

# source_file = 'z_test2.py'
# target_folder = 'kuan_test_folder'
#
# # 检查目标文件是否存在，如果存在，删除它
# if os.path.exists(os.path.join(target_folder, source_file)):
#     os.remove(os.path.join(target_folder, source_file))
#
# # 使用shutil.move()函数来移动文件
# shutil.move(source_file, target_folder)
