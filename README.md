#### http://www.iqiwx.com/
##### 项目由来
由于好几年之前的爬取笔趣阁小说的爬虫不能使用了，也没有维护，又重新写了一个爬取爱奇文学的爬虫 <br />
基于对爬虫和小说的热爱

##### 项目计划
1、本项目目前打算会进行长期维护 <br />
2、会进行数据定期同步 <br />
3、会出一个web展示，或者小程序<br />
4、进行分布式配置 <br />

安装依赖
由于Windows环境下安装各种限制，建议在Linux环境中使用

##### 建议使用单独的依赖环境
```
pip install -r requirements.txt
```
##### 运行爬虫
```
# bookSpider 是爬虫名称
scrapy crawl bookSpider
```

##### 运行爬虫，并且保存组装的item信息
```
# bookSpider 是爬虫名称
scrapy crawl bookSpider -o items.json
```
