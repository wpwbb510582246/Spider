# -*- coding: utf-8 -*-
import scrapy

from Spider.util.CommonUtils import *
from Spider.util.MongoDbUtils import MongoDbUtils


class PieceSpider(scrapy.Spider):
    name = 'piece'
    allowed_domains = ['www.xiaopin5.com']
    start_urls = []
    origin_url = 'https://www.xiaopin5.com/'
    type = 'piece'

    def __init__(self, name=None, **kwargs):
        super(PieceSpider, self).__init__(name, **kwargs)
        # 获取每类小品的根地址
        html = get_one_page(self.origin_url, encode='gbk')
        pattern = '[\s\S]*?<ul class="categorys-items">([\s\S]*? )</ul>[\s\S]*?'
        count = 1
        for ul in parse_one_page(html, pattern):
            if count > 1:
                break
            pattern2 = '[\s\S]*?<a href="([\s\S]*?)">[\s\S]*?</a>'
            for a in parse_one_page(ul, pattern2):
                # 判断当前数据是否爬取
                self.start_urls.append(a)
                print('已添加' + ' -> ' + a)
            count += 1

    def parse(self, response):
        collection = 'piece'
        db_util = MongoDbUtils(collection)

        start_page = 1
        url = response.url
        html = get_one_page(url, encode='gbk')
        pattern = '[\s\S]*?<span class="pageinfo">[\s\S]*?<strong>([\s\S]*?)</strong>[\s\S]*?页'
        for tmp_total_page in parse_one_page(html, pattern):
            if tmp_total_page == '1':
                url = url
            else:
                pattern2 = '[\s\S]*?<div class="page-nav"[\s\S]*?<li><a href=[\s\S]*?list_([\s\S]*?)_[\s\S]*?>下一页[\s\S]*?>[\s\S]*?<span class="pageinfo">[\s\S]*?<strong>([\s\S]*?)</strong>[\s\S]*?页'
                for num in parse_one_page(html, pattern2):
                    type_index = num[0]
                    total_page = (int)(num[1])
        for page_index in range(start_page, total_page + 1):
            if (page_index == 1):
                a2 = url
            else:
                a2 = url + 'list_' + type_index + '_' + (str)(page_index) + '.html'
            # 判断当前数据是否爬取
            if check_spider_history(self.type, a2) == True:
                continue
            html = get_one_page(a2, encode='gbk')
            html = etree.HTML(html)
            count = 1
            for li in html.xpath('/html/body/div/div[5]/div[2]/div[1]/div[2]/ul/li'):
                # 解析小品数据
                # ('http://www.xiaopin5.com/zhaobenshan/272.html', '闫光明、赵本山小品全集高清《狭路相逢》 2012公安部春晚', 'http://www.xiaopin5.com/uploads/allimg/130524/1_05240023404137.jpg', '《狭路相逢》')
                play_url = get_str_from_xpath(li.xpath('./div/a[1]/@href'))
                name = get_str_from_xpath(li.xpath('./p[1]/a/text()'))
                dic = {'drama_url': play_url}
                find_piece = db_util.find(dic)
                if find_piece.count() >= 1:
                    print(name + ' -> 已爬取')
                    continue
                html = get_one_page(play_url, encode='gbk')
                html2 = etree.HTML(html)
                pattern = "[\s\S]*?window.open[\s\S]*?http://player.youku.com/embed/([\s\S]*?)'[\s\S]*?"
                for play_id in parse_one_page(html, pattern):
                    # 获取当前小品的类型
                    type = ''
                    type2 = ''
                    count2 = 1
                    for a3 in html2.xpath('/html/body/div/div[5]/div[1]/a'):
                        type = get_str_from_xpath(html2.xpath('/html/body/div/div[5]/div[1]/a[2]/text()'))
                        type2 = get_str_from_xpath(html2.xpath('/html/body/div/div[5]/div[1]/a[3]/text()'))
                        if len(type2) > 10:
                            # 当前小品没有第二种类型
                            type2 = ''
                    url2 = 'https://v.youku.com/v_show/id_' + play_id + '==.html'
                    piece = {
                        'name': name,
                        'description': get_str_from_xpath(li.xpath('./div/a[1]/@title')),
                        'src': get_str_from_xpath(li.xpath('div/a[1]/img/@src')),
                        'type': type,
                        'type2': type2,
                        'drama_url': play_url,
                        'url': url2
                    }
                    print('正在抓取 -> ' + type + ' ' + type2 + ' ' + piece['name'])
                    db_util.insert(piece)
            count += 1
            # 写入爬取数据
            write_spider_history(self.type, a2)