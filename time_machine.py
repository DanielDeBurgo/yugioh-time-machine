from bs4 import BeautifulSoup
import requests
import random
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("year", help="The year you wish to travel back to (2005-2016 inclusive)", type=int)
args = parser.parse_args()
year = args.year
if year > 2004 and year < 2017:
    page = requests.get("https://yugiohtopdecks.com/?start_date=01%2F01%2F{0}&end_date=01%2F01%2F{1}".format(year, year + 1)).text

    soup = BeautifulSoup(page, 'html.parser')

    domain = "https://yugiohtopdecks.com"
    decks_are_good = False

    while not decks_are_good:
        links = []
        for deck in soup.find_all('a', href=True):
            if deck['href'].startswith('/decks/'):
                links.append(domain + deck['href'])

        P1_link, P2_link = random.sample(links, 2)

        pageP1 = requests.get(P1_link).text
        pageP2 = requests.get(P2_link).text
        pageP1Soup = BeautifulSoup(pageP1, 'html.parser')
        pageP2Soup = BeautifulSoup(pageP2, 'html.parser')
        P1_decks = []
        P2_decks = []

        for row in pageP1Soup.find_all('tr'):
            first = True
            add = False
            for link in row.find_all('a', href=True):
                if first:
                    first = False
                    if link['href'].endswith(str(year)):
                        add = True
                elif add:
                    if link['href'].startswith("/deck/"):
                        P1_decks.append(domain+link['href'])

        for row in pageP2Soup.find_all('tr'):
            first = True
            add = False
            for link in row.find_all('a', href=True):
                if first:
                    first = False
                    if link['href'].endswith(str(year)):
                        add = True
                elif add:
                    if link['href'].startswith("/deck/"):
                        P2_decks.append(domain+link['href'])

        if len(P1_decks) != 0 and len(P2_decks) != 0:
            decks_are_good = True
            PageP1DeckSoup = BeautifulSoup(requests.get(random.sample(P1_decks, 1)[0]).text, 'html.parser')
            PageP2DeckSoup = BeautifulSoup(requests.get(random.sample(P2_decks, 1)[0]).text, 'html.parser')
            for link in PageP1DeckSoup.find_all('a', href=True):
                if link['href'].startswith("/ygopro_deck/"):
                    print("Deck P1 Downloaded")
                    r = requests.get(domain + link['href'], allow_redirects=True)
                    open('P1.ydk', 'wb').write(r.content)
            for link in PageP2DeckSoup.find_all('a', href=True):
                if link['href'].startswith("/ygopro_deck/"):
                    print("Deck P2 Downloaded")
                    r = requests.get(domain + link['href'], allow_redirects=True)
                    open('P2.ydk', 'wb').write(r.content)
        if year < 2008:
            print("MASTER RULES: 1")
        elif year < 2014:
            print("MASTER RULES: 2")
        else:
            print("MASTER RULES: 3")
else:
    print("Please give a year between 2005 and 2016 inclusive")