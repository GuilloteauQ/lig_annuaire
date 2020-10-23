import requests
import base64
import sys
from tabulate import tabulate
from bs4 import BeautifulSoup


url = "https://www.tutorialspoint.com/index.htm"
req = requests.get(url)
URL="http://www.liglab.fr/fr/util/annuaire"




class Person:
    def __init__(self, soup):
        self.soup = soup
        self.get_name()
        self.get_equipe()
        self.get_email()
        self.get_location()
        self.get_bureau()

    def get_name(self):
        self.name = self.soup.find("td", {"class": "civilite"}).find_all('b')[0].text.strip()

    def get_equipe(self):
        self.equipe = self.soup.find("td", {"class": "civilite"}).find_all('a')[0].text.strip()

    def get_email(self):
        self.email = str(base64.b64decode(self.soup.find("a", {"target": "_blank"})["onclick"][20:-2]), "utf-8")

    def get_location(self):
        self.location = self.soup.find("div", {"class": "details"}).find_all('a')[0].text.strip()

    def get_bureau(self):
        lignes = self.soup.find("div", {"class": "details"}).text.split("\n")
        for l in lignes:
            ligne = l.strip()
            if len(ligne) != 0:
                if ligne[0:8] == "Bureau :":
                    self.bureau = ligne[9:-1]
                    return
        self.bureau = ""

    def __str__(self):
        data_to_print = [[self.name, self.equipe, self.email, self.bureau, self.location]]
        return str(tabulate(data_to_print, headers = ["Name", "Team", "Email", "Office", "Location"]))
        # return "{} ({}): {} -> {} ({})".format(self.name, self.equipe, self.email, self.bureau, self.location)


def get_result(nom, prenom):
    myobj = {'nom': nom, 'prenom': prenom, 'rechercher': 'Rechercher', 'form_build_id': 'form-JX5EjuCiVMGS2PhzYD5Mf2UiNGVidpmsko0tCeAAkJ4', 'form_id': 'lig_ose_annuaire_form'}

    x = requests.post(URL, data = myobj)

    return x.text

def get_data(text):
    soup = BeautifulSoup(text, "html.parser")
    return soup.find("div", {"class": "fiche_membre"})


def main():
    args = sys.argv
    if len(args) <= 1 or len(args) > 3:
        print("Usage: lig [LAST_NAME] [FIRST_NAME]")
        return 1

    nom = str(args[1])
    if len(args) == 3:
        prenom = str(args[2])
    else:
        prenom = "*"


    soup = get_data(get_result(nom, prenom))
    me = Person(soup)
    print(me)
    return 0

if __name__ == "__main__":
    main()