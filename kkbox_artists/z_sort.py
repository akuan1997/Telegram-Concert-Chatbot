before = 'taiwanese.txt'
after = 'taiwanese_sorted.txt'

with open(before, 'r', encoding='utf-8') as f:
    lines = f.readlines()

lines = [line for line in lines if
         ',' not in line and ' X ' not in line and '原聲帶' not in line and '+' not in line and '×' not in line and '、' not in line and '/' not in line and '&' not in line and '翻唱' not in line and '主題曲' not in line and '韓劇' not in line and '獻聲' not in line and ' x ' not in line and '成名曲' not in line and '＆' not in line]

with open(after, 'w', encoding='utf-8') as f:
    f.write(''.join(lines))
