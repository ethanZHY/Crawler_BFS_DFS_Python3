import time
from collections import deque
import requests
from bs4 import BeautifulSoup
import os


# for task 3 just change this http below to "https://en.wikipedia.org/wiki/Solar_power"
seed_url = deque(["https://en.wikipedia.org/wiki/Sustainable_energy"])

# a queue to store the acquired url


# result set
result_urls = []
title_list = []
temp_urls = deque([])

#global counter
global depth
depth = 0



def BFS_crawler(arg_url):
    depth = 1
    urls = arg_url
    while depth < 6:
        while (len(urls)) != 0 and len(result_urls) < 1000:
            # dequeue a url
            current_url = urls.popleft()
            time.sleep(1)
            source_code = requests.get(current_url).text
            soup = BeautifulSoup(source_code, "html.parser")
            content = soup.find('div', {'id': 'mw-content-text'})

            for item in content.findAll('a', {'title': True} and {'class': False}):
                if ('#' not in item.get('href')) and item.get('href').startswith('/wiki/') \
                        and not item.get('href').startswith('/wiki/Category:') \
                        and not item.get('href').startswith('/wiki/File:') \
                        and not item.get('href').startswith('/wiki/Template:') \
                        and not item.get('href').startswith('/wiki/Book:') \
                        and not item.get('href').startswith('/wiki/Portal:') \
                        and not item.get('href').startswith('/wiki/Help:') \
                        and not item.get('href').startswith('/wiki/Template_talk:') \
                        and not item.get('href').startswith('/wiki/Talk:'):
                    url = "https://en.wikipedia.org" + item.get('href')
                    if len(result_urls) < 1000 and url not in result_urls:
                        result_urls.append(url)
                        temp_urls.append(url)

                        #download the html file, if you want it, uncomment the following func-call
                        #download_html(url,item.string)

                        print(url)
                        print(len(result_urls))
        urls = temp_urls
        depth += 1
    output_urls(result_urls)


def output_urls(urls):
    file_loc = r'Task_1.txt'
    fx = open(file_loc,"w")
    for url in urls:
        fx.write(url + '\n')
    fx.write('\n' + "Num of URLs: " + str(len(urls)) + '\n')
    fx.close()

#download web source code
def download_html(arg_url, filename):
    time.sleep(1)
    source_code = requests.get(arg_url).text
    soup = BeautifulSoup(source_code, "html.parser")
    lines = str(soup).split("\n")
    if not os.path.exists('urls'):
        os.mkdir('urls')
    file_loc =  r'urls/' + filename + '.txt'
    fx = open(file_loc, "w")
    fx.write(arg_url+ '\n')
    fx.write('=======================================\n')
    for line in lines:
        fx.write(line + '\n')
    fx.close()




BFS_crawler(seed_url)
