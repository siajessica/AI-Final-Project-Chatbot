import requests
import time
from bs4 import BeautifulSoup

url = "https://www.taiwannews.com.tw/en/search?keyword=Covid%20contacts"

req = requests.get(url)
soup = BeautifulSoup(req.text, 'html5lib')

news = soup.body.find('section', attrs={'class': 'mod_search-items'})
# print(latest)

title = news.a['title']
# print(title)

country = 'Taiwan'
keywords = ['COVID', 'quarantine', 'quarantine rules', 'COVID contacts', 'home isolation']

related = 0
for words in keywords:
    if (country in title) and (words in title):
        related = 1
        break

if related == 1:
    article_url = "https://www.taiwannews.com.tw" + news.a['href']
    print(article_url)
    req_article = requests.get(article_url)
    soup_article = BeautifulSoup(req_article.text, 'html5lib')
    content = soup_article.body.find('div', attrs={'itemprop': "articleBody"})
    date = soup_article.body.find('div', attrs={'class': "article-date"})
    # print(date.get_text())
    date = date.get_text()
    content = content.span
    p_tags = content.find_all('p')
    paragraph = ''
  
    for p in p_tags:
        paragraph += p.string.strip()
    # print(paragraph)

    with open("covid_info.txt", 'r+', encoding='utf-8') as corpus:
        content = corpus.read()
        corpus.seek(0, 0)
        corpus.write(date + '\n' + paragraph + '\n' + content)

