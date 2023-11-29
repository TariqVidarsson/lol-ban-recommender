from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import html5lib
import pandas as pd
from selenium import webdriver

#function that scrapes u.gg for 
def character_matchup_chart(character,role,rank):
    driver =webdriver.Chrome()
    if rank=='none':
        url = 'https://u.gg/lol/champions/{}/matchups?role={}'.format(character,role)
    else:
        url = 'https://u.gg/lol/champions/{}/matchups?rank={}&role={}'.format(character,rank,role)
    driver.get( url)
    js_content= driver.page_source
    soup = BeautifulSoup(js_content, 'html.parser')
    quote = soup.find("div", class_="content-section ReactTable ugg-table-2 matchups-table scrollable-table")
    champs = []
    win_rate = []
    for data in quote.text.split('%')[:-1]:
        win_rate.append(float(data[-5:]))
        champ = ''
        for index in data[::-1][5:]:
            if index.isnumeric():
                champs.append(champ)
                break
            else:
                champ = index + champ
    return pd.Series(win_rate, index = champs)

characters = []
counter = 1
while True:
    inp = input("Input Champion #{}. If no more champions type 'NONE' \n".format(counter))
    if inp.lower() == 'none':
        break 
    else:
        characters.append(inp.lower())
        counter += 1
while True:
    rank = input("Which rank are you in? Choose from 'iron', ,'bronze','silver', 'gold', 'platinum', 'emerald', 'diamond', 'master','grandmaster' or 'challenger'.If you do not care type none \n").lower()
    if rank not in ['iron','bronze', 'silver', 'gold', 'platinum', 'emerald', 'diamond', 'master','grandmaster', 'challenger','none']:
        print('The rank provided is not listed above. Please name a rank from those listed or NONE if you do not care. \n')
    else:
        break
while True:
    role = input("Which role are you playing? Choose from 'top', 'middle', 'adc', 'support', or 'jungle' \n").lower()
    if role not in ['top', 'middle', 'adc', 'support', 'jungle']:
        print('The role provided is not listed above. Please name a role from those listed. \n')
    else:
        break
win_rates = []
for character in characters:
    win_rates.append(character_matchup_chart(character,role,rank))
for index in range(len(win_rates)):
    if index == 0:
        continue
    else:
        win_rates[0]=win_rates[0].add(win_rates[index])
print(win_rates[0].idxmin())
