from read_json_function import *
from get_concert_info import *
import re
import json
import pandas as pd
import matplotlib.pyplot as plt
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
    "concert_jsons/concert_5_12_21.json",
    "concert_jsons/concert_5_13_14.json",
    "concert_jsons/concert_5_13_15.json",
    "concert_jsons/concert_5_13_17.json",
    "concert_jsons/concert_5_13_18.json",
    "concert_jsons/concert_5_13_19.json",
    "concert_jsons/concert_5_14_17.json",
    "concert_jsons/concert_5_14_4.json",
    "concert_jsons/concert_5_15_1.json",
    "concert_jsons/concert_5_15_19.json",
    "concert_jsons/concert_5_16_20.json",
    "concert_jsons/concert_5_21_20.json",
    "concert_jsons/concert_5_22_20.json",
    "concert_jsons/concert_5_23_20.json",
    "concert_jsons/concert_5_28_20.json",
    "concert_jsons/concert_5_29_20.json",
    "concert_jsons/concert_6_4_23.json",
]


# for i in range(len(json_list)):
#     get_city_from_stadium(json_list[i])
# def single():
#     data = read_json(json_list[0])
#     era_count = 0
#     indievox_count = 0
#     kktix_count = 0
#     livenation_count = 0
#     ticketplus_count = 0
#     for i in range(len(data)):
#         if data[i]['web'] == 'era':
#             era_count += 1
#         elif data[i]['web'] == 'Indievox':
#             indievox_count += 1
#         elif data[i]['web'] == 'KKTIX':
#             kktix_count += 1
#         elif data[i]['web'] == 'Live Nation':
#             livenation_count += 1
#         elif data[i]['web'] == 'Ticket Plus':
#             ticketplus_count += 1
#     print(f"Era\t\t\t: {era_count} / {len(data)} = {round((era_count / len(data)) * 100, 2)}%")
#     print(f"Indievox\t: {indievox_count} / {len(data)} = {round((indievox_count / len(data)) * 100, 2)}%")
#     print(f"KKTIX\t\t: {kktix_count} / {len(data)} = {round((kktix_count / len(data)) * 100, 2)}%")
#     print(f"Live Nation\t: {livenation_count} / {len(data)} = {round((livenation_count / len(data)) * 100, 2)}%")
#     print(f"Ticket Plus\t: {ticketplus_count} / {len(data)} = {round((ticketplus_count / len(data)) * 100, 2)}%")


def concert_number():
    era_count = 0
    indievox_count = 0
    kktix_count = 0
    livenation_count = 0
    ticketplus_count = 0
    all_count = 0
    for json_file in json_list:
        data = read_json(json_file)
        all_count += len(data)
        for i in range(len(data)):
            if data[i]['web'] == 'era':
                era_count += 1
            elif data[i]['web'] == 'Indievox':
                indievox_count += 1
            elif data[i]['web'] == 'KKTIX':
                kktix_count += 1
            elif data[i]['web'] == 'Live Nation':
                livenation_count += 1
            elif data[i]['web'] == 'Ticket Plus':
                ticketplus_count += 1

    print(f"Era\t\t\t: {era_count} / {all_count} = {round((era_count / all_count) * 100, 2)}%")
    print(f"Indievox\t: {indievox_count} / {all_count} = {round((indievox_count / all_count) * 100, 2)}%")
    print(f"KKTIX\t\t: {kktix_count} / {all_count} = {round((kktix_count / all_count) * 100, 2)}%")
    print(f"Live Nation\t: {livenation_count} / {all_count} = {round((livenation_count / all_count) * 100, 2)}%")
    print(f"Ticket Plus\t: {ticketplus_count} / {all_count} = {round((ticketplus_count / all_count) * 100, 2)}%")


# all()
# cities = []
# for json_file in json_list:
#     data = read_json(json_file)
#     for i in range(len(data)):
#         # print(data[i]['cit'])
#         if data[i]['cit'] != "":
#             cities.append(data[i]['cit'])
# cities = list(set(cities))
# print(cities)
# zh_cities = ["台北", "新北", "桃園", "台中", "台南", "高雄", "基隆", "新竹", "苗栗", "彰化", "南投", "雲林",
#              "嘉義", "屏東", "宜蘭", "花蓮", "台東", "金門", "澎湖", "連江"]
# has_cities = ['新北', '台中', '台南', '新竹', '花蓮', '高雄', '桃園', '宜蘭', '基隆', '嘉義', '台北', '屏東', '台東']
# none_cities = ['苗栗', '彰化', '南投', '雲林', '金門', '澎湖', '連江']
# a = [b for b in zh_cities if b not in has_cities]
# print(a)
# en_cities = ["Taoyuan", "Taichung", "Tainan", "Kaohsiung", "Keelung", "Hsinchu", "Miaoli",
#              "Changhua", "Nantou", "Yunlin", "Chiayi", "Pingtung", "Yilan", "Hualien", "Taitung", "Kinmen", "Penghu",
#              "Lienchiang"]

