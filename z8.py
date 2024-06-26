# txt = f"""
# Usage Instructions
# Inquire by artist name, genre, city, or specific time
#
# Example inputs:
# "Taylor Swift"
# "Rap"
# "Taipei"
# "Tomorrow"
# Specify multiple criteria simultaneously
#
# Example inputs:
# "Taylor Swift concerts in Taipei"
# "Post Malone, next month"
# "Hip-Hop, this week, and in Tainan city"
# Sample Queries
# Inquire about Jazz concerts in Taipei
#
# Query details:
# Keyword: Jazz
# City: Taipei
# Check if Post Malone has any concerts in Taipei this year
#
# Query details:
# Keyword: Post Malone
# Date: this year
# City: Taipei
# Get information on R&B festivals happening in Kaohsiung next month
#
# Query details:
# Keyword: R&B
# City: Kaohsiung
# Date: next month
# Find out which concerts are open for sale tomorrow
#
# Query details:
# Date: tomorrow
# """
# print(txt)

# matched_tags = ['city']
# all_tags = ['keyword', 'date', 'city']
# further_search_tags = [tag for tag in all_tags if tag not in matched_tags]
# print(f"further_search_tags = {further_search_tags}")
# print(f"You can refine your search by specifying more details: {', '.join(further_search_tags)}")

list1 = [1, 2, 3, 4]
list2 = [1, 3, 4, 5, 6]
list3 = [1, 6, 7, 8, 9]
list4 = [1, 9, 10, 11]

# 使用集合操作取并集
union_set = set(list1) & set(list2) & set(list3) & set(list4)

# 转换回列表
union_list = list(union_set)

# 打印结果
print(f"The union of the four lists is: {union_list}")