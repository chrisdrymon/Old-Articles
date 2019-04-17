from bs4 import BeautifulSoup
import requests
import pandas as pd

addresses = pd.read_csv('/home/chris/Desktop/GetURLs.csv')
deckDict = {}
i = 1
for label, value in addresses.iteritems():
    for address in value:
        try:
            source = requests.get(address[29:73]).text
            deckName = address[67:73]
            soup = BeautifulSoup(source, 'lxml')
            cardList = soup.find('ul', class_='deckList')
            gameList = soup.find('ul', class_='matches-list')
            deckScore = soup.find('section', class_='arenaDeckTierscore').find('span').text
            wins = soup.find('span', class_='wins').text
            archetype = soup.find('header', class_='deck-archetype-name').find('span')
            archetype = str(archetype)
            deckType = archetype[6:]
            archetype = deckType.split('<br/>')[0]
            deck = []
            quantity = []
            hsClass = soup.title.text.split()[0]

            for card in cardList.find_all('span', class_='name'):
                deck.append(card.text)

            for card in cardList.find_all('span', class_='quantity'):
                quantity.append(card.text)

            deckDict[deckName] = [hsClass, deckScore, archetype, deck, quantity, wins]
            df = pd.DataFrame(deckDict).T
            df.to_csv('/home/chris/Desktop/decks.csv')
            print('Deck', i, 'scraped.')
            i += 1
        except AttributeError:
            pass

print(df)
