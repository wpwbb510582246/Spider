# 爬虫大全

爬虫大全集合了大家常用的爬虫，为大家日常的开发提供方便。希望大家能共同努力，让这个项目变得丰富而充实。

这个项目主要基于 ```python``` 、```scrapy``` ，数据库采用```MongoDB```数据库，采集到的数据都保存在 ```MongodbDB``` 数据库。

> 本项目仅为学习之作，请勿用作商业用途，否则后果自负！

### 功能说明

##### 40资源网

网址为：https://jx40.net，爬虫名称：ziyuan40，内容：主要爬取最新的影视数据

##### 33uu资源网

网址为：http://www.156zy.co，爬虫名称：ziyuan33uu，内容：主要爬取最新的影视数据

##### ok资源网

网址为：http://www.okzy.co，爬虫名称：ok，内容：主要爬取最新的影视数据

##### 135资源网

网址为：http://135zy0.com，爬虫名称：zuiyuan135，内容：主要爬取最新的影视数据

##### 永久资源网

网址为：http://www.yongjiuzy.cc，爬虫名称：yongjiu，内容：主要爬取最新的影视数据

##### 爱奇艺视频

网址为：[https://iqiyi.com](https://www.iqiyi.com/)，爬虫名称：iqiyi，内容：主要包括各种爱奇艺视频中的电影、电视剧、综艺、动漫、少儿

##### 优酷视频

网址为：[https://youku.com](https://youku.com/)，爬虫名称：youku，内容：主要包括各种优酷视频中的电影、电视剧、综艺、动漫、少儿

##### 腾讯视频

网址为：https://v.qq.com，爬虫名称：tencent，内容：主要包括各种腾讯视频中的电影、电视剧、综艺、动漫、少儿

##### 最大资源网

网址为：www.zuidazy1.net，爬虫名称：zuida，内容：主要包括最大资源网中的各种最新影视资源

##### 酷云资源网

网址为：www.kuyunzy1.com，爬虫名称：kuyun，内容：主要包括酷云资源网中的各种最新影视资源

##### 好趣网

网址为：www.haoqu.net，爬虫名称：tv，内容：主要包括各种电视资源

##### 戏曲屋

网址为：www.xiqu5.com，爬虫名称：drama，内容：主要包括各种戏曲资源

##### 相声小品网

网址为：www.verity-china.com，爬虫名称：piece2，内容：主要包括各种小品资源

##### 小品屋

网址为：www.xiaopin5.com，爬虫名称：piece，内容：主要包括各种小品资源

##### QQ相册

网址为：i.qq.com，爬虫名称：album，内容：用于批量下载QQ空间中的照片

### 打赏

------

- 解决上面这些问题，需要花费很多时间与精力。支持项目继续完善下去，你也可以贡献一份力量！

- 有了打赏，也就会有更新的动力 : )

  ![](image/5.jpg)

### 更新日志

------

#### v4.2.0 `2019/11/13`

- 新增爬虫：
  - 新增小品吧(```piece3```)爬虫，网址为：http://www.xiaopin8.cc，主要爬取一些最新的相声小品
  - 新增小品网(```piece4```)爬虫，网址为：http://www.xiaopin.tv，主要爬取一些最新的相声小品
- 优化原有爬虫部分逻辑

#### v4.1.0 `2019/11/9`

- 新增爬虫：
  - 新增40资源网爬虫(```ziyuan40```)，网址为：[https://jx40.net](https://jx40.net/)，主要爬取一些最新的相声小品
- 优化原有爬虫部分逻辑

#### v3.2.0 `2019/10/25`

- 新增爬虫功能：
  - 爬取最新数据，一部分为6页，一部分为3页
- 优化原有爬虫部分逻辑

#### v3.1.0 `2019/10/19`

- 新增爬虫：
  - 新增相声小品网爬虫(```piece2```)，网址为：https://www.verity-china.com，主要爬取一些最新的相声小品
  - 新增永久资源网爬虫(```yongjiu```)，网址为：http://www.yongjiuzy.cc，主要爬取最新的影视数据
  - 新增135资源网爬虫(```zuiyuan135```)，网址为：[http://135zy0.com](http://135zy0.com)，主要爬取最新的影视数据
  - 新增ok资源网爬虫(```ok```)，网址为：http://www.okzy.co，主要爬取最新的影视数据
  - 新增33uu资源网爬虫(```ziyuan33uu```)，网址为：http://www.156zy.co，主要爬取最新的影视数据
- 优化原有爬虫部分逻辑

#### v2.1.0 `2019/9/30`

- 腾讯影视爬虫中新增少儿部分
- 新增优酷影视爬虫(```youku```)、爱奇艺影视爬虫(```iqiyi```)
- 优化原有爬虫部分逻辑

#### v1.1.0 `2019/9/30`

- 新增腾讯影视爬虫(```tencent```)
- 电视爬虫接口更新为好趣网(http://www.haoqu.net)
- 优化原有爬虫部分逻辑

#### v1.0.0 `2019/9/25`

- 完成项目的初始化
- 当前项目中包含的爬虫包括最大资源网(www.zuidazy1.net)、酷云资源网(www.kuyunzy1.com)、爱看TV(www.icantv.cn)、戏曲屋(www.xiqu5.com)、小品屋(www.xiaopin5.com)、QQ相册(i.qq.com)

### 开发文档[待完善]

------

#### 爬虫代码(Spider)使用方法

1、将```Spider/PocketLifeSpider/PocketLifeSpider/util```下面的```MongoDbUtils.py```中的```139.199.24.205```环卫数据库所在机器的域名或ip地址。

```python
settings = {
    # "ip":'localhost',   #ip
    "ip":'127.0.0.1',   #ip
    "port":27017,           #端口
    "db_name" : "spider",    #数据库名字
}
```

2、资源名称及其对应的命令

| 资源名称           | 命令                                   |
| ------------------ | -------------------------------------- |
| 最大资源网         | scrapy crawl zuida                     |
| 酷云资源网         | scrapy crawl kuyun                     |
| 爱看TV             | scrapy crawl tv                        |
| 爱看TV(指定关键词) | scrapy crawl tv -a keyword=CCTV-1      |
| 戏曲屋             | scrapy crawl drama                     |
| 戏曲屋(指定关键词) | scrapy crawl drama -a keyword=民间小调 |
| 戏曲屋(戏曲类型)   | scrapy crawl drama_type                |
| 小品屋             | scrapy crawl piece                     |
| 小品屋(小品类型)   | scrapy crawl piece_type                |
| QQ相册             | scrapy crawl album                     |
| 腾讯视频           | scrapy crawl tencent                   |
| 优酷视频           | scrapy crawl youku                     |
| 爱奇艺视频         | scrapy crawl iqiyi                     |