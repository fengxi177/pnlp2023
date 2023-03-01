# -*- coding = utf-8 -*-

"""
    author:fengxi
    time:2023/2/17

    project name:pnlp2023
    file name:preprocessing.py
    function:
        文本数据预处理
"""

from datetime import datetime
from zhon.hanzi import punctuation


def load_stopwords():
    """
        加载停用词词典，主要词典来源：https://github.com/goto456/stopwords
        标点符号来源：from zhon.hanzi import punctuation
    :return:
    """
    stopwords = []
    with open("./dict/stopwords.txt", "r", encoding="utf-8") as fr:
        for line in fr.readlines():
            line = line.strip()
            stopwords.append(line)

    # 中文标点符号
    punc_list = list(punctuation)

    # 全部停用词
    stopwords = punc_list + stopwords

    return stopwords


def parse_time(text):
    """
        时间字符串解析
    :param text: eg: '2023-01-15 12:02:00'
    :return:
    """
    time_format = datetime.strptime(text, "%Y-%m-%d %H:%M:%S")
    # 提取具体日期、时间
    year = time_format.year
    month = time_format.month
    day = time_format.day
    hour = time_format.hour
    # minute = time_format.minute
    # second = time_format.second

    result = {"year": year, "month": month, "day": day, "hour": hour}

    return result
