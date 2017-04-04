#coding:utf-8
import json
import re
import copy
import requests
import sys
from bs4 import BeautifulSoup

class TiebaSpider:
    
    def __init__(self,home_page_url,tieba_name,next_page_url):
        self.tieba_name = tieba_name
        self.home_page_url = home_page_url
        self.next_page = next_page_url
        # self.response = requests.get(home_page_url)
        # soup = BeautifulSoup(response.body)
        # # next_soup = soup.find("a","next pagination-item ")
        # # # print(len(next_soup))
        # count = 0
        # # if next_soup:
        # #     next_url = next_soup.get('href')
        # #     print(next_url)
        # #     next_page = response.urljoin(next_url)
        # #     yield scrapy.Request(next_page,callback=self.parse)
        # content_url_soup = soup.find_all("a","j_th_tit")
        # for i in content_url_soup:
        #     # print(i.get('href'))
        #     url = 'http://tieba.baidu.com'+i.get('href')
        #     yield scrapy.Request(url,callback=self.parse_posts)
        #     count += 1
        #     # break
        #     if count > 100:
        #         break
    #得到url的response
    def get_response(self,url):
        try:
            response = requests.get(url)
            print("status :"+str(response.status_code))
        except:
            print("status :"+str(response.status_code))
            print("打开"+url+"失败")
            quit()
        return response
    #得到该帖吧的帖子url_list
    def get_page_url(self):
        home_page_response = self.get_response(self.next_page)
        soup = BeautifulSoup(home_page_response.text)
        content_url_soup = soup.find_all("a","j_th_tit")
        next_page_soup = soup.find_all("a","next pagination-item ")
        if len(next_page_soup) > 0:
            self.next_page = next_page_soup[0].get('href')
        else:
            self.next_page = None
        f = open('./Src/para.json','r')
        data = f.readlines()
        para = ""
        for i in data:
            para += i
        para = eval(para)
        para['next_page_url'] = self.next_page
        f.close()
        f = open('./Src/para.json','w')
        para = json.dumps(para,sort_keys=True,ensure_ascii=False,indent=2)
        f.write(para)
        f.close()
        count = 0
        url_list = []
        for i in content_url_soup:
            # print(i.get('href'))
            url = 'http://tieba.baidu.com'+i.get('href')
            url_list.append(url)
            count += 1
            # break
            # if count >= 1:
            #     break
        return url_list
    #得到response的url
    def get_url(self,response):
        url = response.url
        return url
    #得到帖子url的url_id
    def get_url_id(self,page_url):
        url_id_re_string = r"http://tieba.baidu.com/p/(\d+)"
        url_id_pattern = re.compile(url_id_re_string)
        url_id = url_id_pattern.findall(page_url)[0]
        return url_id
    #根据帖子网址的response,得到贴子标题
    def get_title(self,page_response):
        soup = BeautifulSoup(page_response.text)
        title_soup = soup.find("h1")
        title = title_soup.get_text()
        return title
    #根据帖子response，得到帖子发帖时间
    def get_post_date(self,page_response):
        soup = BeautifulSoup(page_response.text)
        date_soup = soup.find_all("div","l_post j_l_post l_post_bright noborder ")
        date = None
        if len(date_soup)>0:
            date_soup = date_soup[0]
            data_field_str = date_soup.get('data-field')
            data_field_dict =  json.loads(data_field_str)
            date = data_field_dict['content']['date']
        return date
    #根据帖子response，得到楼主帖子的post_id
    def get_content_post_id(self,page_response):
        soup = BeautifulSoup(page_response.text)
        data_soup = soup.find_all("div","l_post j_l_post l_post_bright noborder ")
        content_post_id = None
        if len(data_soup)>0:
            data_soup = data_soup[0]
            data_field_str = data_soup.get('data-field')
            data_field_dict =  json.loads(data_field_str)
            content_post_id = data_field_dict['content']['post_id']
        return content_post_id
    #根据帖子response，得到帖子正文内容
    def get_post_content(self,page_response):
        soup = BeautifulSoup(page_response.text)
        content_post_id = self.get_content_post_id(page_response)
        soup_id = 'post_content_'+str(content_post_id)
        content_soup = soup.find_all("div",id=soup_id)
        content = None
        if len(content_soup) > 0:
            content_soup = content_soup[0]
            content = content_soup.get_text()
        return content
    #得到帖子的open_type
    def get_open_type(self,page_response):
        soup = BeautifulSoup(page_response.text)
        data_soup = soup.find_all("div","l_post j_l_post l_post_bright noborder ")
        open_type = None
        if len(data_soup)>0:
            data_soup = data_soup[0]
            data_field_str = data_soup.get('data-field')
            data_field_dict =  json.loads(data_field_str)
            open_type = data_field_dict['content']['open_type']
        return open_type
    #得到作者信息：user_id,user_name,user_sex,level
    def get_author(self,page_response):
        soup = BeautifulSoup(page_response.text)
        data_soup = soup.find_all("div","l_post j_l_post l_post_bright noborder ")
        author = {
            'user_id' : None,
            'user_name' : None,
            'user_sex' : None,
            'user_level' : None
        }
        sex_dict = {
            0 : None,
            1 : "man",
            2 : "woman"
        }
        if len(data_soup)>0:
            author = {
                'user_id' : None,
                'user_name' : None,
                'user_sex' : None,
                'user_level' : None
            }
            data_soup = data_soup[0]
            data_field_str = data_soup.get('data-field')
            data_field_dict =  json.loads(data_field_str)
            author['user_id'] = data_field_dict['author']['user_id']
            author['user_name'] = data_field_dict['author']['user_name']
            author['user_sex'] = data_field_dict['author']['user_sex']
            author['user_level'] = data_field_dict['author']['level_id']
            author['user_sex'] = sex_dict[author['user_sex']]
        return author
    #得到帖子的回复贴数
    def get_reply_num(self,page_response):
        soup = BeautifulSoup(page_response.text)
        reply_soup = soup.find_all("span","red")
        reply_num = None
        if len(reply_soup)>0:
            reply_soup = reply_soup[0]
            # reply_soup = reply_soup.findall('li')
            # print(len(reply_soup))
            reply_num = reply_soup.get_text()
        return reply_num
    #得到帖子的回复页数
    def get_reply_page_num(self,page_response):
        soup = BeautifulSoup(page_response.text)
        reply_soup = soup.find_all("span","red")
        reply_page_num = None
        if len(reply_soup)>0:
            reply_soup = reply_soup[1]
            # reply_soup = reply_soup.findall('li')
            # print(len(reply_soup))
            reply_page_num = reply_soup.get_text()
        return reply_page_num
    #得到楼主正文信息：url_id,content_post_id,post_date,title,post_content,open_type,author,reply_num,page_num,url
    def get_content_info(self,page_response):
        info = {}
        info['url'] = self.get_url(page_response)
        info['url_id'] = self.get_url_id(page_response.url)
        info['title'] = self.get_title(page_response)
        info['post_date'] = self.get_post_date(page_response)
        info['content_post_id'] = self.get_content_post_id(page_response)
        info['post_content'] = self.get_post_content(page_response)
        info['open_type'] = self.get_open_type(page_response)
        info['author'] = self.get_author(page_response)
        info['reply_num'] = self.get_reply_num(page_response)
        info['reply_page_num'] = self.get_reply_page_num(page_response)
        info['reply_content_list'] = []
        return info
    #得到楼中楼，返回reply_in_reply_list
    def parse_reply_in_reply(self,url_id,post_id,reply_num):
        pages = int(reply_num/10) + 1
        reply_in_reply_list = []
        for page in range(1,pages+1):
            reply_list = []
            url = 'http://tieba.baidu.com/p/comment?tid='+str(url_id)+'&pid='+str(post_id)+'&pn='+str(page)
            reply_response = requests.get(url)
            reply_list = self.get_reply_in_reply(reply_response)
            reply_in_reply_list += reply_list
        return reply_in_reply_list
    #通过楼中楼页面的response，得到该response中的楼中楼
    def get_reply_in_reply(self,reply_response):
        # reply_in_reply_list = reply_response.meta['reply_list']
        reply_in_reply_list = []
        soup = BeautifulSoup(reply_response.content)
        reply_soup = soup.find_all('div','lzl_cnt')
        # print("************")
        # print(reply_response.url)
        # print("************")
        if len(reply_soup) > 0:
            for soup_temp in reply_soup:
                reply_in_reply = {
                    'user_name' : None,
                    'reply_content' : None,
                    'reply_time' : None
                }
                reply_data_soup = soup_temp.find_all('a','at j_user_card ')[0]
                reply_in_reply['user_name'] = reply_data_soup.get('username')
                reply_content_soup = soup_temp.find_all('span','lzl_content_main')[0]
                reply_in_reply['reply_content'] = reply_content_soup.get_text()
                reply_date_soup = soup_temp.find_all('span','lzl_time')[0]
                reply_in_reply['reply_time'] = reply_date_soup.get_text()
                reply_in_reply_list.append(reply_in_reply)
        return reply_in_reply_list


    #得到回复楼层的信息：reply_content
    def get_reply_content(self,response):
        soup = BeautifulSoup(response.text)
        data_soup = soup.find_all("div","l_post j_l_post l_post_bright ")
        author = {
            'user_id' : None,
            'user_name' : None,
            'user_sex' : None,
            'user_level' : None
        }
        reply_content_list = []
        reply_content = {
            'post_no' : None,
            'post_id' : None,
            'open_type' : None,
            'reply_content_text' : None,
            'reply_num' : None,
            'author' : author,
            'reply_in_reply' : []
        }
        reply_in_reply = {
            'user_name' : None,
            'reply_content' : None,
            'reply_time' : None
        }
        sex_dict = {
            0 : None,
            1 : "man",
            2 : "woman"
        }

        if len(data_soup) > 0:
            count = 0
            for reply_soup in data_soup:
                data_field_str = reply_soup.get('data-field')
                data_field_dict = json.loads(data_field_str)
                user_id = data_field_dict['author']['user_id']
                user_name = data_field_dict['author']['user_name']
                user_sex =sex_dict[data_field_dict['author']['user_sex']]
                user_level = data_field_dict['author']['level_id']
                author = {
                    'user_id' : None,
                    'user_name' : None,
                    'user_sex' : None,
                    'user_level' : None
                }
                author['user_id'] = user_id
                author['user_name'] = user_name
                author['user_sex'] = user_sex
                author['user_level'] = user_level
                post_no = data_field_dict['content']['post_no']
                post_id = data_field_dict['content']['post_id']
                open_type = data_field_dict['content']['open_type']
                reply_num = data_field_dict['content']['comment_num']
                content_soup = reply_soup.find_all('div','d_post_content j_d_post_content clearfix')
                reply_content_text = None
                if len(content_soup) > 0:
                    content_soup = content_soup[0]
                    reply_content_text = content_soup.get_text()
                reply_content['post_no'] = post_no
                reply_content['post_id'] = post_id
                reply_content['open_type'] = open_type
                reply_content['reply_content_text'] = reply_content_text
                reply_content['reply_num'] = reply_num
                reply_content['author'] = author
                if int(reply_num) > 0:
                    reply_in_reply_list = self.parse_reply_in_reply(self.get_url_id(response.url),post_id,reply_num)
                    reply_content['reply_in_reply'] = reply_in_reply_list
                else:
                    reply_content['reply_in_reply'] = []
                if author['user_name'] == "贴吧触点推广":
                    continue
                reply_content_list.append(copy.deepcopy(reply_content))
        return reply_content_list

    #存储帖子为json
    def save_info(self,info):
        f = open('./Src/para.json','r')
        data = f.readlines()
        para = ""
        for i in data:
            para += i
        para = eval(para)
        json_num = para['json_num']
        f.close()

        f1 = open('./json/'+str(json_num)+'.json','w',errors="ignore")
        line = json.dumps(info,sort_keys=True,ensure_ascii=False,indent=2)
        f1.write(line)
        f1.close()

        f = open('./Src/para.json','w')
        para['json_num'] = int(json_num) + 1
        line = json.dumps(para,sort_keys=True,ensure_ascii=False,indent=2)
        f.write(line)
        f.close()
        print("写入"+str(json_num)+".json成功")


    def parse_posts(self):
        f = open('./Src/para.json','r')
        data = f.readlines()
        para = ""
        for i in data:
            para += i
        para = eval(para)
        count_sum = int(para['json_num'])
        f.close()
        count1 = count_sum
        next_page1 = self.next_page
        try:
            while True:
                count1 = count_sum
                next_page1 = self.next_page
                page_url_list = self.get_page_url()
                if len(page_url_list) == 0:
                    break
            # print(self.next_page)
                for page_url in page_url_list:
                    try:
                        page_url_response = self.get_response(page_url)
                        print("*"*40)
                        print("count_sum:"+str(count_sum)+" 正在下载："+page_url)
                        info = self.get_content_info(page_url_response)
                        reply_page_num = int(info['reply_page_num'])
                        print("共："+str(reply_page_num)+"页评论")
                        for page in range(1,reply_page_num+1):
                    # print("page = "+str(page))
                            print("正在下载%d页评论"%page)
                            url = 'http://tieba.baidu.com/p/'+info['url_id']+'?pn='+str(page)
                            content_response = requests.get(url)
                            info['reply_content_list'] += self.get_reply_content(content_response)
                        self.save_info(info)
                        count_sum += 1
                        print("count1:"+str(count1))
                        print("*"*40)
                        if count_sum >= 1500:
                            quit()
                    except KeyboardInterrupt:
                        quit()
                    finally:
                        print("count_sum:"+str(count_sum)+"Error")
                        print(page_url)
                        print(sys.exc_info()[0])
                        if count_sum >= 1500:
                            quit()
        except:
            para['json_num'] = count1
            para['next_page_url'] = next_page1
            f = open('./Src/para.json','w')
            line = json.dumps(para,sort_keys=True,ensure_ascii=False,indent=2)
            f.write(line)
            f.close()
            print(str(count_sum)+"失败")
            print(sys.exc_info()[0])
            quit()

            # # print(info)
            #     line = json.dumps(info,sort_keys=True,ensure_ascii=False,indent=2)
            # # print(type(line))
            # # print(line.encode('gbk').decode('utf-8'))
            # # print(line)
            #     f = open("test.json","w")
            #     f.write(line)
            #     f.close()
        # item = TiebaspiderItem()
        # item['reply_content_list'] = []
        #得到帖子的正文信息
        # info = self.get_content_info(response)
        # #得到帖子的评论内容
        # page_num = int(info['reply_page_num'])
        # for page in range(1,page_num+1):
        #     url = 'http://tieba.baidu.com/p/4873016256?pn='+str(page)
        #     content_response = requests.get(url)
        #     item['reply_content_list'] += self.get_reply_content(content_response)
        #     print("正在下载%d页评论"%page)
        # # f = open("test.json","w")
        # # f.write(item)
        # # f.close()
        # return item
        # item['reply_content_list'] = self.get_reply_content(response)
def main():
    
    home_page_url = 'http://tieba.baidu.com/f?kw=%E6%B1%9F%E5%8D%97%E5%A4%A7%E5%AD%A6'
    tieba_name = '江南大学吧'

    f = open('./Src/para.json','r')
    data = f.readlines()
    para = ""
    for i in data:
        para += i
    para = eval(para)
    next_page_url = para['next_page_url']
    f.close()
    # print(next_page_url)
    spider = TiebaSpider(home_page_url,tieba_name,next_page_url)
    spider.parse_posts()

if __name__ == '__main__':
    main()