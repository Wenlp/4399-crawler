# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 22:45:40 2021

@author: asus-pc
"""

import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from queue import Queue
from sympy.core.numbers import Integer

def frontier_extend(seed,headers):
    wait_que = Queue()
    wait_que.put(seed)
    parsed_list = [seed] #包括所有加入过wait_que的url，可以解析过（不在队伍里）或者没解析过（还在等待）
    df = pd.DataFrame(
        columns = ['g_tit','g_cls','g_size','g_date','g_spe','g_intro']
    )
    wait_que.maxsize = 1000
    stop_sign = Integer(0) # just in demo, stop once qsize reached max
    #-----------bfs-------------
    while(not wait_que.empty()):
        url = wait_que.get()
        html = requests.get(url,headers=headers)
        if html.status_code==200:
            #parsed_list.append(url)
            html.encoding='GBK'
            soup = BeautifulSoup(html.text,features='lxml')
            
            intr = soup.find(name='div',attrs={'class':'intr-r'})
            if intr is not None:# intro page 小游戏简介页面
                g_tit = intr.find(name='div',attrs={'class':'tit cf'}).text
                g_cls, g_size, g_date = [
                    x[3:] for x in 
                    intr.find(name='div',attrs={'class':'cls'}).text.replace('\xa0','').split('|')
                ]
                g_spe_list = intr.find(name='div',attrs={'class':'spe'})
                if g_spe_list is not None:
                    g_spe_list = g_spe_list.findAll(name='a')
                    g_spe_list = [x.text for x in g_spe_list]
                else:
                    g_spe_list = []
                if intr.find(name='font') is None:
                    g_intro = ''
                else:
                    g_intro = intr.find(name='font').text
            else: 
                intr = soup.find(name='div',attrs={'class':'game-des'})
                if intr is not None: # game page 小游戏开始页面
                    g_tit = intr.find(name='div',attrs={'class':"name"}).find(\
                         name='a').text
                    sorts_cf = intr.find(name='div',attrs={'class':'sorts cf'})
                    emphases = sorts_cf.findAll(name='em')
                    g_cls = emphases[0].find(name='a').text
                    g_size = emphases[1].text[3:]
                    g_date = emphases[2].text[3:]
                    g_spe_list = sorts_cf.find(name='div',attrs={'class':'spe'})
                    if g_spe_list is not None:
                        g_spe_list = g_spe_list.findAll(name='a')
                        g_spe_list = [x.text for x in g_spe_list]
                    else:
                        g_spe_list = []
                    g_intro = ''
                else:
                    continue #网页游戏没有简介，不计入采集范围
            #end if
            df = df.append([{'g_tit':g_tit,
                       'g_cls':g_cls,
                       'g_size':g_size,
                       'g_date':g_date,
                       'g_spe':g_spe_list,
                       'g_intro':g_intro
                       }],ignore_index=True)
        else:# html.status_code!=200, no #1. executed
            print(html) #like 400/404/...
        
        #2.from html to new urls to wait_que
        if stop_sign == 0:
            abs_url = re.findall('http://www.4399.com/flash/[0-9_]+\.htm',html.text)
            rel_url = re.findall('/flash/[0-9_]+\.htm',html.text)
            all_url = ['http://www.4399.com'+x for x in rel_url] + abs_url
            for i in all_url:
                if i not in parsed_list:
                    if wait_que.qsize() < wait_que.maxsize:
                        wait_que.put(i)
                        parsed_list.append(i)
                    else:
                        stop_sign = Integer(1)
                        break
        else:
            pass #once reached max, never execute step #2.
        # end #2.
    #------------end bfs--------------
    return df #内部变量做拷贝?
         
if __name__ == '__main__':
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.3\
6 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36 SE 2.X MetaSr 1.0'}
    seed = 'http://www.4399.com/flash/1.htm'
    df = frontier_extend(seed=seed,headers=headers)
    print(df)
    df.to_excel("C:/Users/asus-pc/Desktop/4399.xlsx")
