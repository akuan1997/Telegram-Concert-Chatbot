import json
import re

with open('concert_data_new_zh.json', 'r', encoding='utf-8') as f:
    new_data = json.load(f)

with open('concert_data_old_zh.json', 'r', encoding='utf-8') as f:
    old_data = json.load(f)

with open('concert_zh.json', 'r', encoding='utf-8') as f:
    all_data = json.load(f)


# Function to display new concert data that is not in old data
def show_new_but_old(new_but_old_pins):
    print('\n--- new but old ---\n')
    for pin in new_but_old_pins:
        for i in range(len(new_data)):
            if new_data[i]['pin'] == pin:  # Check if the pin from new data matches the pin from the list
                print(new_data[i]['tit'])  # Print the title of the concert
                print(new_data[i]['url'])  # Print the URL of the concert
    print('\n--- new but old ---\n')


# Function to display old concert data that is not in new data
def show_old_but_new(old_but_new_pins):
    print('\n--- old but new ---\n')
    for pin in old_but_new_pins:
        for i in range(len(old_data)):
            if old_data[i]['pin'] == pin:  # Check if the pin from old data matches the pin from the list
                print(old_data[i]['tit'])  # Print the title of the concert
                print(old_data[i]['url'])  # Print the URL of the concert
    print('\n--- old but new ---\n')


# Function to remove concerts from all_data that are no longer active
def old_concert_delete(old_but_new_pins, all_data):
    print(f'all_data ({len(all_data)}) - old_but_new_pins ({len(old_but_new_pins)}) = ', end='')
    # print(f'len(delete_pins) = {len(old_but_new_pins)}')
    # print(f'len(all_data) = {len(all_data)}')
    all_data_filtered = [data for data in all_data if
                         data['pin'] not in old_but_new_pins]  # Filter out deleted concerts
    all_data.clear()  # Clear existing data
    all_data.extend(all_data_filtered)  # Update all_data with filtered list
    print(f'all_data ({len(all_data)})')


# Function to find the index of a concert in all_data using its pin
def get_pin_index_in_all_data(pin, all_data):
    index = -1  # Default index
    for i in range(len(all_data)):
        if all_data[i]['pin'] == pin:
            index = i  # Update index if pin is found
            break
    return index


