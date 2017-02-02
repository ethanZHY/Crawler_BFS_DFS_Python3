import time
from collections import deque
import requests
from bs4 import BeautifulSoup
import re



seed_url = "https://en.wikipedia.org/wiki/Sustainable_energy"

# result set
result_urls = []
title_list = []

temp_urls = deque([])



# Because the keyword maintains in the whole process, I simply make a local variable to hold it
# instead of passing it as an argument
def DFS_crawler(arg_url, depth):

    source_code = requests.get(arg_url).text
    soup = BeautifulSoup(source_code, "html.parser")
    content = soup.find('div', {'id': 'mw-content-text'})
    title = soup.find('h1', {'id':'firstHeading'} and {'class':'firstHeading'})
    print(depth)

    for item in content.findAll('a', {'title': True} and {'class': False}):

        if ('#' not in item.get('href')) and item.get('href').startswith('/wiki/') \
        and not item.get('href').startswith('/wiki/Category:') \
        and not item.get('href').startswith('/wiki/File:') \
        and not item.get('href').startswith('/wiki/Template:') \
        and not item.get('href').startswith('/wiki/Book:') \
        and not item.get('href').startswith('/wiki/Help:') \
        and not item.get('href').startswith('/wiki/Portal:') \
        and not item.get('href').startswith('/wiki/Template_talk:') \
        and not item.get('href').startswith('/wiki/Talk:'):
            url = "https://en.wikipedia.org" + item.get('href')
            keyword = "solar"
            if re.search(keyword, url, re.IGNORECASE) and title not in title_list:
                DFS_visit(url, depth)
    output_urls(result_urls)



def DFS_visit(arg_url, depth):

    if (len(result_urls) == 1000):
        return 0

    depth += 1

    if depth < 6:
        print('depth:', depth)
        time.sleep(1)
        source_code = requests.get(arg_url).text
        soup = BeautifulSoup(source_code, "html.parser")
        content = soup.find('div', {'id': 'mw-content-text'})
        title = soup.find('h1', {'id': 'firstHeading'} and {'class': 'firstHeading'})

        for item in content.findAll('a', {'title': True} and {'class': False}):

            if ('#' not in item.get('href')) and item.get('href').startswith('/wiki/') \
            and not item.get('href').startswith('/wiki/Category:') \
            and not item.get('href').startswith('/wiki/File:') \
            and not item.get('href').startswith('/wiki/Template:') \
            and not item.get('href').startswith('/wiki/Book:') \
            and not item.get('href').startswith('/wiki/Help:') \
            and not item.get('href').startswith('/wiki/Portal:') \
            and not item.get('href').startswith('/wiki/Template_talk:') \
            and not item.get('href').startswith('/wiki/Talk:'):
                url = "https://en.wikipedia.org" + item.get('href')
                keyword = "solar"
                if re.search(keyword, url, re.IGNORECASE) and title not in title_list:
                    if depth < 6 :
                        DFS_visit(url, depth)
                    if len(result_urls) < 1000 and url not in result_urls:
                        result_urls.append(url)
                        print(url)
                        print(len(result_urls))
                        addVisited_url(url)




    return 0

# The way here to solve the problem, different urls point to the same page, is to check the title of each page
# correspond to each URL.

def addVisited_url(arg_url):
    time.sleep(1)
    source_code = requests.get(arg_url).text
    soup = BeautifulSoup(source_code, "html.parser")
    title = soup.find('h1', {'id': 'firstHeading'})
    title_list.append(title)

# write urls into text file
def output_urls(urls):
    file_loc = r'Task_2_B.txt'
    fx = open(file_loc,"w")
    for url in urls:
        fx.write(url + '\n')
    fx.write('\n' + "Num of Urls: " + str(len(urls)) + '\n')
    fx.close()



DFS_crawler(seed_url, 1)
