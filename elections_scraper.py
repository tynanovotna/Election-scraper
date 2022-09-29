"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie

author: Kristýna Novotná
email: tynadanielova@seznam.cz
discord: KristýnaN #4503
"""

import bs4
import html5lib
import lxml
import requests

import sys

def download_web_page(url):
    try:
        print(repr(url))
        raw_web_page = requests.get(url)
        print(f"Downloading data from selected URL: {url}")
        return raw_web_page
    except requests.exceptions.MissingSchema:
        print(f"Invalid URL {url}.")
        exit()
        
def validate_output_file_name(output_file_name):
    if not output_file_name.endswith(".csv"):
        print("Incorect file suffix(= .csv). ")
        exit()
        
def election_scraper(url, output_file_name):
    validate_output_file_name(output_file_name)
    raw_web_page = download_web_page(url)
    print(raw_web_page)

if __name__ == "__main__": 
    print(sys.argv)
    if not len(sys.argv) == 3:
        print("Incorect number of parameters.")
        print("There should be exactly 2. First = URL, second = output-file-name.csv")
        exit()
    url = sys.argv[1]
    output_file_name = sys.argv[2]
    if not "https://" in url and "https://" in output_file_name and url.endswith(".csv"):
        print("Incorect order of parameters. First = URl, second = file.csv")
    election_scraper(url, output_file_name)
    