"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie

author: Kristýna Novotná
email: tynadanielova@seznam.cz
discord: KristýnaN #4503
"""

from bs4 import BeautifulSoup
import requests
from requests.adapters import HTTPAdapter, Retry

import re
import sys
import csv

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

def process_region_data(region_url):
    region_data = {}
    response = download_web_page(region_url)
    soup = BeautifulSoup(response.content, "lxml")
    region_data["code"] = re.search("xobec=(.*?)&x", region_url).group(1)
    data = soup.find(id="publikace")
    h3 = data.find_all("h3")
    region_data["location"] = h3[2].text.split("Obec: ")[1].strip()
    tables = soup.find_all("table")
    table_data = tables[0].find_all("td")
    region_data["registered"] = table_data[3].text.replace("\xa0", " ")
    region_data["envelopes"] = table_data[4].text.replace("\xa0", " ")
    region_data["valid"] = table_data[7].text.replace("\xa0", " ")
    
    party_names_with_votes = {}
    for i in range(1, len(tables)):
        table = tables[i]
        party_names = table.find_all(headers=f"t{i}sa1 t{i}sb2")
        valid_votes = table.find_all(headers=f"t{i}sa2 t{i}sb3")
        for j in range(len(party_names)):
            if not party_names[j].text == "-":
                party_names_with_votes[party_names[j].text] = valid_votes[j].text.replace("\xa0", " ")
    region_data["party_names_with_votes"] = party_names_with_votes
    return region_data

def process_data_and_make_file(region_urls, output_file_name):
    party_names = []
    print(f"Writing file {output_file_name}")
    with open(output_file_name, "w") as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        for region_url in region_urls:
            region_data = process_region_data(region_url)
            if not party_names:
                party_names = list(region_data["party_names_with_votes"].keys())
                writer.writerow(["Code", "Location", "Registred", "Envelopes", "Valid"] + party_names)
            party_votes = []
            for party_name in party_names:
                party_votes.append(region_data["party_names_with_votes"][party_name])
            writer.writerow([
                region_data["code"],
                region_data["location"], 
                region_data["registered"],
                region_data["envelopes"], 
                region_data["valid"]
            ] + party_votes)
    print("Exiting Election Scraper")
    
def election_scraper(url, output_file_name):
    validate_output_file_name(output_file_name)
    response = download_web_page(url, True)
    soup = BeautifulSoup(response.content, "lxml")
    region_urls = get_region_urls(soup)
    process_data_and_make_file(region_urls, output_file_name)
    
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
    