def concert_cities():
    miaoli_count = 0
    changhua_count = 0
    nantou_count = 0
    yunlin_count = 0
    kinmen_count = 0
    penghu_count = 0
    lienchiang_count = 0
    new_taipei_count = 0
    taichung_count = 0
    taitung_count = 0
    pingtung_count = 0
    taipei_count = 0
    chiayi_count = 0
    keelung_count = 0
    yilan_count = 0
    taoyuan_count = 0
    kaohsiung_count = 0
    hualien_count = 0
    hsinchu_count = 0
    tainan_count = 0
    unknown_count = 0
    all_count = 0
    for json_file in json_list:
        data = read_json(json_file)
        all_count += len(data)
        for i in range(len(data)):
            if data[i]['cit'] != "":
                if data[i]['cit'] == '新北':
                    new_taipei_count += 1
                elif data[i]['cit'] == '台中':
                    taichung_count += 1
                elif data[i]['cit'] == '台東':
                    taitung_count += 1
                elif data[i]['cit'] == '屏東':
                    pingtung_count += 1
                elif data[i]['cit'] == '台北':
                    taipei_count += 1
                elif data[i]['cit'] == '嘉義':
                    chiayi_count += 1
                elif data[i]['cit'] == '基隆':
                    keelung_count += 1
                elif data[i]['cit'] == '宜蘭':
                    yilan_count += 1
                elif data[i]['cit'] == '桃園':
                    taoyuan_count += 1
                elif data[i]['cit'] == '高雄':
                    kaohsiung_count += 1
                elif data[i]['cit'] == '花蓮':
                    hualien_count += 1
                elif data[i]['cit'] == '新竹':
                    hsinchu_count += 1
                elif data[i]['cit'] == '台南':
                    tainan_count += 1
                else:
                    unknown_count += 1

    print(f"Taipei\t\t: {taipei_count} / {all_count} = {round((taipei_count / all_count) * 100, 2)}%")
    print(f"Taichung\t: {taichung_count} / {all_count} = {round((taichung_count / all_count) * 100, 2)}%")
    print(f"Kaosiung\t: {kaohsiung_count} / {all_count} = {round((kaohsiung_count / all_count) * 100, 2)}%")
    print(f"New Taipei\t: {new_taipei_count} / {all_count} = {round((new_taipei_count / all_count) * 100, 2)}%")
    print(f"Taoyuan\t\t: {taoyuan_count} / {all_count} = {round((taoyuan_count / all_count) * 100, 2)}%")
    print(f"Keelung\t\t: {keelung_count} / {all_count} = {round((keelung_count / all_count) * 100, 2)}%")
    print(f"Hsinchu\t\t: {hsinchu_count} / {all_count} = {round((hsinchu_count / all_count) * 100, 2)}%")
    print(f"Tainan\t\t: {tainan_count} / {all_count} = {round((tainan_count / all_count) * 100, 2)}%")
    print(f"Taitung\t\t: {taitung_count} / {all_count} = {round((taitung_count / all_count) * 100, 2)}%")
    print(f"Pingtung\t: {pingtung_count} / {all_count} = {round((pingtung_count / all_count) * 100, 2)}%")
    print(f"Chiayi\t\t: {chiayi_count} / {all_count} = {round((chiayi_count / all_count) * 100, 2)}%")
    print(f"Yilan\t\t: {yilan_count} / {all_count} = {round((yilan_count / all_count) * 100, 2)}%")
    print(f"Hualien\t\t: {hualien_count} / {all_count} = {round((hualien_count / all_count) * 100, 2)}%")
    print(f"Miaoli\t\t: {miaoli_count} / {all_count} = {round((miaoli_count / all_count) * 100, 2)}%")
    print(f"Changhua\t: {changhua_count} / {all_count} = {round((changhua_count / all_count) * 100, 2)}%")
    print(f"Nantou\t\t: {nantou_count} / {all_count} = {round((nantou_count / all_count) * 100, 2)}%")
    print(f"Yunlin\t\t: {yunlin_count} / {all_count} = {round((yunlin_count / all_count) * 100, 2)}%")
    print(f"Kinmen\t\t: {kinmen_count} / {all_count} = {round((kinmen_count / all_count) * 100, 2)}%")
    print(f"Penghu\t\t: {penghu_count} / {all_count} = {round((penghu_count / all_count) * 100, 2)}%")
    print(f"Lien Chiang\t: {lienchiang_count} / {all_count} = {round((lienchiang_count / all_count) * 100, 2)}%")
    print(f"Unknown\t\t: {unknown_count} / {all_count} = {round((unknown_count / all_count) * 100, 2)}%")


