### http://www.iqiwx.com/
#### 项目由来
由于好几年之前的爬取笔趣阁小说的爬虫不能使用了，也没有维护，又重新写了一个爬取爱奇文学的爬虫 <br />
基于对爬虫和小说的热爱

#### 项目计划
1、本项目目前打算会进行长期维护 <br />
2、会进行数据定期同步 <br />
3、会出一个web展示，或者小程序<br />
4、进行分布式配置 <br />

#### 一、项目结构
```shell
.
├── Dockerfile                          # 项目Dockerfile脚本
├── README.md                           # 项目介绍文件README.md  
├── requirements.txt                    # 项目依赖文件
├── run_spider.py                       # 爬虫启动文件
├── scrapy.cfg
├── iqiwx                               # 爬虫项目
│   ├── __init__.py
│   ├── items.py                        
│   ├── middlewares.py
│   ├── pipelines.py
│   ├── settings.py
│   ├── spiders
│   │   ├── __init__.py
│   │   ├── iqiwx.py                    
│   └── utils.py
├──  web_book                            # web服务项目
│   ├── create_table.sql                # web服务依赖的数据库文件
│   ├── db.sqlite3
│   ├── images                          # 书封面的存放文件夹
│   ├── __init__.py
│   ├── manage.py
│   ├── scheduled_tasks                 # 任务服务，定时对爬取的新数据进行数据整理
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── __init__.py
│   │   ├── migrations
│   │   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── tasks.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── web_api                         # 提供前端使用API
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── __init__.py
│   │   ├── migrations
│   │   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   ├── utils.py
│   │   └── views.py
│   └── web_book
│       ├── celery.py
│       ├── database_router.py          # 数据库驱动文件
│       ├── __init__.py
│       ├── pagination.py               # 分页
│       ├── settings                    # web服务配置文件
│       │   ├── __init__.py
│       │   ├── prod.py                 # 私有配置文件
│       │   └── settings.py             # 基础配置文件
│       ├── urls.py
│       └── wsgi.py
└── web_html                            # 前端服务项目
    ├── babel.config.js
    ├── package.json
    ├── package-lock.json
    ├── public
    │   ├── favicon.ico
    │   ├── images
    │   │   └── window.gif
    │   └── index.html
    ├── README.md
    ├── src
    │   ├── App.vue
    │   ├── assets
    │   │   └── logo.png
    │   ├── components
    │   │   └── HelloWorld.vue
    │   ├── main.js
    │   ├── plugins
    │   │   ├── axios.js
    │   │   └── element.js
    │   ├── router
    │   │   └── index.js                # 前端路由
    │   ├── store
    │   │   └── index.js                # vue-x
    │   └── views
    │       ├── BookDetail.vue          # 书的章节列表
    │       ├── BookList.vue            # 书籍分类下的数据列表
    │       ├── BookRead.vue            # 每章的内容
    │       ├── Home.vue                
    │       └── Index.vue
    └── vue.config.js                   # 前端代理

```
#### 二、项目依赖安装
##### 1、后端服务及爬虫服务依赖安装
```shell script
pip install -r requirements.txt
```
##### 2、前端项目依赖安装
```shell script
npm install
```

#### 三、项目开发调试运行
`爬虫和后台服务启动，请先将相应表创建好，创建表sql文件 create_table.sql`
##### 1、爬虫(一下方式三选一即可)
###### ① 运行
```shell script
# bookSpider 是爬虫名称
scrapy crawl bookSpider
```

###### ② 运行爬虫，并且保存组装的item信息
```shell script
# bookSpider 是爬虫名称
scrapy crawl bookSpider -o items.json
```
###### ③ Python文件运行爬虫
```shell script
python run_spider.py
```

##### 2、web后台服务
`需修将mysql数据库的配置和缓存使用的redis数据库 改成你自己的 (web_book/settings/prod.py)`
```shell script
python manage.py runserver 0.0.0.0:8090
```

##### 3、celery服务
`需修将celery使用的redis数据库改成你自己的 (web_book/settings/prod.py)`
```shell script
celery worker -A web_book -P eventlet  -c 4 -l info
```

##### 4、前端服务运行
`需要修改后端代理文件（vue.config.js），指向你运行的web后台服务`
```shell script
# npm 安装依赖
npm install

# 运行服务
npm run serve
```

#### 四、部署
##### 1、创建数据库（如果以有数据库不需要次操作）
```shell script
# 进到mysql文件内,创建mysql镜像
docker build -t mysql:zh .
# 启动mysql服务容器
docker run -p 13306:3306 -d --name mysql mysql:zh
```

##### 2、爬虫、web服务及celery服务
`需修改配置文件中mysql数据库的配置和redis缓存数据库配置 (web_book/settings/prod.py)`
```shell script
# scrapy_book文件内,创建爬虫及web服务镜像
docker build -t scrapy_book:v1 .

# /data/scrapy_book需要更换成你自己的文件路径，绝对路径
# 爬虫服务
docker run -idt -v /data/scrapy_book:/scrapy_book --name=book_spider scrapy_book:v1 sh -c "cd /scrapy_book && python3 run_spider.py"
# web服务
docker run -itd -p 8090:8000 --name=web_book -v /data/scrapy_book/web_book:/web_book/ scrapy_book:v1 uwsgi --http 0.0.0.0:8000 --chdir /web_book/ --wsgi-file web_book/web_book/wsgi.py --module web_book.wsgi --master --processes 8 --threads 4

#需修将celery使用的redis数据库改成你自己的 (web_book/settings/prod.py)
docker run -it --name=celery -v /data/scrapy_book/web_book/:/web_book/ scrapy_book:v1 celery --workdir=/web_book/  worker -A web_book -P eventlet -c 4 -l info
```

##### 3、前端服务
`前端服务部署采用NGINX静态服务代理`
