# -*- coding: utf-8 -*-
import time
from urllib import parse

import numpy
import redis
import scrapy
from selenium.webdriver.support.wait import WebDriverWait

from Spider.items import DramaItem
from Spider.util.CommonUtils import *
from Spider.util.MongoDbUtils import MongoDbUtils


class DramaSpider(scrapy.Spider):
    name = 'drama'
    allowed_domains = ['www.xiqu5.com']
    start_urls = []
    orign_url = 'http://www.xiqu5.com'
    parse_orign_url = 'https://pocket.mynatapp.cc'
    collection = 'drama'
    dbutils = MongoDbUtils(collection)
    search_domain = 'http://www.xiqu5.com/search.asp'
    # 搜索关键词
    keyword = None
    type = 'drama'

    def __init__(self, target=None, keyword=None, name=None, **kwargs):
        super(DramaSpider, self).__init__(name, **kwargs)
        if keyword is not None:
            # 搜索指定影视
            driver = get_driver(0)
            driver.get(self.orign_url)
            # //*[@id="seach"]/form/input[1]
            driver.find_element_by_xpath('//*[@id="seach"]/form/input[1]').send_keys(keyword)
            driver.find_element_by_xpath('//*[@id="ssubmit"]').click()
            driver.implicitly_wait(2)
            js = "var q=document.documentElement.scrollTop=100000"
            driver.execute_script(js)
            driver.find_element_by_id('qiushi').send_keys('1')
            driver.find_element_by_xpath('//*[@id="page"]/input[2]').click()
            self.keyword = driver.current_url.split('keyword=')[1]
            first_search_url = self.search_domain + '?page=1&keyword=' + self.keyword
            self.start_urls.append(first_search_url)
            driver.quit()
        else:
            html = get_one_page(self.orign_url, 'gb2312')
            pattern = '[\s\S]*?<div class="acc2 ">([\s\S]*?)</div>'
            for row in parse_one_page(html, pattern):
                pattern2 = '[\s\S]*?<a href="([\s\S]*?)"[\s\S]*?>([\s\S]*?)</a>[\s\S]*?'
                for col in parse_one_page(row, pattern2):
                    # 戏曲分类型地址
                    url = self.orign_url + col[0]
                    if '.html' not in url:
                        url = url + 'index.html'
                        self.start_urls.append(url)
                    # 戏曲类型名称
                    drama_type_name = col[1]
                    if 'font' in col[1]:
                        drama_type_name = col[1].split('>')[1].split('<')[0]

    def parse(self, response):
        try:
            if self.keyword is not None:
                driver = get_driver(0)
                page_size = 10
            else:
                page_size = 24
        except:
            driver.execute_script('window.stop()')
        finally:
            html = get_one_page(response.url, 'gb2312')
            pattern3 = ''
            if self.keyword is not None:
                pattern3 = pattern3 = '[\s\S]*?<div id="page" class="bord mtop">[\s\S]*?共([\s\S]*?)条记录[\s\S]*?'
            else:
                pattern3 = '[\s\S]*?<div id="page" class="bord mtop">[\s\S]*?共([\s\S]*?)部[\s\S]*?'
            total = 0
            for total2 in parse_one_page(html, pattern3):
                total = (int)(total2)
            total_page = total / page_size
            if total % page_size != 0:
                total_page += 1
            for index in numpy.arange(1, total_page + 1, 1):
                drama_type_url = response.url
                if self.keyword is not None:
                    url = drama_type_url.split('page=')[0] + 'page=' + (str)((int)(index)) + '&' + \
                          drama_type_url.split('page=')[1].split('&')[1]
                else:
                    if 'index.html' in response.url:
                        url = drama_type_url
                    else:
                        if '.html' not in response.url:
                            url = response.url + 'index.html'
                    if index != 1:
                        url = url.split('.html')[0] + (str)((int)(index)) + '.html'
                # 判断当前数据是否爬取
                if check_spider_history(self.type, url) == True:
                    continue
                html = get_one_page(url, 'gb2312')
                pattern3 = '[\s\S]*?<div class="content bord mtop">[\s\S]*?([\s\S]*?)</div>'
                for div in parse_one_page(html, pattern3):
                    if self.keyword is not None:
                        pattern4 = '[\s\S]*?<li>[\s\S]*?<a href="([\s\S]*?)"[\s\S]*?src="([\s\S]*?)"[\s\S]*?title="([\s\S]*?)"[\s\S]*?主演：([\s\S]*?)</p>[\s\S]*?分类：([\s\S]*?)</p>[\s\S]*?来源：([\s\S]*?)</p>[\s\S]*?时间：([\s\S]*?)</p>[\s\S]*?</li>'
                    else:
                        pattern4 = '[\s\S]*?<li>[\s\S]*?<a href="([\s\S]*?)"[\s\S]*?src="([\s\S]*?)"[\s\S]*?title="([\s\S]*?)"[\s\S]*?说明：([\s\S]*?)</p>[\s\S]*?频道：([\s\S]*?)</p>[\s\S]*?更新：([\s\S]*?)</p>[\s\S]*?简介：([\s\S]*?)</p>[\s\S]*?</li>'
                    for drama in parse_one_page(div, pattern4):
                        dramaItem = DramaItem()
                        # ('148451', '京剧锁五龙孟广禄主演', '未知', '京剧', '2019/4/25 14:32:11', '京剧锁五龙孟广禄主演详情请观看该戏曲，谢谢光临')
                        if self.keyword is not None:
                            id = drama[0].split('/')[1]
                            drama_url = url.split('search.asp')[0] + drama[0]
                        else:
                            id = drama[0]
                            # http://www.xiqu5.com/jj/index2.html
                            drama_url = url.split('.html')[0].split('index')[0] + id
                        dic = {'id': id}
                        find_drama = self.dbutils.find(dic)
                        source_exists = False
                        if find_drama.count() >= 1:
                            for tmp_drama in find_drama:
                                if len(tmp_drama['sources']) == 0:
                                    print(id + ' ->已插入，戏曲源未抓取')
                                else:
                                    print(id + ' ->已插入，戏曲源已抓取')
                                    source_exists = True
                                break
                        else:
                            if self.keyword is not None:
                                dramaItem['id'] = id
                                dramaItem['src'] = drama[1]
                                dramaItem['name'] = drama[2]
                                dramaItem['description'] = drama[3]
                                dramaItem['type'] = drama[4]
                                dramaItem['update_time'] = drama[6]
                                dramaItem['introduction'] = '详情请观看该戏曲，谢谢光临'
                            else:
                                dramaItem['id'] = id
                                dramaItem['src'] = drama[1]
                                dramaItem['name'] = drama[2]
                                dramaItem['description'] = drama[3]
                                dramaItem['type'] = drama[4]
                                dramaItem['update_time'] = drama[5]
                                dramaItem['introduction'] = drama[6]
                            type_name = drama_url.split('/')[3]
                        if source_exists == True:
                            continue
                        # 戏曲源没有抓取
                        html = get_one_page(drama_url, 'gb2312')
                        pattern = '[\s\S]*?戏曲说明：([\s\S]*?)</span>[\s\S]*?播放时长：<em>([\s\S]*?)</em>'
                        # 解析资源种类
                        for drama2 in parse_one_page(html, pattern):
                            print('正在解析戏曲信息 -> ' + id)
                            dramaItem['drama_description'] = drama2[0]
                            dramaItem['play_time'] = drama2[1]
                            print(id + ' -> 戏曲说明:' + dramaItem['drama_description'] + ' 播放时长:' + dramaItem['play_time'])
                            pattern = '<div class="bord demand mtop">[\s\S]*?</h3>([\s\S]*?)<div class="clear"></div>'
                        sources = []
                        count_source = 1
                        # 解析类型种类
                        for source_html in parse_one_page(html, pattern):
                            if count_source > 1:
                                break
                            types = []
                            pattern = '[\s\S]*?<a [\s\S]*? href="([\s\S]*?)" title="([\s\S]*?)">[\s\S]*?</a>'
                            for type in parse_one_page(source_html, pattern):
                                type_html = type[0]
                                type_name = type[1]
                                html = get_one_page(drama_url + '/' + type_html)
                                pattern = '[\s\S]*?var arr2 = [\s\S]*?"([\s\S]*?).youku'
                                # 解析播放地址
                                type_id = ''
                                for t_id in parse_one_page(html, pattern):
                                    type_id = t_id
                                url2 = 'https://v.youku.com/v_show/id_' + type_id + '.html'
                                type = {'name': type_name, 'url': url2}
                                types.append(type)
                            source = {'types': types}
                            sources.append(source)
                            count_source += 1
                        dramaItem['sources'] = sources
                        dic = {'id': id}
                        print('正在插入 -> 类型:' + type_name + ' 当前页:' + (str)((int)(index)) + ' 总页数:' + (str)(
                            (int)(total_page)) + ' 戏曲id:' + id + ' 戏曲名称:' + dramaItem['name'])
                        self.dbutils.insert(dict(dramaItem))
                        print(id + ' -> 信息插入完成')
                # 写入爬取数据
                write_spider_history(self.type, url)
            if self.keyword is not None:
                driver.quit()