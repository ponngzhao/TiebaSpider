## 运行要求
1. python3.5
2. 安装json 
    `$ pip install json`
3. 安装requests
    `$ pip install requests`
4. 安装BeautifulSoup4
    `$ pip install beautifulsoup4`

## 运行步骤
1. 所要爬取的贴吧主页地址:home_page_url,贴吧名字:tieba_name,如：
    `home_page_url = http://tieba.baidu.com/f?kw=%E6%B1%9F%E5%8D%97%E5%A4%A7%E5%AD%A6`
    `tieba_name = '江南大学吧'`
2. 将/Src目录下的tiebaSpider.py中，main函数中的home_page_url和tieba_name改为相应的值
3. 将/Src目录下的para.json中，json_num改为0，next_page_url改为home_page_url的值
4. 将/Src目录下的tiebaSpider.py中,378行的数值改为目标爬去的贴数
5. 爬取完成后，运行/json_utf-8目录下的change.py
6. /json_utf-8目录下的json文件即为爬取结果

## 注意事项
- /json目录下的json为GBK编码，经过`运行步骤5`后，/json_utf-8目录下会出现utf-8编码文件
- 爬取速度较慢，所以一般不会被封ip，平均1秒钟爬1贴
- 程序中断时，只需重新运行/Src/tiebaSpider.py即可
- 当输出的status为403时，隔断时间再运行
- 一次只能爬取一个贴吧的帖子，除非再复制一个工程
- 达到目标爬取贴数时，不会立即停止(因为要把当前页面内的帖子全部爬取完成)

## json内容说明
- 一个json文件即为一个帖子
- 整体结构：
```
[
    {
        'url_id' ："" , //网址的url_id
        'content_post_id' : "" , //正文的post_id
        'post_date' : "" ,//发帖时间
        'title' : "" ,//贴子标题
        'reply_num' : "" ,//回复贴数
        'reply_page_num' : "" ,//回复页数
        'url' : "" ,//帖子地址
        'post_content' : "",//帖子正文内容
        'open_type' : "",//作者的open_type
        'author':{
            'user_id' : "",//作者user_id
            'user_name' : "",//作者名字
            'user_sex' : "",//作者性别
            'user_level' "": ,//作者级别
        }
        'reply_content_list' : [ //帖子的回复列表
            reply_content1,
            reply_content2,
            ......
        ]
    }
]
```
- reply_content结构
```
[
    {
        'post_no':"" ,//该楼层数
        'post_id': "",//该楼层的post_id
        'open_type':"" ,//该楼层的open_type设备信息
        'reply_content_text':"" ,//该楼层的回复内容
        'reply_num':"" ,//该楼层的回复数量
        'author':{//该楼层的作者信息
            'user_id': "",//该楼层作者id
            'user_name': "",//该楼层作者名字
            'user_sex' : "",//该楼层作者性别
            'user_level' : ""//该楼层作者等级
        },
        'reply_in_reply':[//该楼层的回复信息列表
            {
                'user_name' : "",//该楼层回复者名字
                'reply_content' :  "",//该楼层回复内容
                'reply_time' :"" //该楼层回复时间
            }
            {
                ...
            }
        ]
    }
    {
        ...
    }
]
```
## 待处理事项
- 增加多线程，加快帖子处理速度
- gbk转成utf-8
- ip地址代理 
- 防封ip处理
- 帖子查重