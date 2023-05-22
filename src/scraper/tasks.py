from celery import shared_task
from games.models import Game, GameData
from django.utils.text import slugify
from django.utils import timezone

from bs4 import BeautifulSoup
import os
import time
import requests
import yaml
import pandas as pd
import re
import random

import logging


@shared_task
def add(x, y):
    return x + y

@shared_task
def get_data():
    logger = logging.getLogger(__name__)
    logger.info("Starting scraping task")
    start_time = time.time()
    date = timezone.now().date()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    headers_file_path = os.path.join(script_dir, "files/headers.yml")

    with open(headers_file_path) as f_headers:
        browser_headers = yaml.safe_load(f_headers)
    headers = browser_headers["Chrome"]
    def get_good_proxies(u):
        good_proxies = set()
        while len(good_proxies) <= 0 :
            response = requests.get("http://free-proxy-list.net/")
            proxy_list = pd.read_html(response.text)[0]
            proxy_list['url'] = "http://" + proxy_list['IP Address'] + ":" + proxy_list['Port'].astype(str)
            https_proxies = proxy_list[proxy_list["Https"] == "yes"]
            https_proxies.count()
            length = len(https_proxies)
            j = 0
            print(f"Found {length} proxies")
            for proxy_url in https_proxies["url"]:
                j += 1
                proxies = {
                    "http": proxy_url,
                    "https": proxy_url,
                }
                try:
                    response = requests.get(u, headers=headers, proxies=proxies, timeout=random.randint(2, 5))
                    if response.ok:
                        good_proxies.add(proxy_url)
                        print(f"{j}/{length} - Proxy {proxy_url} OK , {len(good_proxies)}")
                    else :
                        print(f"{j}/{length} - Proxy {proxy_url} BAD, {response.status_code}")
                except Exception:
                    print(f"{j}/{length} - Proxy {proxy_url} BAD")
                    pass
                # if len(good_proxies) >= 2 :
                #     break
        return good_proxies

    i = limit = 1

    while i <= 160:
        url = f"https://www.instant-gaming.com/fr/rechercher/?type%5B0%5D=pc&page={i}"
        print(f"Scraping page {i} : ")
        if limit == i:
            good_proxies = get_good_proxies(url)
        else :
            limit = i
        for browser, headers in browser_headers.items():
            if limit != i:
                break
            print(f"\n\nUsing {browser} headers\n")
            for proxy_url in good_proxies:   
                proxies = {
                    "http": proxy_url,
                    "https": proxy_url,
                }
                time.sleep(0.2)
                print(f"Scraping page {i} : started")
                try:
                    response = requests.get(url, headers=headers, proxies=proxies, timeout=random.uniform(2.5, 10.0))
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.text, 'html.parser')
                        infos = soup.findAll('div', {'class': ["item", "force-badge"]})
                        print(f'{len(infos)} items scraped.')
                        j = 0
                        for info in infos:
                            j += 1
                            name = info.find('div', {'class': 'name'})
                            if (name == None) :
                                name = None
                            else :
                                name = name.text
                                if "DLC" in name:
                                    type = "DLC"
                                else :
                                    type = "Game"
                                name = name.replace("DLC", "").replace("\n", "")

                            price = info.find('div', {'class': 'price'})
                            if (price == None) :
                                price = '0'
                            else :
                                price = rf"{price.text}"
                                price = re.sub(r"[^\d\.]", "", price)

                            discount = info.find('div', {'class': 'discount'})
                            if (discount == None) :
                                discount = '0'
                            else :
                                discount = discount.text
                                discount = discount.replace("%", "")

                            image = info.find('img', {'class': 'picture'})
                            if (image == None) :
                                image = ''
                            else :
                                image = image['data-src']

                            link = info.find('a', {'class': ['cover', 'video']})
                            if (link == None) :
                                link = info.find('a', {'class': ['cover']})
                            elif (link == None) :
                                link = '#'
                            else :
                                link = link['href']

                            if name:
                                slug = slugify(name)
                                item = {
                                    "name": name, 
                                    'slug': slug,
                                    "type": type,
                                    'description': '',
                                    'shop': 'Instant Gaming',
                                    "link": link,
                                    "image": image
                                }
                                print(f'Game slug is {slug}')
                                game = Game.objects.filter(slug=item["slug"]).first()

                                if not game:
                                    game = Game.objects.create(**item)


                                game_data_exists = GameData.objects.filter(game=game, date__date=date).exists()
                                if not game_data_exists:
                                    data = {
                                        "game": game,
                                        "price": price,
                                        "discount": discount,
                                    }
                                    GameData.objects.create(**data)
                                else:
                                    print(f"Game {game.name} already exists for {date}")
                                    pass
                                print(f"{j}/{len(infos)} - {name} scraped.")
                        print(f"Page {i} scraped, files saved.")
                        i += 1
                        url = f"https://www.instant-gaming.com/fr/rechercher/?type%5B0%5D=pc&page={i}"
                        print('\n\n-------------------------\n\n')
                    break
                except Exception as e:
                    print(f"Erreur : {e}")
                    print(f"Scraping page {i} : Proxy {proxy_url} failed, trying another one.")

    end_time = time.time()
    elapsed_time = end_time - start_time
    formatted_elapsed_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
    print(f"Temps d'exécution : { formatted_elapsed_time }")

    return f"Temps d'exécution : { formatted_elapsed_time }"


