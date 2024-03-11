# import jieba
#
# # 加载自定义词典
# jieba.load_userdict("user_dict.txt")
#
# test_word = 'Taylor Swift'
# text = jieba.lcut(test_word)
# print(text)
#
# # # 分词
# # text = "taylor swift是一位知名的歌手。"
# # seg_list = jieba.lcut(text, cut_all=True)
# #
# # # 遍历分词结果，如果包含自定义词汇，则替换为自定义词汇
# # result = []
# # for word in seg_list:
# #     if word in ["taylor swift"]:
# #         result.append(word)
# #     else:
# #         result.extend(jieba.lcut(word))
# #
# # # 输出分词结果
# # print(result)

import jieba

# 載入自定義詞典
jieba.load_userdict("user_dict.txt")

# 要斷詞的文本
text = "Eric Nam"

# 斷詞並確認是否包含自定義詞彙
result = jieba.cut(text)
word_list = list(result)
print(word_list)