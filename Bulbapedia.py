#Packages
from bs4 import BeautifulSoup
import urllib
import re
import pandas as pd
import numpy as np
import requests
from urllib.request import urlopen
import csv

#Set-up
url = "https://bulbapedia.bulbagarden.net/"
pageurl = url + "wiki/List_of_Pokémon_by_National_Pokédex_number"
response = requests.get(pageurl)

pokeList = []

page = response.text
soup = BeautifulSoup(page, 'html.parser')

all_matches = soup.find_all('table', attrs={'align':['center']})
for i in all_matches:
    list = ([a.attrs.get('href') for a in soup.select('table[align="center"] td a[title*="Pok"]')])
    for x in list:
        pokeList.append(url + x)

for x in pokeList:
    print(x)

#List
no = []
name = []
generation = []
abil = []
habil = []
primary = []
secondary = []
hp = []
atk = []
defense = []
spatk = []
spdef = []
spd = []
bst = []

timer = 1

#Scraping Bulbapedia
for x in pokeList[:952]: #Pokemon total 952
    p_url = x
    response = requests.get(p_url)
    p_page = response.text
    p_soup = BeautifulSoup(p_page, 'html.parser')

    #Find pokemon dex number
    no.append(p_soup.th.big.a.span.text)
    #print(no)

    #Find pokemon name
    name.append(p_soup.div.p.b.text)
    print(str(timer) + " " + (p_soup.div.p.b.text))

    #Loop Number
    timer = timer + 1


    #Find typing
    store = []
    typing = p_soup.select( 'td a[href*="(type)"] span b' )
    #print(typing)

    #Convert the 'typing' bs4 tag into string and place into store and remove <b> tag. Add value into store
    for x in typing:
        x = str(x)
        x = x[:-4]
        x = x[3:]
        store.append(x)

    primary.append(store[0])
    secondary.append(store[1])

    #Finding Default and Hidden Ability
    store = []
    ability = p_soup.select( 'td a[href*="(Ability)"] span' )

    for x in ability:
        x = str(x)
        x = x[:-7]
        x = x[26:]
        store.append(x)

    abil.append(store[0])
    habil.append(store[3])


    #Find stats
    stats = p_soup.findAll('th', attrs = {'style':['width:85px; padding-left:0.5em; padding-right:0.5em']})
    stats = ([x.text for x in stats])
    #print(stats)

    #Keep only the stats numbers and store into a list
    store = []
    for x in stats:
        store.append(re.findall(r'[0-9]?[0-9]?[0-9]', x))

    #print(store)

    #Removing brackets and converting stats into integer
    holder = []
    for x in store:
        x = str(x)
        x = (x[:-2])
        x = (x[2:])
        x= int(x)
        holder.append(x)

    #Store stats into appropriate list
    hp.append(holder[0])
    atk.append(holder[1])
    defense.append(holder[2])
    spatk.append(holder[3])
    spdef.append(holder[4])
    spd.append(holder[5])
    bst.append(holder[6])

    #Generation
    store = []
    g = p_soup.select( 'td a[href*="/wiki/Generation"] span' )
    for x in g:
        x = str(x)
        x = x[:-7]
        x = x[26:]
        store.append(x)

    generation.append(store[0])


pokemon = {'Dex No.': no,
           'Name': name,
           'Generation':generation,
           'Primary Type': primary,
           'Secondary Type': secondary,
           'Ability': abil,
           'Hidden Ability': habil,
           'Health':hp,
           'Attack':atk,
           'Defense':defense,
           'Sp. Attack':spatk,
           'Sp. Defense':spdef,
           'Speed':spd,
           'BST':bst
          }

#Write to CSV
df=pd.DataFrame.from_dict(pokemon)
df.to_csv (r'C:\Users\Ryan Luu\Desktop\Pokemon Project\pokemon_data.csv', index = None, header=True)
