#!/usr/bin/env python3
from bs4 import BeautifulSoup
import requests
import csv
import bs4
import codecs
import enchant

def check_link(url):
    try:
        
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print('Connected falied！！！')


def get_contents(urlist):
    '''urlist: a list containing all the useful urls'''
    result = []
    for url in urlist:
        content = check_link(url)
        soup = BeautifulSoup(content,'lxml')
        trs = soup.find_all('tr')
        for tr in trs:
            ui = []
            for td in tr:
                ui.append(td.string)
            result.append(ui)
    return result


def get_urls(url_content,root_url="https://www.shanbay.com"):
    ulist = []
    soup = BeautifulSoup(url_content,'lxml')
    urls=soup.find_all('a')  
    for url in urls:  
        try:
            if url.string.startswith('【无老师7天TOEFL】List'):
                ulist.append(root_url+url.get('href'))
                for j in range(2,11):
                    extend_url = root_url+url.get('href')+'?page='+str(j)
                    ulist.append(extend_url)
        except:
            pass
    return ulist


   
def save_contents(result):
    d = enchant.Dict("en_US")
    with codecs.open('tofel.csv', 'w','utf_8_sig') as f:
        writer = csv.writer(f)
        for i in range(len(result)):
        #    print(result[i][1])W
            try:
                if d.check(''.join(result[i][1])):   
                    writer.writerow([result[i][1],result[i][3]])
                    print("write in line:",i)
            except:
                print("error in line:{}, contents is:{}".format(i,result[i]))
                return



def main():
    src_url = "https://www.shanbay.com/wordbook/5440/"
    src_content = check_link(src_url)
    urls = get_urls(src_content)

    result = get_contents(urls)
    save_contents(result)

main()