@shared_task
def get_data_without_proxy():
    logger = logging.getLogger(__name__)
    logger.info("Starting scraping task")
    start_time = time.time()
    date = timezone.now().date()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    headers_file_path = os.path.join(script_dir, "files/headers.yml")

    with open(headers_file_path) as f_headers:
        browser_headers = yaml.safe_load(f_headers)
    headers = browser_headers["Chrome"]
    i = limit = 1
    while i <= 160:
        url = f"https://www.instant-gaming.com/fr/rechercher/?type%5B0%5D=pc&page={i}"
        print(f"Scraping page {i} : ")
        if limit == i:
        #     good_proxies = get_good_proxies(url)
            print('Using proxies')
        else :
            limit = i
        for browser, headers in browser_headers.items():
            if limit != i:
                break
            print(f"\n\nUsing {browser} headers\n")
            # for proxy_url in good_proxies:   
            #     proxies = {
            #         "http": proxy_url,
            #         "https": proxy_url,
            #     }
            time.sleep(random.uniform(2.5, 10.0))
            print(f"Scraping page {i} : started")
            try:
                # response = requests.get(url, headers=headers, proxies=proxies, timeout=random.uniform(2.5, 10.0))
                response = requests.get(url, headers=headers, timeout=random.uniform(10.0, 25.0))
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    infos = soup.findAll('div', {'class': ["item", "force-badge"]})
                    print(f'{len(infos)} items scraped.')
                    j = 0
                    for info in infos:
                        j += 1
                        name = info.find('div', {'class': 'name'})
                        if (name == None) :
                            name = None
                        else :
                            name = name.text
                            if "DLC" in name:
                                type = "DLC"
                            else :
                                type = "Game"
                            name = name.replace("DLC", "").replace("\n", "")
                        price = info.find('div', {'class': 'price'})
                        if (price == None) :
                            price = '0'
                        else :
                            price = rf"{price.text}"
                            price = re.sub(r"[^\d\.]", "", price)
                        discount = info.find('div', {'class': 'discount'})
                        if (discount == None) :
                            discount = '0'
                        else :
                            discount = discount.text
                            discount = discount.replace("%", "")
                        image = info.find('img', {'class': 'picture'})
                        if (image == None) :
                            image = ''
                        else :
                            image = image['data-src']
                        link = info.find('a', {'class': ['cover', 'video']})
                        if (link == None) :
                            link = info.find('a', {'class': ['cover']})
                        elif (link == None) :
                            link = '#'
                        else :
                            link = link['href']
                        if name:
                            slug = slugify(name)
                            item = {
                                "name": name, 
                                'slug': slug,
                                "type": type,
                                'description': '',
                                'shop': 'Instant Gaming',
                                "link": link,
                                "image": image
                            }
                            print(f'Game slug is {slug}')
                            game = Game.objects.filter(slug=item["slug"]).first()
                            if not game:
                                game = Game.objects.create(**item)
                            game_data_exists = GameData.objects.filter(game=game, date__date=date).exists()
                            if not game_data_exists:
                                data = {
                                    "game": game,
                                    "price": price,
                                    "discount": discount,
                                }
                                GameData.objects.create(**data)
                            else:
                                print(f"Game {game.name} already exists for {date}")
                                pass
                            print(f"{j}/{len(infos)} - {name} scraped.")
                    print(f"Page {i} scraped, files saved.")
                    i += 1
                    url = f"https://www.instant-gaming.com/fr/rechercher/?type%5B0%5D=pc&page={i}"
                    print('\n\n-------------------------\n\n')
                break
            except Exception as e:
                print(f"Erreur : {e}")
                print(f"Scraping page {i} : failed, trying another one.")

    end_time = time.time()
    elapsed_time = end_time - start_time
    formatted_elapsed_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
    print(f"Temps d'exécution : { formatted_elapsed_time }")

    return f"Temps d'exécution : { formatted_elapsed_time }"