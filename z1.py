# with open('concert_pin_postid.txt', 'r', encoding='utf-8') as f:
#     lines = f.readlines()
#
# pin = "https://ticketplus.com.tw/activity/8455304be5b4ffef154340fd40d9dfa71"
# for index, line in enumerate(lines):
#     line_pin = line.split('|||')[1].replace('\n', '')
#     if pin == line_pin:
#         lines.pop(index)
#
# with open('concert_pin_postid1.txt', 'w', encoding='utf-8') as f:
#     f.writelines(lines)
#
# print(lines)
# print(len(lines))
import json
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
    "concert_jsons/concert_4_15_1.json",
    "concert_jsons/concert_4_2_0.json",
    "concert_jsons/concert_4_3_10.json",
    "concert_jsons/concert_4_3_22.json",
    "concert_jsons/concert_4_4_14.json",
    "concert_jsons/concert_4_4_3.json",
    "concert_jsons/concert_4_5_16.json",
    "concert_jsons/concert_4_7_17.json",
    "concert_jsons/concert_5_2_14.json",
    "concert_jsons/concert_5_4_20.json",
    "concert_jsons/concert_5_7_1.json",
    "concert_jsons/concert_5_7_21.json",
    "concert_jsons/concert_5_8_16.json",

]

# for i in range(len(json_list)):
#     data = read_json(json_list[i])
#     for j in range(len(data)):
#         if data[j]['tit'] == '':
#             print(data[j]['web'])
#             print(data[j]['url'])
#     print('-----------------------------------------')

# data = read_json("concert_5_8_20.json")
# data = read_json("concert_zh.json")
# print(len(data))
# blank_titles = []
# for j in range(len(data)):
#     if data[j]['tit'] == '':
#         blank_titles.append(data[j])
#         print(data[j]['web'])
#         print(data[j]['url'])
#         print('-----------------------------------------')
# print(len(blank_titles))
# not_exists = [6065, 6067, 6069, 6071, 6073, 6075, 6077, 6079, 6081, 6083, 6085, 6090, 6096, 6099, 6115, 6126, 6164, 6184, 6188, 6220, 6240]
# exists = [6062, 6063, 6064, 6066, 6068, 6070, 6072, 6074, 6076, 6078, 6080, 6082, 6084, 6086, 6087, 6088, 6089, 6091, 6092, 6093, 6094, 6095, 6097, 6098, 6100, 6101, 6102, 6103, 6104, 6105, 6106, 6107, 6108, 6109, 6110, 6111, 6112, 6113, 6114, 6116, 6117, 6118, 6119, 6120, 6121, 6122, 6123, 6124, 6125, 6127, 6128, 6129, 6130, 6131, 6132, 6133, 6134, 6135, 6136, 6137, 6138, 6139, 6140, 6141, 6142, 6143, 6144, 6145, 6146, 6147, 6148, 6149, 6150, 6151, 6152, 6153, 6154, 6155, 6156, 6157, 6158, 6159, 6160, 6161, 6162, 6163, 6165, 6166, 6167, 6168, 6169, 6170, 6171, 6172, 6173, 6174, 6175, 6176, 6177, 6178, 6179, 6180, 6181, 6182, 6183, 6185, 6186, 6187, 6189, 6190, 6191, 6192, 6193, 6194, 6195, 6196, 6197, 6198, 6199, 6200, 6201, 6202, 6203, 6204, 6205, 6206, 6207, 6208, 6209, 6210, 6211, 6212, 6213, 6214, 6215, 6216, 6217, 6218, 6219, 6221, 6222, 6223, 6224, 6225, 6226, 6227, 6228, 6229, 6230, 6231, 6232, 6233, 6234, 6235, 6236, 6237, 6238, 6239, 6241, 6242, 6243, 6244, 6245, 6246, 6247, 6248, 6249, 6250, 6251, 6252, 6253, 6254, 6255, 6256, 6257, 6258, 6259, 6260, 6261, 6262, 6263, 6264, 6265, 6266, 6267, 6268, 6269, 6270, 6271, 6272, 6273, 6274, 6275, 6276, 6277, 6278, 6279, 6280, 6281, 6282, 6283, 6284, 6285, 6286, 6287, 6288, 6289, 6290, 6291, 6292, 6293, 6294, 6295, 6296, 6297, 6298, 6299, 6300, 6301, 6302, 6303, 6304, 6305, 6306, 6307, 6308, 6309, 6310, 6311, 6312, 6313, 6314, 6315, 6316, 6317, 6318, 6319, 6320, 6321, 6322, 6323, 6324, 6325, 6326]
# problems = []
# print(len(not_exists))
# print(len(exists))
for i in range(31):
    print(i, i + 1)