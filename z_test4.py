a = ['TICC', '小巨蛋']

a_str = ''
for i in range(len(a)):
    a_str += a[i] + ' / '
print(a_str)
a_str = a_str[:-3]
print(a_str)