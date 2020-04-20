import urllib.request
from bs4 import BeautifulSoup
import re

with open("taboo_cards.tsv", "a") as f:
    while True:
        contents = urllib.request.urlopen("http://playtaboo.com/ajax/v1/next").read()
        soup = BeautifulSoup(contents)
        word_to_guess = soup.find_all("h2", text=True)[0].getText().lower()
        forbidden_words = soup.find_all("li", text=True)
        to_write = word_to_guess.strip() + "\t" + "\t".join([f.getText().lower().strip()
                                                             for f in forbidden_words])
        print(to_write)
        f.write(to_write + "\n")
