# from fuzzywuzzy import fuzz
#
# sim = fuzz.ratio('寶兒', 'BoA 寶兒')
# print(sim)

with open('japanese_link.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for line in lines:
    line = line.replace('\n', '')
    print(line[line.index('|||')+3:])