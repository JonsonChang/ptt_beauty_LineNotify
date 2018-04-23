# -*- coding: utf-8 -*-
import os
import requests
import re
from PttWebCrawler.crawler import PttWebCrawler as crawler
import codecs, json, os
 
def lineNotify(token, msg):
 
    url = "https://notify-api.line.me/api/notify"
    headers = {
        "Authorization": "Bearer " + token, 
        "Content-Type" : "application/x-www-form-urlencoded"
    }
    
    payload = {'message': msg}
    r = requests.post(url, headers = headers, params = payload)
    return r.status_code
    
def lineNotifyPic(token, msg, picURI):
    url = "https://notify-api.line.me/api/notify"
    headers = {
        "Authorization": "Bearer " + token
    }

    # download image  
    r_pic = requests.get(picURI)
    with open('a.jpg', 'wb') as f:  
        f.write(r_pic.content)

    payload = {'message': msg}
    files = {'imageFile': open('a.jpg', 'rb')}
    r = requests.post(url, headers = headers, params = payload, files = files)
    return r.status_code

def parse_URL(content):
    result = []
    regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    token = re.split(' ',tmp)
    for t in token:
        if re.match(regex, t):
            result.append(t)
            #print(t, "GG\r\n\r\n")
            
    #print( re.match(regex, "http://www.example.com") ) # True
    #print( re.match(regex, "example.com") ) # False        
    return result

    
# 發文字
#token = "xxxxxxxxxxxxxxxxxxxxx"
#msg = "Notify from Python \nHave a nice day 張小捲"
# lineNotify(token, msg)  


# 發圖片
#msg = "Hello Python"
#picURI = 'C:\\Users\\jonson\Desktop\\ptt_beauty_LineNotify\\a.jpg'
#picURI = 'https://i.imgur.com/eCNafC4.jpg'
# lineNotifyPic(token, msg, picURI)  


history_list=[]

if __name__ == '__main__':
    token = "ddddddddddddddddd"
    board = "Beauty"
    push_num = 10 #推文數門檻
    last_page = crawler.getLastPage(board)
    index_start = last_page - 1
    index_end = last_page
    filename = '{0}-{1}-{2}.json'.format(board, index_start, index_end)
    crawler(['-b', board, '-i', str(index_start), str(index_end)])
#    with codecs.open(filename, 'r', encoding='utf-8') as f:
#        data = json.load(f)
        # M.1127808641.A.C03.html is empty, so decrease 1 from 40 articles
        #self.assertEqual(len(data['articles']), 39)
        
    data = crawler.get(filename)
    os.remove(filename)
    articles =  data['articles']
    for a in articles:
        title = a['article_title']
        article_id = a['article_id']
        url = a['url']
        content = a['content']
        push =  a['message_count']['push']
        if push >= push_num and article_id not in history_list:
            print(push, title, url)
            history_list.append(article_id)
            imgs_url = parse_URL(content)
            lineNotify(token, "{0} {1}".format(title, url))  
            for u in imgs_url:
                lineNotifyPic(token, title, u)
            
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
