import requests
import base64
import sys
from tabulate import tabulate
from bs4 import BeautifulSoup


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

    def data_to_print(self):
        return [[self.name, self.equipe, self.email, self.bureau, self.location]]


def tabulate_print(data_to_print):
    print(tabulate(data_to_print, headers = ["Name", "Team", "Email", "Office", "Location"]))

def get_result(nom, prenom=''):
    myobj = {'nom': nom, 'prenom': prenom, 'rechercher': 'Rechercher', 'form_build_id': 'form-JX5EjuCiVMGS2PhzYD5Mf2UiNGVidpmsko0tCeAAkJ4', 'form_id': 'lig_ose_annuaire_form'}
    x = requests.post(URL, data = myobj)
    return x.text

def get_data(text):
    soup = BeautifulSoup(text, "html.parser")
    return soup.find("div", {"class": "fiche_membre"})


def main():
    args = sys.argv
    if len(args) <= 1:
        print("Usage: lig LAST_NAME")
        return 1


    nom = ' '.join(args[1:])

    text = get_result(nom)
    soup = BeautifulSoup(text, "html.parser")

    # We look for multiple results
    even_names = [person_tr.find_all('td')[1].text for person_tr in soup.find_all("tr", {"class": "even"})]
    odd_names = [person_tr.find_all('td')[1].text for person_tr in soup.find_all("tr", {"class": "odd"})]
    all_names = even_names + odd_names
    # If there are some
    if len(all_names) > 0:
        to_print = [ ]
        for first_name in all_names:
            to_print += Person(get_data(get_result(nom, first_name))).data_to_print()
        tabulate_print(to_print)
        return 0

    soup = soup.find("div", {"class": "fiche_membre"})
    # If there are no result
    if soup is None:
        print("No result for '{}'".format(nom))
    else:
        me = Person(soup)
        tabulate_print(me.data_to_print())
    return 0

if __name__ == "__main__":
    main()
