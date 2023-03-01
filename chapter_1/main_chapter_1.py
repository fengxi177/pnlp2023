# -*- coding = utf-8 -*-

"""
    author:fengxi
    time:2023/2/17

    project name:pnlp2023
    file name:main.py
    function:
        chapter_1主方法：
            数据加载、预处理
            文本（短评）数据可视化
            数据分析与可视化
"""

import jieba
import pandas as pd
from preprocessing import load_stopwords
from visualization_comments import generate_wordcloud, get_cooccurrence_graph, generate_celebrity_graph
from visualization_data import analysis_location


# 加载自定义词典
jieba.load_userdict("./dict/custom_dictionary.txt")


def load_pre_data(filename):
    """
        加载全部数据
        对评论进行预处理
    :param filename:
    :return:
    """
    # === 加载全部数据
    df = pd.read_csv(filename, encoding="utf-8")

    # 提取每一列数据
    user_name = df["用户名"].values.tolist()
    video_status = df["电视剧观看状态"].values.tolist()
    comment_score = df["评论分数"].values.tolist()
    comment_level = df["评论等级"].values.tolist()
    comment_time = df["评论时间"].values.tolist()
    comment_location = df["评论位置"].values.tolist()
    comment_vote_count = df["评论点赞数"].values.tolist()
    comment_content = df["评论"].values.tolist()

    # === 对评论进行预处理
    # 加载停用词词典
    stopwords = load_stopwords()

    comment_seg_list = []  # 分词后的评论
    for comment in comment_content:
        # 简单预处理
        comment = comment.replace("\r", "")
        # 分词
        comment_seg = []
        for words in jieba.lcut(comment):
            # 去停用词（包括中文标点符号）
            if words in stopwords:
                continue
            # 过滤单个字符的词
            if len(words) < 2:
                continue
            # 过滤数字
            if words.isdigit():
                continue
            comment_seg.append(words)
        comment_seg_list.append(comment_seg)

    return user_name, video_status, comment_score, comment_level, comment_time, \
        comment_location, comment_vote_count, comment_seg_list


def main():
    """
        数据分析主流程：
            1、短评分析与可视化：词云图、词共现关系图、人物关系图谱
            2、数据分析与可视化
    :return:
    """
    # 加载和预处理数据
    user_name, video_status, comment_score, comment_level, comment_time, comment_location, \
    comment_vote_count, comment_content = load_pre_data("./data/狂飙.csv")

    # 生成词云图
    generate_wordcloud(comment_content)

    # 获得词共现关系图
    get_cooccurrence_graph(comment_content)

    # 构建人物关系图谱
    generate_celebrity_graph()

    # 统计分析评论位置分布情况
    analysis_location(comment_location)


if __name__ == '__main__':
    # 主方法
    main()
    print("数据分析完成...")

    pass