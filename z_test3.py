import re

text = '這是一段文本\n \n \n \n \n哈哈哈'
print(text)
print()
text = re.sub(r'\s*\n+\s*', '\n', text)
print(f'{text}')