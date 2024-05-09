# from y_example_read_json import *
# data = read_json("concert_zh.json")
#
# for i in range(len(data)):
#     for j in range(i + 1, len(data)):
#         if data[i]['pin'] == data[j]['pin']:
#             print(data[i]['pin'])
#
# with open('concert_pin_postid.txt', 'r', encoding='utf-8') as f:
#     lines = f.readlines()
# pins = [line.split('|||')[1].replace('\n', '') for line in lines]
# for i in range(len(pins)):
#     for j in range(i + 1, len(pins)):
#         if pins[i] == pins[j]:
#             print(pins[i])
""""""
# not_exists = [5487, 5489, 5491, 5493, 5495, 5497, 5499, 5501, 5503, 5505, 5507, 5512, 5518, 5521, 5537, 5586, 5606, 5610, 5662, 5733, 5735, 5737, 5739, 5742]
# exists = [5484, 5485, 5486, 5488, 5490, 5492, 5494, 5496, 5498, 5500, 5502, 5504, 5506, 5508, 5509, 5510, 5511, 5513, 5514, 5515, 5516, 5517, 5519, 5520, 5522, 5523, 5524, 5525, 5526, 5527, 5528, 5529, 5530, 5531, 5532, 5533, 5534, 5535, 5536, 5538, 5539, 5540, 5541, 5542, 5543, 5544, 5545, 5546, 5547, 5548, 5549, 5550, 5551, 5552, 5553, 5554, 5555, 5556, 5557, 5558, 5559, 5560, 5561, 5562, 5563, 5564, 5565, 5566, 5567, 5568, 5569, 5570, 5571, 5572, 5573, 5574, 5575, 5576, 5577, 5578, 5579, 5580, 5581, 5582, 5583, 5584, 5585, 5587, 5588, 5589, 5590, 5591, 5592, 5593, 5594, 5595, 5596, 5597, 5598, 5599, 5600, 5601, 5602, 5603, 5604, 5605, 5607, 5608, 5609, 5611, 5612, 5613, 5614, 5615, 5616, 5617, 5618, 5619, 5620, 5621, 5622, 5623, 5624, 5625, 5626, 5627, 5628, 5629, 5630, 5631, 5632, 5633, 5634, 5635, 5636, 5637, 5638, 5639, 5640, 5641, 5642, 5643, 5644, 5645, 5646, 5647, 5648, 5649, 5650, 5651, 5652, 5653, 5654, 5655, 5656, 5657, 5658, 5659, 5660, 5661, 5663, 5664, 5665, 5666, 5667, 5668, 5669, 5670, 5671, 5672, 5673, 5674, 5675, 5676, 5677, 5678, 5679, 5680, 5681, 5682, 5683, 5684, 5685, 5686, 5687, 5688, 5689, 5690, 5691, 5692, 5693, 5694, 5695, 5696, 5697, 5698, 5699, 5700, 5701, 5702, 5703, 5704, 5705, 5706, 5707, 5708, 5709, 5710, 5711, 5712, 5713, 5714, 5715, 5716, 5717, 5718, 5719, 5720, 5721, 5722, 5723, 5724, 5725, 5726, 5727, 5728, 5729, 5730, 5731, 5743, 5744, 5745, 5746, 5747, 5748, 5749, 5750, 5751, 5752, 5753, 5754, 5755, 5756, 5757, 5758, 5759]
# problems = [5732, 5734, 5736, 5738, 5740, 5741, 5760, 5761, 5762, 5763, 5764, 5765, 5766, 5767, 5768, 5769, 5770, 5771, 5772]
# print(len(not_exists))
# print(len(exists))
# print(len(problems))
""""""
# print(len(data))
# print(len(pins))
# print('---')
# matched = []
# mores = []
# for i in range(len(data)):
#     found = False
#     for pin in pins:
#         if data[i]['pin'] == pin:
#             matched.append(pin)
#             found = True
#     if not found:
#         mores.append(data[i]['pin'])
# print(len(matched))
# print(len(mores))

""""""

# from y_example_read_json import *
# data = read_json("concert_zh.json")
#
# with open('concert_pin_postid.txt', 'r', encoding='utf-8') as f:
#     lines = f.readlines()
# pins = [line.split('|||')[1].replace('\n', '') for line in lines]
#
# print(len(data))  # 298
# print(len(pins))  # 477
# print('---')
#
# matched = set()  # 使用集合來存儲已匹配的pin
# mores = []
# for item in data:
#     if item['pin'] in pins:
#         matched.add(item['pin'])  # 只有當pin不在matched集合中時才添加
#     else:
#         mores.append(item['pin'])
# print(len(matched))  # 應該小於或等於298，如果沒有重複的pin
# print(len(mores))

""""""

# from y_example_read_json import *
# data = read_json("concert_zh.json")
#
# with open('concert_pin_postid.txt', 'r', encoding='utf-8') as f:
#     lines = f.readlines()
# pins = [line.split('|||')[1].replace('\n', '') for line in lines]
#
# data_pins = set(item['pin'] for item in data)  # 从data中收集所有pin
# pins_set = set(pins)  # 将pins列表转换为集合以去除重复
#
# matched = data_pins & pins_set  # 使用集合交集找到匹配的pins
# mores = pins_set - data_pins  # 使用集合差集找到只在pins中的pins
#
# print(len(data))
# print(len(pins))
# print('---')
# print(len(matched))
# print(len(mores))
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
        "concert_5_8_20.json"
    ]
""""""
for i in range(len(json_list)):
    data = read_json(json_list[i])
    print(f"{len(data)} -> ", end='')
    data = [item for item in data if item['tit'] != '']
    print(f"{len(data)}")
    with open(json_list[i], 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print('---')
""""""
# data = read_json(json_list[0])
# print(len(data))
# data = [item for item in data if item['tit'] != '']
# print(len(data))
