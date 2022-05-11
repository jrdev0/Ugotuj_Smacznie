from bs4 import BeautifulSoup
import requests

#przepis_do_wyszukania = input('Czego szukasz do zjedzenia?: ')

def wyszukiwarka_przepisow(przepisek):
    global tytul_przepisu
    tytul_przepisu = przepisek
    headers = {'User_Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0'}
    wyszukaj = f'https://www.kwestiasmaku.com/szukaj?search_api_views_fulltext={przepisek}'
    r = requests.get(wyszukaj, headers)
    soup = BeautifulSoup(r.content, 'html.parser')

    return soup


def dane_przepisow(soup):
    lista_przepisow = []
    licznik = 0
    przepisy = soup.find_all('div', class_='node')

    for p in przepisy:
        if licznik != '3':

            nazwa_dania = p.find('h2').text
            oc = str(p.find('div', class_='star-1')).split('>')[2:-2][0].replace("['", " ")
            ocena = str(oc).split('<')[0][0:3]


            ilosc_oc = str(p.find('span', class_='fivestar_votes_count')).split('>')[1]
            ilosc_ocen = ilosc_oc.split('<')[0]

            try:
                podtyt = str(p.find('h2', class_='field-name-field-podtytul')).split('>')[1]
                podtytu = str(podtyt.split(' ')[4:-2])
                podtytul = podtytu.replace("'", " ").replace(",", " ").replace("    ", " ")[1:-1]

            except IndexError or ValueError or KeyError:
                podtytul = 'brak'
            link = p.find('a')
            link_do = str(link)
            link_do_p = link_do.split('"')[1]
            link_do_przepisu = 'https://www.kwestiasmaku.com' + link_do_p

         #   print('Nazwa dania:', nazwa_dania)
           # print('Nagłówek: ', podtytul)
          #  print(f'Ocena: {ocena} z {ilosc_ocen} opini')
          #  print(link_do_przepisu)
            if podtytul == 'brak':
                dupa = {

                    'Danie': nazwa_dania,
                    'Ocena': ocena + ' z ' + ilosc_ocen + ' opini'
            }
            else:
                dupa = {
                    'Danie': nazwa_dania,
                    'Nagłówek': podtytul,
                    'Ocena': ocena + ' z ' + ilosc_ocen + ' opini'
                }
            lista_przepisow.append(dupa)
            licznik += 1

        else:
            break
    return lista_przepisow


def osobny_przepis(soup):
    lista_przepisow = []
    licznik = 0
    przepisy = soup.find_all('div', class_='node')

    for p in przepisy:
        if licznik != '3':
            link = p.find('a')
            link_do = str(link)
            link_do_p = link_do.split('"')[1]
            link_do_przepisu = 'https://www.kwestiasmaku.com' + link_do_p
            dupa = {
                  'Link': link_do_przepisu
            }
            lista_przepisow.append(dupa)
            licznik += 1
        else:
            break
    return lista_przepisow


def wykonanie(przepisek):

    znajdz = wyszukiwarka_przepisow(przepisek)
    wyniki = dane_przepisow(znajdz)

    return wyniki




def drukowanie_linku(przepisek, wybor):
    wykonanie_l = wyszukiwarka_przepisow(przepisek)
    wyniki = osobny_przepis(wykonanie_l)
    # Dostep do linku [zamiast 2 jest opcja wyboru

    link = str(wyniki[wybor]).split("'")[3]
    headers = {'User_Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0'}
    wyszukaj = f'{link}'
    #print('Pobrany link', wyszukaj)
    print('')

    r = requests.get(wyszukaj, headers)
    soup = BeautifulSoup(r.content, 'html.parser')

    return soup


def wykonanie_linku(soup):
    szczegoly_przepisu = soup.find_all('div', class_='row row-2')

    for wynik in szczegoly_przepisu:
        skladniki = wynik.find('ul').text
        skladniki =  skladniki.replace("\n\t\t", "") + '\n'
        przygotowanie = str(wynik.find('div', class_='col-xs-12 col-sm-8 col-md-8').text)
        przygotowanie = przygotowanie.replace("\n\t", "").strip().replace("Dodaj notatkę", "").replace('\t', '').replace('  ', '').replace('\xa0',' ') + '\n'
        lista = []
        lista.append(str(przygotowanie))
        print(lista)
        naglowek = f'{str(tytul_przepisu).upper()} \n\n'
        with open('przepis.txt', 'w+') as f:
            f.write(naglowek)
        with open('przepis.txt', 'a+') as f:
            f.write(skladniki)
        with open('przepis.txt', 'a+') as f:
            f.write(przygotowanie)
        return skladniki, przygotowanie




dr = drukowanie_linku('zupa krupnik', 1)
print(wykonanie_linku(dr)[0])
print(wykonanie_linku(dr)[1])
