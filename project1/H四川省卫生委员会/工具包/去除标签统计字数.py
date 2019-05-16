# coding:utf-8
import re
def word_count(content):
    content = re.sub('<[^>]*>', '', content)
    content = re.sub(" ", '', content)
    word_num = len(content)
    return word_num