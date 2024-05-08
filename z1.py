with open('concert_pin_postid.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

pin = "https://ticketplus.com.tw/activity/8455304be5b4ffef154340fd40d9dfa71"
for index, line in enumerate(lines):
    line_pin = line.split('|||')[1].replace('\n', '')
    if pin == line_pin:
        lines.pop(index)

with open('concert_pin_postid1.txt', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print(lines)
print(len(lines))