def concert_ticketing_time():
    morning_count = 0
    noon_count = 0
    afternoon_count = 0
    night_count = 0
    all_count = 0
    unknown_count = 0
    for json_file in json_list:
        data = read_json(json_file)
        all_count += len(data)
        for i in range(len(data)):
            for j in range(len(data[i]['sdt'])):
                ticketing_time = re.findall(r"\d{1,2}:\d{1,2}", data[i]['sdt'][j])
                # if ticketing_time:
                # hour = int(ticketing_time[0].split(":"))
                hour = int(ticketing_time[0].split(":")[0])
                if hour > 6 and hour < 12:
                    morning_count += 1
                elif hour == 12:
                    noon_count += 1
                elif hour > 12 and hour < 18:
                    afternoon_count += 1
                elif hour > 18:
                    night_count += 1
                else:
                    unknown_count += 1
    print(f"Morning\t\t: {morning_count} / {all_count} = {round((morning_count / all_count) * 100, 2)}%")
    print(f"Noon\t\t: {noon_count} / {all_count} = {round((noon_count / all_count) * 100, 2)}%")
    print(f"Afternoon\t: {afternoon_count} / {all_count} = {round((afternoon_count / all_count) * 100, 2)}%")
    print(f"Night\t\t: {night_count} / {all_count} = {round((night_count / all_count) * 100, 2)}%")
    print(f"Unknown\t\t: {unknown_count} / {all_count} = {round((unknown_count / all_count) * 100, 2)}%")

def concert_price():
    data = []

    for file in json_list:
        with open(file, 'r', encoding='utf-8') as f:
            data.extend(json.load(f))

    # 提取票價數據
    price_data = []
    for item in data:
        if 'prc' in item and item['prc']:
            for price in item['prc']:
                price_data.append({'website': item['web'], 'price': price})

    # 創建 DataFrame
    df = pd.DataFrame(price_data)

    # 將 price 列轉換為數字類型，忽略非數字值
    df['price'] = pd.to_numeric(df['price'], errors='coerce')

    # 移除包含 NaN 的行
    df = df.dropna(subset=['price'])

    # 確保 price 列為整數
    df['price'] = df['price'].astype(int)

    # 計算每個網站的票價範圍和中位數
    summary = df.groupby('website')['price'].agg(['min', 'max', 'median']).reset_index()

    # 繪製簡化的條形圖
    fig, ax = plt.subplots(figsize=(12, 8))
    colors = ['skyblue', 'lightgreen', 'lightcoral', 'lightsalmon', 'lightpink']

    # 繪製每個網站的票價範圍條形
    bars = ax.bar(summary['website'], summary['max'] - summary['min'], bottom=summary['min'], color=colors,
                  edgecolor='grey')

    # 在條形圖中標記中位數
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax.plot([i, i], [summary['min'][i], summary['max'][i]], color='black', marker='_', markersize=20,
                markeredgewidth=2)
        ax.text(i, summary['median'][i], f"{summary['median'][i]}", ha='center', va='bottom', color='black',
                fontsize=12)

    # 添加標題和標籤
    ax.set_title('Simplified Ticket Price Range and Median by Website', fontsize=16)
    ax.set_xlabel('Website', fontsize=14)
    ax.set_ylabel('Price (TWD)', fontsize=14)
    ax.set_ylim(0, summary['max'].max() + 500)

    # 添加說明
    plt.text(-0.5, summary['max'].max() + 300, "Each bar represents the price range of a website", fontsize=12)
    plt.text(-0.5, summary['max'].max() + 100, "The black line indicates the median price", fontsize=12)

    # 顯示圖表
    plt.show()


# concert_number()
# print('---')
# concert_cities()
# print('---')
concert_ticketing_time()
print('---')

