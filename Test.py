import pandas as pd
import requests

df = pd.read_csv('/home/chris/Desktop/datedURLs2.csv')
addresses = df['Address']
newAdList = []
for address in addresses:
    print(address[38:44])
