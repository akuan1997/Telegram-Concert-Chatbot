with open('concert_pin_postid.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

pin = "https://ticketplus.com.tw/activity/8455304be5b4ffef154340fd40d9dfa71"
for index, line in enumerate(lines):
    line_pin = line.split('|||')[1].replace('\n', '')
    if pin == line_pin:
        lines.pop(index)

# import json
# from y_example_read_json import *
#
# json_list = [
#     "concert_jsons/concert_3_14_23.json",
#     "concert_jsons/concert_3_17_16.json",
#     "concert_jsons/concert_3_17_19.json",
#     "concert_jsons/concert_3_18_13.json",
#     "concert_jsons/concert_3_20_16.json",
#     "concert_jsons/concert_3_22_0.json",
#     "concert_jsons/concert_3_23_14.json",
#     "concert_jsons/concert_3_24_8.json",
#     "concert_jsons/concert_3_25_0.json",
#     "concert_jsons/concert_3_25_17.json",
#     "concert_jsons/concert_3_26_0.json",
#     "concert_jsons/concert_3_27_3.json",
#     "concert_jsons/concert_3_29_0.json",
#     "concert_jsons/concert_3_30_13.json",
#     "concert_jsons/concert_3_30_20.json",
#     "concert_jsons/concert_3_31_14.json",
#     "concert_jsons/concert_3_31_18.json",
#     "concert_jsons/concert_4_15_1.json",
#     "concert_jsons/concert_4_2_0.json",
#     "concert_jsons/concert_4_3_10.json",
#     "concert_jsons/concert_4_3_22.json",
#     "concert_jsons/concert_4_4_14.json",
#     "concert_jsons/concert_4_4_3.json",
#     "concert_jsons/concert_4_5_16.json",
#     "concert_jsons/concert_4_7_17.json",
#     "concert_jsons/concert_5_2_14.json",
#     "concert_jsons/concert_5_4_20.json",
#     "concert_jsons/concert_5_7_1.json",
#     "concert_jsons/concert_5_7_21.json",
#     "concert_jsons/concert_5_8_16.json",
#
# ]
#
# # for i in range(len(json_list)):
# #     data = read_json(json_list[i])
# #     for j in range(len(data)):
# #         if data[j]['tit'] == '':
# #             print(data[j]['web'])
# #             print(data[j]['url'])
# #     print('-----------------------------------------')
#
# # data = read_json("concert_5_8_20.json")
# # data = read_json("concert_zh.json")
# # print(len(data))
# # blank_titles = []
# # for j in range(len(data)):
# #     if data[j]['tit'] == '':
# #         blank_titles.append(data[j])
# #         print(data[j]['web'])
# #         print(data[j]['url'])
# #         print('-----------------------------------------')
# # print(len(blank_titles))
# # not_exists = [6065, 6067, 6069, 6071, 6073, 6075, 6077, 6079, 6081, 6083, 6085, 6090, 6096, 6099, 6115, 6126, 6164, 6184, 6188, 6220, 6240]
# # exists = [6062, 6063, 6064, 6066, 6068, 6070, 6072, 6074, 6076, 6078, 6080, 6082, 6084, 6086, 6087, 6088, 6089, 6091, 6092, 6093, 6094, 6095, 6097, 6098, 6100, 6101, 6102, 6103, 6104, 6105, 6106, 6107, 6108, 6109, 6110, 6111, 6112, 6113, 6114, 6116, 6117, 6118, 6119, 6120, 6121, 6122, 6123, 6124, 6125, 6127, 6128, 6129, 6130, 6131, 6132, 6133, 6134, 6135, 6136, 6137, 6138, 6139, 6140, 6141, 6142, 6143, 6144, 6145, 6146, 6147, 6148, 6149, 6150, 6151, 6152, 6153, 6154, 6155, 6156, 6157, 6158, 6159, 6160, 6161, 6162, 6163, 6165, 6166, 6167, 6168, 6169, 6170, 6171, 6172, 6173, 6174, 6175, 6176, 6177, 6178, 6179, 6180, 6181, 6182, 6183, 6185, 6186, 6187, 6189, 6190, 6191, 6192, 6193, 6194, 6195, 6196, 6197, 6198, 6199, 6200, 6201, 6202, 6203, 6204, 6205, 6206, 6207, 6208, 6209, 6210, 6211, 6212, 6213, 6214, 6215, 6216, 6217, 6218, 6219, 6221, 6222, 6223, 6224, 6225, 6226, 6227, 6228, 6229, 6230, 6231, 6232, 6233, 6234, 6235, 6236, 6237, 6238, 6239, 6241, 6242, 6243, 6244, 6245, 6246, 6247, 6248, 6249, 6250, 6251, 6252, 6253, 6254, 6255, 6256, 6257, 6258, 6259, 6260, 6261, 6262, 6263, 6264, 6265, 6266, 6267, 6268, 6269, 6270, 6271, 6272, 6273, 6274, 6275, 6276, 6277, 6278, 6279, 6280, 6281, 6282, 6283, 6284, 6285, 6286, 6287, 6288, 6289, 6290, 6291, 6292, 6293, 6294, 6295, 6296, 6297, 6298, 6299, 6300, 6301, 6302, 6303, 6304, 6305, 6306, 6307, 6308, 6309, 6310, 6311, 6312, 6313, 6314, 6315, 6316, 6317, 6318, 6319, 6320, 6321, 6322, 6323, 6324, 6325, 6326]
# # problems = []
# # print(len(not_exists))
# # print(len(exists))
# # for i in range(31):
# #     print(i, i + 1)
# # data = read_json("singer_info.json")
# # # print(8101 + len(data))
# # with open('singer_postid_wikiurl.txt', 'w', encoding='utf-8') as f:
# #     f.write('')
# # for i in range(len(data)):
# #     with open('singer_postid_wikiurl.txt', 'a', encoding='utf-8') as f:
# #         f.write(f"{8101+i}|||{data[i]['singer_name']}|||{data[i]['singer_page_url']}\n")
# #     print('---')
# # from get_concert_info import *
#
# import shutil
# from googletrans import Translator
# import re
#
# zh_cities = ["台北", "新北", "桃園", "台中", "台南", "高雄", "基隆", "新竹", "苗栗", "彰化", "南投", "雲林",
#              "嘉義", "屏東", "宜蘭", "花蓮", "台東", "金門", "澎湖", "連江"]
# en_cities = ["Taipei", "New Taipei", "Taoyuan", "Taichung", "Tainan", "Kaohsiung", "Keelung", "Hsinchu", "Miaoli",
#              "Changhua", "Nantou", "Yunlin", "Chiayi", "Pingtung", "Yilan", "Hualien", "Taitung", "Kinmen", "Penghu",
#              "Lienchiang"]
# # city_mapping = dict(zip(zh_cities, en_cities))
# # # Copying the original file to a new file for translated content
# # shutil.copy(zh_json, en_json)
# #
# # translator = Translator()
# #
# # # Open the copied file for reading and translation
# # with open(en_json, 'r', encoding='utf-8') as f:
# #     data = json.load(f)
# #
# # for i in range(1):
# #     # print(f'current progress {i + 1}/{len(data)}')
# #     title = re.sub(r'[^\u4e00-\u9fa5]+', '', data[i]['int'])
# #     translated_title = translator.translate(data[i]['int'], src="zh-TW", dest="en").text
# #     print(translated_title)
# #
# #     # Check if 'int' field is not None or empty
# #     if data[i]['int']:
# #         try:
# #             # 使用正則表達式移除非中文字符
# #             data[i]['int'] = re.sub(r'[^\u4e00-\u9fa5]+', '', data[i]['int'])
# #             # Translate the text and update the 'int' field
# #             translated_text = translator.translate(data[i]['int'], src="zh-TW", dest="en").text
# #             data[i]['int'] = translated_text
# #             print('Successful')
# #         except Exception as e:
# #             print(f'Error translating: {e}')
# #             print('Skipping this entry')
# #     else:
# #         print('None or empty, skip')
# #
# #     # if 'cit' in data[i]:
# #     #     if data[i]['cit'] in city_mapping:
# #     #         data[i]['cit'] = city_mapping[data[i]['cit']]
# #     #         print(data[i]['cit'])
# #
# #             # with open('concert_test.json', 'w', encoding='utf-8') as f:
# #             #     json.dump(data, f, indent=4, ensure_ascii=False)
# #
# #     print('------------------------------------')
#
# import shutil
# import os
# from get_concert_new_old import *
#
#
# def get_old_json_filename(directory):
#     # 檢查目錄是否存在
#     if not os.path.exists(directory):
#         print(f"目錄 '{directory}' 不存在。")
#         return
#
#     # 獲取目錄中的所有檔案名稱
#     filenames = os.listdir(directory)
#
#     filenames = [filename for filename in filenames if ".json" in filename]
#
#     old_json = filenames[-1]
#
#     return old_json
#
#
# def get_new_old(json_filename):
#     shutil.move(json_filename, "concert_jsons")
#     old_json = get_old_json_filename(r"C:\Users\pfii1\akuan\git-repos\2024_Concert_Chatbot\concert_jsons")
#     new_json = json_filename
#     print(f"old_json = {old_json}")
#     print(f"new_json = {new_json}")
#
#     with open(f"concert_jsons/{old_json}", 'r', encoding='utf-8') as f:
#         old_data = json.load(f)
#     with open(f"concert_jsons/{new_json}", 'r', encoding='utf-8') as f:
#         new_data = json.load(f)
#     with open('concert_zh.json', 'r', encoding='utf-8') as f:
#         all_data = json.load(f)
#
#     pins_new = [entry['pin'] for entry in new_data]
#     pins_old = [entry['pin'] for entry in old_data]
#
#     new_but_old_pins = [pin for pin in pins_new if pin not in pins_old]
#     old_but_new_pins = [pin for pin in pins_old if pin not in pins_new]
#
#     print(f'len(new_data) = {len(new_data)}')
#     print(f'len(old_data) = {len(old_data)}')
#     print(f'len(all_data) = {len(all_data)}')
#     print(f'len(new_but_old_pins) = {len(new_but_old_pins)}')
#     print(f'len(old_but_new_pins) = {len(old_but_new_pins)}')
#
#     new_data_filtered, plus_concerts, all_data = get_new_delete_compare_concerts(new_but_old_pins, old_but_new_pins,
#                                                                                  new_data, old_data, all_data)
#
#     print(f"len(new_data_filtered) = {len(new_data_filtered)}")
#     print(f"len(plus_concerts) = {len(plus_concerts)}")
#     for i in range(len(plus_concerts)):
#         print(plus_concerts[i]['tit'])
#         print(plus_concerts[i]['url'])
#     print(f'運算結束 -> len(all_data) = {len(all_data)}')
#     # 寫進json裡面
#     write_json = 0  # 0 not write, 1 write (for testing)
#     if write_json == 1:
#         with open('concert_zh.json', "w", encoding="utf-8") as f:
#             json.dump(all_data, f, indent=4, ensure_ascii=False)
#             print('寫入成功')
#     else:
#         print('設定為未寫入')
#
#     return new_data_filtered, plus_concerts
#
#
# def move_back(filename):
#     current_directory = os.getcwd()
#     shutil.move(f"concert_jsons/{filename}",
#                 os.path.join(current_directory, os.path.basename(f"concert_jsons/{filename}")))
#
#
# move_back("concert_5_10_9.json")
# new_concerts, plus_concerts = get_new_old("concert_5_10_9.json")
# print(new_concerts)
# for concert in new_concerts:
#     print(concert['tit'])
#     print(concert['url'])
#     print()
# print(plus_concerts)
# import json

# data = read_json("concert_zh.json")
# indexes = [82, 96, 214]
# index = 207
# for index in indexes:
#     print(data[index]['tit'])
#     print('cit', data[index]['cit'])
#     print('sdt', data[index]['sdt'])
#     print('pdt', data[index]['pdt'])
#     print('---')
# from y_example_read_json import *
# data = read_json("singer_info.json")
# for i in range(len(data)):
#     if len(data[i]['singer_name']) == 2:
#         print(data[i]['singer_name'])
from y_example_read_json import *
json_list = [
    "concert_jsons/concert_3_14_23.json",
    "concert_jsons/concert_3_17_16.json",
    "concert_jsons/concert_3_17_19.json",
    "concert_jsons/concert_3_18_13.json",
    "concert_jsons/concert_3_20_16.json",
    "concert_jsons/concert_3_22_0.json",
    "concert_jsons/concert_3_23_14.json",
    "concert_jsons/concert_3_24_8.json",
    "concert_jsons/concert_3_25_0.json",
    "concert_jsons/concert_3_25_17.json",
    "concert_jsons/concert_3_26_0.json",
    "concert_jsons/concert_3_27_3.json",
    "concert_jsons/concert_3_29_0.json",
    "concert_jsons/concert_3_30_13.json",
    "concert_jsons/concert_3_30_20.json",
    "concert_jsons/concert_3_31_14.json",
    "concert_jsons/concert_3_31_18.json",
    "concert_jsons/concert_4_2_0.json",
    "concert_jsons/concert_4_3_10.json",
    "concert_jsons/concert_4_3_22.json",
    "concert_jsons/concert_4_4_14.json",
    "concert_jsons/concert_4_4_3.json",
    "concert_jsons/concert_4_5_16.json",
    "concert_jsons/concert_4_7_17.json",
    "concert_jsons/concert_4_15_1.json",
    "concert_jsons/concert_5_2_14.json",
    "concert_jsons/concert_5_4_20.json",
    "concert_jsons/concert_5_7_1.json",
    "concert_jsons/concert_5_7_21.json",
    "concert_jsons/concert_5_9_14.json",
    "concert_jsons/concert_5_10_11.json",
    "concert_jsons/concert_5_11_23.json",
    "concert_jsons/concert_5_12_11.json",
    "concert_jsons/concert_5_12_21.json"
]
# data = read_json("concert_jsons/concert_5_13_3.json")
# print(len(data))
change_pins = ['https://www.livenation.com.tw/show/1476056/jp-saxe-a-grey-area-world-tour/taipei/2024-05-23/tw0', 'https://www.livenation.com.tw/show/1476056/jp-saxe-a-grey-area-world-tour/taipei/2024-05-23/tw0', 'https://www.livenation.com.tw/show/1476056/jp-saxe-a-grey-area-world-tour/taipei/2024-05-23/tw0', 'https://www.livenation.com.tw/show/1476056/jp-saxe-a-grey-area-world-tour/taipei/2024-05-23/tw0', 'https://www.livenation.com.tw/show/1468089/elijah-woods-ilu-24-7-365-tour/taipei/2024-05-24/tw1', 'https://studpa.kktix.cc/events/ourstories2340', 'https://cohesionmusic.kktix.cc/events/0529-09110', 'https://cohesionmusic.kktix.cc/events/0529-09110', 'https://theuumouth.kktix.cc/events/uu2405290', 'https://theuumouth.kktix.cc/events/uu2405290', 'https://youngteam.kktix.cc/events/thefin20240', 'https://youngteam.kktix.cc/events/thefin20240', 'https://welcome-music.kktix.cc/events/asjfklj0', 'https://welcome-music.kktix.cc/events/asjfklj0', 'https://romanticoffice.kktix.cc/events/2406020', 'https://romanticoffice.kktix.cc/events/2406020', 'https://www.livenation.com.tw/show/1482266/gryffin-asia-tour-2024/taipei/2024-06-11/tw2', 'https://www.livenation.com.tw/show/1482266/gryffin-asia-tour-2024/taipei/2024-06-11/tw2', 'https://www.livenation.com.tw/show/1482266/gryffin-asia-tour-2024/taipei/2024-06-11/tw2', 'https://gorgeousettm.kktix.cc/events/kgrethj-030', 'https://gorgeousettm.kktix.cc/events/kgrethj-030', 'https://kklivetw.kktix.cc/events/2024riizefancontour-tp0', 'https://kklivetw.kktix.cc/events/2024riizefancontour-tp0', 'https://willmusic.kktix.cc/events/fesf5a0', 'https://willmusic.kktix.cc/events/fesf5a0', 'https://reasonbrothers.kktix.cc/events/ukllef-030', 'https://reasonbrothers.kktix.cc/events/ukllef-030', 'https://www.livenation.com.tw/show/1474356/%e6%bb%85%e7%81%ab%e5%99%a8-fire-ex-%e4%b8%80%e7%94%9f%e5%88%b0%e5%ba%95-one-life-one-shot-%e6%bc%94%e5%94%b1%e6%9c%83-%e5%8f%b0%e5%8c%97%e5%a0%b4/taipei/2024-06-15/tw3', 'https://www.livenation.com.tw/show/1474356/%e6%bb%85%e7%81%ab%e5%99%a8-fire-ex-%e4%b8%80%e7%94%9f%e5%88%b0%e5%ba%95-one-life-one-shot-%e6%bc%94%e5%94%b1%e6%9c%83-%e5%8f%b0%e5%8c%97%e5%a0%b4/taipei/2024-06-15/tw3', 'https://www.livenation.com.tw/show/1474356/%e6%bb%85%e7%81%ab%e5%99%a8-fire-ex-%e4%b8%80%e7%94%9f%e5%88%b0%e5%ba%95-one-life-one-shot-%e6%bc%94%e5%94%b1%e6%9c%83-%e5%8f%b0%e5%8c%97%e5%a0%b4/taipei/2024-06-15/tw3', 'https://www.livenation.com.tw/show/1474353/alexander-23-american-boy-in-asia/taipei/2024-06-16/tw4', 'https://reasonbrothers.kktix.cc/events/ukllef-060', 'https://reasonbrothers.kktix.cc/events/ukllef-060', 'https://theuumouth.kktix.cc/events/uu240623noon0', 'https://theuumouth.kktix.cc/events/uu240623noon0', 'https://www.livenation.com.tw/show/1485467/-babymonster-presents-see-you-there-in-taipei/taipei/2024-06-23/tw5', 'https://www.livenation.com.tw/show/1485467/-babymonster-presents-see-you-there-in-taipei/taipei/2024-06-23/tw5', 'https://www.livenation.com.tw/show/1485467/-babymonster-presents-see-you-there-in-taipei/taipei/2024-06-23/tw5', 'https://www.livenation.com.tw/show/1478141/atarashii-gakko-world-tour-/taipei/2024-06-27/tw6', 'https://www.livenation.com.tw/show/1478141/atarashii-gakko-world-tour-/taipei/2024-06-27/tw6', 'https://spaceport.kktix.cc/events/erdye50', 'https://spaceport.kktix.cc/events/erdye50', 'https://omni.kktix.cc/events/pcewg0', 'https://omni.kktix.cc/events/pcewg0', 'https://www.livenation.com.tw/show/1484004/alec-benjamin-12-notes-tour/taipei/2024-07-24/tw8', 'https://www.livenation.com.tw/show/1484004/alec-benjamin-12-notes-tour/taipei/2024-07-24/tw8', 'https://www.livenation.com.tw/show/1484004/alec-benjamin-12-notes-tour/taipei/2024-07-24/tw8', 'https://www.livenation.com.tw/show/1480300/%e8%a1%80%e8%82%89%e6%9e%9c%e6%b1%81%e6%a9%9f-2024%e5%bb%ba%e5%ae%ae%e8%93%8b%e5%bb%9f-%e5%ae%87%e5%ae%99%e9%a0%90%e8%a8%80/taipei/2024-07-27/tw9', 'https://www.livenation.com.tw/show/1480300/%e8%a1%80%e8%82%89%e6%9e%9c%e6%b1%81%e6%a9%9f-2024%e5%bb%ba%e5%ae%ae%e8%93%8b%e5%bb%9f-%e5%ae%87%e5%ae%99%e9%a0%90%e8%a8%80/taipei/2024-07-27/tw9', 'https://www.livenation.com.tw/show/1480300/%e8%a1%80%e8%82%89%e6%9e%9c%e6%b1%81%e6%a9%9f-2024%e5%bb%ba%e5%ae%ae%e8%93%8b%e5%bb%9f-%e5%ae%87%e5%ae%99%e9%a0%90%e8%a8%80/taipei/2024-07-27/tw9', 'https://www.livenation.com.tw/show/1483048/chris-james-dopamine-overload-asia-tour-2024/taipei/2024-08-22/tw10', 'https://www.livenation.com.tw/show/1483048/chris-james-dopamine-overload-asia-tour-2024/taipei/2024-08-22/tw10', 'https://www.livenation.com.tw/show/1483048/chris-james-dopamine-overload-asia-tour-2024/taipei/2024-08-22/tw10', 'https://www.livenation.com.tw/show/1485152/conan-gray-found-heaven-on-tour/taipei/2024-08-30/tw11', 'https://www.livenation.com.tw/show/1483664/laufey-bewitched-the-goddess-tour-asia-and-australia-/taipei/2024-08-31/tw12', 'https://www.livenation.com.tw/show/1483664/laufey-bewitched-the-goddess-tour-asia-and-australia-/taipei/2024-08-31/tw12', 'https://www.livenation.com.tw/show/1485511/nigel-ng-the-haiyaa-world-tour/taipei/2024-09-26/tw13', 'https://www.livenation.com.tw/show/1485511/nigel-ng-the-haiyaa-world-tour/taipei/2024-09-26/tw13', 'https://www.livenation.com.tw/show/1485511/nigel-ng-the-haiyaa-world-tour/taipei/2024-09-26/tw13', 'https://www.livenation.com.tw/show/1474950/lany-a-beautiful-blur-the-world-tour/kaohsiung/2024-10-04/tw14', 'https://www.livenation.com.tw/show/1474950/lany-a-beautiful-blur-the-world-tour/kaohsiung/2024-10-04/tw14', 'https://www.livenation.com.tw/show/1474950/lany-a-beautiful-blur-the-world-tour/kaohsiung/2024-10-04/tw14', 'https://www.livenation.com.tw/show/1484599/porter-robinson-smile-d-world-tour/taipei/2024-12-10/tw15', 'https://www.livenation.com.tw/show/1484599/porter-robinson-smile-d-world-tour/taipei/2024-12-10/tw15', 'https://www.livenation.com.tw/show/1484599/porter-robinson-smile-d-world-tour/taipei/2024-12-10/tw15']
data = read_json("concert_zh.json")
for i in range(len(data)):
    for pin in change_pins:
        if data[i]['pin'] == pin:
            print(data[i]['pin'])
# index = 30
# for k in range(index, index + 1):
#     # data1 = read_json("concert_jsons/concert_5_11_23.json")
#     # data2 = read_json("concert_jsons/concert_5_12_11.json")
#     data1 = read_json(json_list[k])
#     data2 = read_json(json_list[k+1])
#     for i in range(len(data1)):
#         for j in range(len(data2)):
#             if data1[i]['pin'] == data2[j]['pin']:
#                 if data1[i]['tit'] != data2[j]['tit']:
#                     print(data1[i]['tit'])
#                     print(data1[i]['url'])
#                     print(data2[i]['tit'])
#                     print(data2[i]['url'])
#                     print('---')
