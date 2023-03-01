# -*- coding = utf-8 -*-

"""
    author:fengxi
    time:2023/2/17

    project name:pnlp2023
    file name:get_celebrity_info.py
    function:
        爬取豆瓣《狂飙》的演职员相关信息
        链接：https://movie.douban.com/subject/35465232/celebrities
"""

import pandas as pd
from bs4 import BeautifulSoup
from get_comments_data import get_html


def get_celebrity(url, filename):
    """
        解析演职员信息页面,提取数据并保存
    :param url:
    :param filename: csv文件名
    :return:
    """
    html = get_html(url)
    soup_info = BeautifulSoup(html, 'html.parser')

    # 获得的结果信息
    result_info_dict = {}

    # 提取评论
    info_all = soup_info.findAll("div", "info")
    for info in info_all:
        info_name = info.find("span", "name").text
        info_role = info.find("span", "role").text
        info_works_list = info.find("span", "works").findAll("a")

        # 预处理
        info_name_split = info_name.split(" ")
        if len(info_name_split) >= 2:
            name = info_name_split[0]  # 姓名
            # name_pinyin = " ".join(info_name_split[1:])
        else:
            name = info_name
        role_to_play = ""  # 饰演人物名
        if "演员" in info_role:
            role = ["演员"]  # 担任角色
            role_to_play = info_role.split(" ")[-1].replace(")", "")
        else:
            role = info_role.split(" ")[0].split("/")  # 担任角色
        works_list = []  # 代表作list
        for a_works in info_works_list:
            works = a_works.text
            works_list.append(works)

        # 添加上没有标注该片的
        if "狂飙" not in works_list:
            works_list.append("狂飙")
        # print(name, role, role_to_play, works_list)

        if name not in result_info_dict.keys():
            result_info_dict[name] = {"role": role, "role_to_play": role_to_play, "works": works_list}
        else:
            # 一人担任多个角色情况
            role_temp = result_info_dict[name]["role"]
            if role not in role_temp:
                role_temp += role
            result_info_dict[name]["role"] = role_temp

    # 保存数据
    result = []
    for key, value in result_info_dict.items():
        # 姓名、角色(";"分割多个)、饰演人物(可能为空)、代表作(";"分割多个)
        row = [key, ";".join(value["role"]), value["role_to_play"], ";".join(value["works"])]
        result.append(row)

    colunms_list = ["姓名", "角色", "饰演人物", "代表作"]
    df = pd.DataFrame(result, columns=colunms_list)
    df.to_csv(filename, index=False, encoding="utf-8-sig")
    print("演职员信息获取、保存完毕...")


if __name__ == '__main__':
    # 获取《狂飙》演职员信息
    filename = "./data/狂飙演职员信息表.csv"

    url = "https://movie.douban.com/subject/35465232/celebrities"
    get_celebrity(url, filename)
