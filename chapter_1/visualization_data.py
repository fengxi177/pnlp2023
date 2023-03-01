# -*- coding = utf-8 -*-

"""
    author:fengxi
    time:2023/2/28

    project name:pnlp2023
    file name:visualization_data.py
    function:
    短评相关数据分析与可视化
        (1) 评论数与位置分布图
        (2) 自行添加：评分与时间、评分与位置、评分与点赞数等 关系分析
"""

from collections import Counter
from pyecharts import options as opts
from pyecharts.charts import Bar


def analysis_location(location_list):
    """
        统计分析评论位置分布情况
    :param location_list: list
    :return:
    """

    location_dict = dict(Counter(location_list))
    x_list = list(location_dict.keys())
    y_list = list(location_dict.values())

    c = (
        Bar()
        .add_xaxis(x_list)
        .add_yaxis("评论位置与数量",
                   y_list,
                   # is_realtime_sort=True,
                   markpoint_opts=opts.MarkPointOpts(label_opts=opts.LabelOpts(position="top")),
                   )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="《狂飙》评论位置统计情况"),
            yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(formatter="{value} 条")),
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=90))
        )
        .render("./result/评论位置统计情况.html")
    )
    print("评论与位置关系分析结束，保存路径为：./result/评论位置统计情况.html")
