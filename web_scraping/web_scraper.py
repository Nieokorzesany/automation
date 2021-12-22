import requests
from bs4 import BeautifulSoup



content = ''

def extract_news(url):
    print('extracting')
    cnt = ''
    cnt+=('<b>HN Top Stories:>/b>\n'+'<br>'+'-'*50+'<br>')
    response = requests.get(url)
    content=response.content
    soup = BeautifulSoup(content,'html.parser')
    test = soup.findAll('div',class_='central-featured-lang')
    
    for i,div in enumerate(test):

        print(list(div)[1].get('title')+' : '+ 'https:'+list(div)[1].get('href'))
    

cnt= extract_news('https://www.wikipedia.org/')