# Function to check and update concert information between new and old data sets
def check_each_info(new_data, old_data, all_data):
    # Iterate over each item in new_data
    for i in range(len(new_data)):
        # Iterate over each item in old_data
        for j in range(len(old_data)):
            # Check if the current items in new_data and old_data have the same 'pin' value
            if new_data[i]['pin'] == old_data[j]['pin']:
                pin = old_data[j]['pin']  # Retrieve the 'pin' code, which is the same in both new and old data
                pin_index_in_all_data = get_pin_index_in_all_data(pin,
                                                                  all_data)  # Find the index of this 'pin' in all_data

                # Special case handling for KKTIX platform
                if new_data[i]['web'] == 'KKTIX':
                    # If the 'int' field is different in new and old data, check further
                    if new_data[i]['int'] != old_data[j]['int']:
                        # If new data indicates an added show and old data doesn't, notify the user
                        if ('加場' in new_data[i]['int'] or '加開' in new_data[i]['int']) and '加場' not in old_data[j][
                            'int']:
                            print('通知使用者')
                            print(f"new_data[i]['tit'] = {new_data[i]['tit']}")
                            print(new_data[i]['url'])
                            all_data[pin_index_in_all_data]['int'] = new_data[i]['int']  # Update 'int' in all_data
                else:
                    # replace "\n \n" or "\n\n" to "\n"
                    new_data[i]['int'] = re.sub(r'\s*\n+\s*', '\n', new_data[i]['int'])
                    old_data[j]['int'] = re.sub(r'\s*\n+\s*', '\n', old_data[j]['int'])

                    ''''''

                    # For other platforms, check and print changes in 'sdt', 'prc', 'pdt', and 'loc'
                    if new_data[i]['sdt'] != old_data[j]['sdt']:
                        if len(new_data[i]['sdt']) > len(old_data[j]['sdt']):
                            print(f"{new_data[i]['tit']}")
                            print(f"新增sdt\n{new_data[i]['sdt']} != {old_data[j]['sdt']}\n{new_data[i]['url']}\n---")
                            all_data[pin_index_in_all_data]['sdt'] = new_data[i]['sdt']
                        else:
                            print(f"{new_data[i]['tit']}")
                            print(
                                f"sdt減少 / {old_data[j]['sdt']} -> {new_data[i]['sdt']} / 不修改all_data\n{new_data[i]['url']}\n---")

                    if new_data[i]['prc'] != old_data[j]['prc']:
                        if len(new_data[i]['prc']) > len(old_data[j]['prc']):
                            print(f"{new_data[i]['tit']}")
                            print(f"新增prc\n{new_data[i]['prc']} != {old_data[j]['prc']}\n{new_data[i]['url']}\n---")
                            all_data[pin_index_in_all_data]['prc'] = new_data[i]['prc']
                        else:
                            print(f"{new_data[i]['tit']}")
                            print(
                                f"prc減少 / {old_data[j]['prc']} -> {new_data[i]['prc']} / 不修改all_data\n{new_data[i]['url']}\n---")

                    if new_data[i]['pdt'] != old_data[j]['pdt']:
                        if len(new_data[i]['pdt']) > len(old_data[j]['pdt']):
                            print(f"{new_data[i]['tit']}")
                            print(new_data[i], old_data[j])
                            print(f"新增pdt\n{new_data[i]['pdt']} != {old_data[j]['pdt']}\n{new_data[i]['url']}\n---")
                            all_data[pin_index_in_all_data]['pdt'] = new_data[i]['pdt']
                        else:
                            print(f"{new_data[i]['tit']}")
                            print(
                                f"pdt減少 / {old_data[j]['pdt']} -> {new_data[i]['pdt']}\n / 不修改all_data{new_data[i]['url']}\n---")

                    if new_data[i]['loc'] != old_data[j]['loc']:
                        if len(new_data[i]['loc']) > len(old_data[j]['loc']):
                            print(f"{new_data[i]['tit']}")
                            print(f"新增loc\n{new_data[i]['loc']} != {old_data[j]['loc']}\n{new_data[i]['url']}\n---")
                            all_data[pin_index_in_all_data]['loc'] = new_data[i]['loc']
                        else:
                            print(f"{new_data[i]['tit']}")
                            print(
                                f"loc減少 / {old_data[j]['loc']} -> {new_data[i]['loc']}\n / 不修改all_data{new_data[i]['url']}\n---")

                    # Check 'int' field again for changes other than KKTIX
                    if new_data[i]['int'] != old_data[j]['int']:
                        print(new_data[i]['tit'])
                        print(f'{new_data[i]["web"]} int 不同')
                        if len(new_data[i]['int']) > len(old_data[j]['int']):
                            print('新增了一些文字，', end='')
                            # print(repr(new_data[i]['int']))
                            # print(repr(old_data[j]['int']))
                            if '加場' in new_data[i]['int'] or '加開' in new_data[i]['int']:
                                print('而且是有關於加場的，通知使用者\n---')
                            else:
                                print('但不是有關於加場 / 加開方面的資訊\n---')
                        else:
                            print('新資料減少了一些文字，不需要更改\n---')

                        all_data[pin_index_in_all_data]['int'] = new_data[i]['int']  # Update 'int' in all_data

                # Potential code to write the updated all_data to a JSON file
                # with open('concert_zh.json', 'w', encoding='utf-8') as file:
                #     json.dump(all_data, file, indent=4, ensure_ascii=False)


# def print_details(new_data_item, old_data_item):
#     """Helper function to print differences in data fields."""
#     print(f"title = {old_data_item['tit']}")
#     print(f"new_data[i]['sdt'] = {new_data_item['sdt']}")
#     print(f"old_data[j]['sdt'] = {old_data_item['sdt']}")
#     print(f"web = {new_data_item['web']}")
#     print(f"url = {new_data_item['url']}")
#     print('---------')


# Function to add new concerts to all_data
def new_concerts(new_but_old_pins, new_data, all_data):
    print(f'all_data ({len(all_data)}) + new_but_old_pins ({len(new_but_old_pins)}) = ', end='')
    new_data_filtered = [data for data in new_data if data['pin'] in new_but_old_pins]  # Filter new concerts by pin
    all_data.extend(new_data_filtered)  # Add new concerts to all_data
    print(f'all_data ({len(all_data)})')


# Main function to check and update concert data
def check_concerts():
    pins_new = [entry['pin'] for entry in new_data]  # List of pins in new data
    pins_old = [entry['pin'] for entry in old_data]  # List of pins in old data
    new_but_old_pins = [pin for pin in pins_new if pin not in pins_old]  # Find new concerts
    old_but_new_pins = [pin for pin in pins_old if pin not in pins_new]  # Find deleted concerts
    check_each_info(new_data, old_data, all_data)  # Check and update concert info
