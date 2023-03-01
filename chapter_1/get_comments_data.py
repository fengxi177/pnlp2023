# -*- coding = utf-8 -*-

"""
    author:fengxi
    time:2023/2/17

    project name:pnlp2023
    file name:get_comments_data.py
    function:
        爬取豆瓣《狂飙》评论（短评）信息
        链接：https://movie.douban.com/subject/35465232/comments?status=P
"""

import random
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup


def get_html(url):
    """获取url页面"""
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                             '(KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
    req = requests.get(url, headers=headers)
    content = req.content.decode('utf-8')

    return content


def parse_comments(url):
    """
        解析HTML页面,获得评论及相关数据
    :param url:
    :return:
    """
    html = get_html(url)
    soup_comment = BeautifulSoup(html, 'html.parser')

    # 所有获取的一页数据
    data_page = []

    # 提取评论
    comments_all = soup_comment.findAll("div", "comment-item")
    for comments in comments_all:
        try:
            # 解析评论及相关数据
            comment_info = comments.find("span", "comment-info")  # 评论id相关信息
            comment_vote = comments.find("span", "comment-vote")  # 评论点赞信息
            comment_content = comments.find("span", "short").text.replace("\n", "")  # 评论内容

            # 提取需要的各字段信息
            info_list = comment_info.findAll("span")
            star_rating = info_list[1]

            user_name = comment_info.find("a").text
            video_status = info_list[0].text  # 电视剧观看状态
            comment_score = int(star_rating["class"][0][-2:])  # 评论分值
            comment_level = star_rating["title"]  # 评论等级
            comment_time = info_list[2].text.replace("\n", "").replace("    ", "")  # 评论时间
            # print(info_list)
            comment_location = info_list[3].text  # 评论位置

            comment_vote_count = int(comment_vote.find("span", "votes vote-count").text)  # 评论被点赞数

            # 获取的一条数据
            # ["用户名", "电视剧观看状态", "评论分数", "评论等级", "评论时间", "评论位置", "评论点赞数", "评论"]
            data_row = [user_name, video_status, comment_score, comment_level,
                        comment_time, comment_location,
                        comment_vote_count, comment_content]
            data_page.append(data_row)
        except:
            # 跳过解析异常的数据
            continue

    return data_page


def get_all_comments(filename):
    """
        爬取短评（好评、中评和差评）
    :param filename: csv文件，保存评论数据
    :return:
    """
    comment_type_dict = {"好评": "h", "中评": "m", "差评": "l"}  # 评论类型字典
    for comment_type, comment_type_value in comment_type_dict.items():
        for page in range(11):
            url = "https://movie.douban.com/subject/35465232/comments?percent_type={}" \
                  "&start={}&limit=20&status=P&sort=new_score"\
                .format(comment_type_value, page*20)
            print('正在获取：{}的第{}页的评论'.format(comment_type, page + 1))
            print(url)

            # 解析获得一页数据
            data_page = parse_comments(url)
            columns_list = ["用户名", "电视剧观看状态", "评论分数", "评论等级", "评论时间", "评论位置", "评论点赞数", "评论"]  # 列名
            df = pd.DataFrame(data_page, columns=columns_list)

            # 每页数据保存一次，防止获取数据过程中断
            if page == 0 and comment_type_value == "h":
                df.to_csv(filename, index=False, encoding="utf-8-sig")
            else:
                # 第二页开始追加保存数据
                df.to_csv(filename, index=False, header=False, encoding="utf-8-sig", mode="a")

            # 随机休眠，限制访问频率
            time.sleep(random.choice([3, 4, 5, 6]))
    print("数据获取完毕...")


if __name__ == '__main__':
    # 保存评论文件名
    filename = "./data/狂飙_20230228.csv"
    print("开始获取数据...")
    get_all_comments(filename)

    pass


