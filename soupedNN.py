from bs4 import BeautifulSoup
import requests

with open('HearthArena.html') as html_file:
    soup = BeautifulSoup(html_file, 'lxml')

i = 1
cardList = soup.find('ul', class_='deckList')
for card in cardList.find_all('span', class_='name'):
    print(i, card)
    i += 1
#card = match.span
#print(cardList.prettify)

for card in cardList.find_all('span', class_='quantity'):
    print(i, card)
    i += 1
