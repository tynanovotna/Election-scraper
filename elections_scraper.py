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

def download_web_page(url, first_url=False):
    try:
        session = requests.Session()
        retries = Retry(total=200, backoff_factor=2, status_forcelist=[104, 107,  502, 503, 504])
        session.mount("http://", HTTPAdapter(max_retries=retries))
        response = session.get(url)
        if first_url:
            print(f"Downloading data from selected URL: {url}")
        return response
    except requests.exceptions.MissingSchema:
        print(f"Invalid URL {url}.")
        exit()

def get_region_urls(soup):
    elements = soup.find_all(class_="cislo")   
    region_urls = []
    for element in elements:
        element_attrs = element.find("a").attrs
        url = element_attrs["href"].replace("amp;", "")
        region_urls.append(URL_BEGINNIG + url)
    return region_urls

def validate_output_file_name(output_file_name):
    if not output_file_name.endswith(".csv"):
        print("Incorect file suffix(= .csv). ")
        exit()

def process_data(region_urls):
    processed_data = {}
    for region_url in region_urls:
        response = download_web_page(region_url)
        soup = BeautifulSoup(response.content, "lxml")
        town_code = re.search("xobec=(.*?)&x", region_url).group(1)
        if not town_code in processed_data:
            data = soup.find(id="publikace")
            h3 = data.find_all("h3")
            town = h3[2].text.split("Obec: ")[1].strip()
            tables = soup.find_all("table")
            table_data = tables[0].find_all("td")
            registered = table_data[3].text.replace("\xa0", " ")
            envelopes = table_data[4].text.replace("\xa0", " ")
            valid = table_data[7].text.replace("\xa0", " ")        
        
def election_scraper(url, output_file_name):
    validate_output_file_name(output_file_name)
    response = download_web_page(url, True)
    soup = BeautifulSoup(response.content, "lxml")
    region_urls = get_region_urls(soup)
    process_data(region_urls)
    
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
    