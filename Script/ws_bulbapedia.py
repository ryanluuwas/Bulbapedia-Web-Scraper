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

# Start of Script
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
for x in pokeList[:5]: #Pokemon total 953
    p_url = x
    response = requests.get(p_url)
    p_page = response.text
    p_soup = BeautifulSoup(p_page, 'html.parser')

    #Find pokemon dex number
    no.append(p_soup.th.big.a.span.text)

    #Find pokemon name
    name.append(p_soup.div.p.b.text)
    #print(str(timer) + " " + (p_soup.div.p.b.text))
    timer = timer + 1

    #Find Generation
    g = p_soup.select( 'ul li span a[class*="external text"] ' )
    g = BeautifulSoup(str(g)).get_text()
    g = g[:-1][1:]
    g = g.split(",")
    generation.append(g[0])

    #Find typing
    t = p_soup.select( 'td a[href*="(type)"] span b' )
    t = BeautifulSoup(str(t)).get_text()
    t = t[:-1][1:]
    t = t.split(",")
    primary.append(t[0])
    secondary.append(t[1])

    '''
    Work-in-progress
    #Finding Default and Hidden Ability
    a = p_soup.select( 'td a[href*="(Ability)"] span' )
    a = BeautifulSoup(str(a)).get_text()
    a = a[:-1][1:]
    a = a.split(",")
    abil.append(a[0])
    habil.append(a[3])
    '''

    #Find stats
    stats = p_soup.findAll('th', attrs = {'style':['width:85px; padding-left:0.5em; padding-right:0.5em']})
    stats = ([x.text for x in stats])

    #Keep only the stats numbers and store into a list
    store = []
    for x in stats:
        store.append(re.findall(r'[0-9]?[0-9]?[0-9]', x))

    #Removing brackets and converting stats into integer
    holder = []
    for x in store:
        x = int((str(x))[:-2][2:])
        holder.append(x)

    #Store stats into appropriate list
    hp.append(holder[0])
    atk.append(holder[1])
    defense.append(holder[2])
    spatk.append(holder[3])
    spdef.append(holder[4])
    spd.append(holder[5])
    bst.append(holder[6])

pokemon = {'Dex No.': no,
           'Name': name,
           'Generation':generation,
           'Primary Type': primary,
           'Secondary Type': secondary,
           #'Ability': abil,
           #'Hidden Ability': habil,
           'Health':hp,
           'Attack':atk,
           'Defense':defense,
           'Sp. Attack':spatk,
           'Sp. Defense':spdef,
           'Speed':spd,
           'BST':bst
          }

#Create Dataframe
df=pd.DataFrame.from_dict(pokemon)

#Data Cleaning
df.loc[779:869,'Generation'] = 'Generation VII'
df.loc[870:951,'Generation'] = 'Generation VIII'
df.drop_duplicates()

#Write Csv
df.to_csv('bulbapedia_data.csv', index = None, header = True) 
