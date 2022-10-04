"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie

author: Kristýna Novotná
email: tynadanielova@seznam.cz
discord: KristýnaN #4503
"""

import bs4
from bs4 import BeautifulSoup
import html5lib
import lxml
import requests
from requests.adapters import HTTPAdapter, Retry

import re
import sys

URL_BEGINNIG = "https://www.volby.cz/pls/ps2017nss/"

def download_web_page(url):
    try:
        session = requests.Session()
        retries = Retry(total=200, backoff_factor=2, status_forcelist=[104, 107,  502, 503, 504])
        session.mount("http://", HTTPAdapter(max_retries=retries))
        response = session.get(url)
        print(f"Downloading data from selected URL: {url}")
        return response
    except requests.exceptions.MissingSchema:
        print(f"Invalid URL {url}.")
        exit()

def get_urls(soup):
    elements = soup.find_all(class_="cislo")
    urls = []
    for element in elements:
        element_attrs = element.find("a").attrs
        urls.append(URL_BEGINNIG + element_attrs["href"].replace("amp;", ""))
    return urls

def process_areas(urls):   
    for url in urls:
        response = download_web_page(url)
        soup = BeautifulSoup(response.content, "lxml")
        urls = get_urls(soup)

def validate_output_file_name(output_file_name):
    if not output_file_name.endswith(".csv"):
        print("Incorect file suffix(= .csv). ")
        exit()
        
def election_scraper(url, output_file_name):
    validate_output_file_name(output_file_name)
    response = download_web_page(url)
    soup = BeautifulSoup(response.content, "lxml")
    urls = get_urls(soup)
    process_areas(urls)
    
if __name__ == "__main__": 
    if not len(sys.argv) == 3:
        print("Incorect number of parameters.")
        print("There should be exactly 2. First = URL, second = output-file-name.csv")
        exit()
    url = sys.argv[1]
    output_file_name = sys.argv[2]
    if not "https://" in url and "https://" in output_file_name and url.endswith(".csv"):
        print("Incorect order of parameters. First = URl, second = file.csv")
    election_scraper(url, output_file_name)
    