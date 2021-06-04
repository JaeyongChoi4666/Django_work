'''
Created on 2021. 6. 4.

@author: ADMIN
'''
import requests
from bs4 import BeautifulSoup

def movie_crawling(data):
    for i in range(101):
        base_url='https://movie.naver.com/movie/point/af/list.nhn?page='
        url=base_url+str(i+1)
        req=requests.get(url)
        
        if req.ok:
            