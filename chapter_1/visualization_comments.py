# -*- coding = utf-8 -*-

"""
    author:fengxi
    time:2023/2/17

    project name:pnlp2023
    file name:analysis_visualization.py
    function:
    文本分析与可视化
        (1)生成词云图
        (2)获得词共现关系图
        (3)构建人物关系图谱
"""

import itertools
import pandas as pd
import pyecharts.options as opts
from pyecharts.globals import ThemeType
from pyecharts.charts import WordCloud
from pyecharts.charts import Graph
from collections import Counter


def generate_wordcloud(data_list):
    """
        生成词云图
    :param data_list: 分词后的评论list
    :return:
    """

    # 数据格式转换
    words_list = [word for seg_list in data_list for word in seg_list]

    # 转换为绘制词云图格式
    comment_words_dict = dict(Counter(words_list))
    data_pair = [(words, freq) for words, freq in comment_words_dict.items()]

    wordcloud = WordCloud()
    wordcloud.add("",
                  data_pair,
                  word_gap=2,
                  # mask_image=mask_image,  # 背景图设置
                  word_size_range=[10, 50])
    wordcloud.render("./result/词云图.html")
    print("词云图绘制结束，保存路径为：./result/词云图.html")


def get_cooccurrence_graph(data_list):
    """
        可视化top2000组词共现关系图
    :param data_list:  分词后的评论list
    :return:
    """

    co_words_list = []  # 共现词组
    for data in data_list:
        # 获得共现词组合
        co_words = list(itertools.combinations(data, 2))
        co_words_list += ["\t".join(word) for word in co_words]

    # 统计共现频率作为权重
    words_freq_dict = dict(Counter(co_words_list))
    # 排序
    sorted_words_freq = sorted(words_freq_dict.items(), key=lambda x: x[1], reverse=True)

    # 获取top 2000组
    result = []
    nodes = []
    links = []
    nodes_list = []  # 避免节点重复
    for words, freq in sorted_words_freq[:2000]:
        start_w, end_w = words.split("\t")
        result.append([start_w, end_w, freq])

        # 添加节点和关系
        if start_w not in nodes_list:
            nodes_list.append(start_w)
            nodes.append(opts.GraphNode(name=start_w, symbol_size=freq))
        if end_w not in nodes_list:
            nodes_list.append(end_w)
            nodes.append(opts.GraphNode(name=end_w, symbol_size=freq))
        links.append(opts.GraphLink(source=start_w, target=end_w))

    c = (
        Graph(opts.InitOpts(width="1500px", height="1000px"))
        .add("",
             nodes,
             links,
             linestyle_opts=opts.LineStyleOpts(curve=0.6),
             repulsion=4000)
        .set_global_opts(title_opts=opts.TitleOpts(title="短评：词共现图"))
        .render("./result/词共现graph.html")
    )

    # 保存共现矩阵
    columns_list = ["source", "target", "weight"]
    df = pd.DataFrame(result, columns=columns_list)
    df.to_csv("./result/top2000词共现关系.csv", index=False, encoding="utf-8-sig")
    print("top2000组词共现关系图绘制结束，保存路径为：./result/词共现graph.html")


def generate_celebrity_graph():
    """
        构建演职员关系图谱
    :return:
    """
    df = pd.read_csv("./data/狂飙演职员信息表.csv")
    data = df.values.tolist()

    # 转换格式
    nodes = []
    links = []
    nodes_name = []

    symbolSize_dict = {"姓名": 30, "角色": 20, "饰演人物": 20, "代表作": 20}
    categories = [{"name": x} for x in symbolSize_dict.keys()]

    for row in data:
        # 姓名、角色(";"分割多个)、饰演人物(可能为空)、代表作(";"分割多个)
        name, role, role_to_play, works = row
        role_list = role.split(";")
        works_list = works.split(";")

        if name not in nodes_name:
            nodes_name.append(name)
            # 一个节点
            node = {
                "name": name,
                "symbolSize": symbolSize_dict["姓名"],
                "category": "姓名",
            }
            nodes.append(node)

        for role_temp in role_list:
            if role_temp not in nodes_name:
                nodes_name.append(role_temp)
                node = {
                    "name": role_temp,
                    "symbolSize": symbolSize_dict["角色"],
                    "category": "角色",
                }
                nodes.append(node)

            link = {
                "source": name,
                "target": role_temp
            }
            links.append(link)

            if role_temp == "演员":
                if role_to_play not in nodes_name:
                    nodes_name.append(role_to_play)
                    node = {
                        "name": role_to_play,
                        "symbolSize": symbolSize_dict["饰演人物"],
                        "category": "饰演人物",
                    }
                    nodes.append(node)

                link = {
                    "source": name,
                    "target": role_to_play
                }
                links.append(link)

        for works_temp in works_list:
            if works_temp not in nodes_name:
                nodes_name.append(works_temp)
                if works_temp == "狂飙":
                    node = {
                        "name": works_temp,
                        "symbolSize": 50,  # 特别设置
                        "category": "代表作",
                    }
                else:
                    node = {
                        "name": works_temp,
                        "symbolSize": symbolSize_dict["代表作"],
                        "category": "代表作",
                    }
                nodes.append(node)

            link = {
                "source": name,
                "target": works_temp
            }
            links.append(link)

    c = (
        Graph(init_opts=opts.InitOpts(theme=ThemeType.CHALK, width="1500px", height="1000px"))
        .add(
            "",
            nodes,
            links,
            categories,
            repulsion=1000,
            linestyle_opts=opts.LineStyleOpts(curve=0.6),
        )
        .set_global_opts(
            legend_opts=opts.LegendOpts(pos_left=100, pos_top=350, orient="vertical"),
            title_opts=opts.TitleOpts(title="人物关系图谱"),
        )
        .render("./result/演职员图谱.html")
    )
    print("演职员关系图谱，保存路径为：./result/演职员图谱.html")
