def current_one():
    # 首先讀取a.txt的所有數據
    with open('z_test2_a.txt', 'r', encoding='utf-8') as f:
        a_datas = f.readlines()

    # 處理每條數據
    for i, a_data in enumerate(a_datas):
        a_data = a_data.strip()  # 移除換行符

        # do something with a_data

        # 寫入數據到b.txt
        with open('z_test2_b.txt', 'a', encoding='utf-8') as f:
            f.write(a_data + '\n')

        # 更新a.txt：寫入還沒處理的數據
        with open('z_test2_a.txt', 'w', encoding='utf-8') as f:
            f.writelines(a_datas[i + 1:])

        # 驗證 ---------------------------

        with open('z_test2_a.txt', 'r', encoding='utf-8') as f:
            current_a = f.readlines()
        with open('z_test2_b.txt', 'r', encoding='utf-8') as f:
            current_b = f.readlines()
        print(current_a)
        print(current_b)
        print('---------------------------')


def try_one():
    # 首先讀取a.txt的所有數據
    with open('z_test2_a.txt', 'r', encoding='utf-8') as f:
        waiting_categories = f.readlines()

    # 處理每條數據
    for i, waiting_category in enumerate(waiting_categories):
        waiting_category = waiting_category.strip()  # 移除換行符

        with open('z_test2_b.txt', 'r', encoding='utf-8') as f:
            processed_categories = f.readlines()
        processed_categories = [processed_category.replace('\n', '') for processed_category in processed_categories]

        if waiting_category not in processed_categories:
            # do something
            print('write data!')
            # 寫入數據到b.txt
            with open('z_test2_b.txt', 'a', encoding='utf-8') as f:
                f.write(waiting_category + '\n')
            # 更新a.txt：寫入還沒處理的數據
            with open('z_test2_a.txt', 'w', encoding='utf-8') as f:
                f.writelines(waiting_categories[i + 1:])
        else:
            print('已經完成這個頁面了!')

        # 驗證 ---------------------------

        with open('z_test2_a.txt', 'r', encoding='utf-8') as f:
            current_a = f.readlines()
        with open('z_test2_b.txt', 'r', encoding='utf-8') as f:
            current_b = f.readlines()
        print(current_a)
        print(current_b)
        print('---------------------------')


# current_one()
try_one()
