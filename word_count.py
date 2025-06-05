import re

sentence = input("请输入一个包含标点符号的英文句子：")
words = [word for word in re.split(r'[^a-zA-Z]+', sentence) if word]
print(len(words))
