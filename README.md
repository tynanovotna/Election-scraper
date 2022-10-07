# Election-scraper
# Project info:
This project is done for scraping parliamentary election results from the year 2017, their location: https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ.

# How to install libraries:
All requirements for installing libraries are in a file ```requirements.txt```. I also recommend using the pipenv virtual environment, which enables the Pipfile.lock and Pipfile. If you wish to use the pipenv virtual environment and it's not installed yet run the following command: 
    ```
    pip install pipenv
    ```
###### how to install with pipenv:
```pipenv install```
    
###### how to install with pip: 
```pip install -r requirements.txt```

# How to run this project:
### This program needs 3 arguments from the terminal:
```python elections_scraper.py <url_of_district_area> <output_file_name.csv> ```

All data are transformed to file with the suffix ```.csv```

# Example of the running program:
### How to get election results of district e.g., Plzeň-město:
1. argument = ```https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=4&xnumnuts=3203 # url of the selected district area```
2. argument = ```results_Plzen_mesto.csv # output file name```

Those arguments must be strings("" or '').

##### example:
```
python elections_scraper.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=4&xnumnuts=3203" "results_Plzen_mesto.csv"
```

### What to expect from a successful run:
```
Downloading data from the selected URL: https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=4&xnumnuts=3203
Writing file results_Plzen_mesto.csv
Exiting Election Scraper
```

### Partial output:
```
Code;Location;Registred;Envelopes;...
558851;Dýšina;1 349;860;853;114;0;0;48;...
558966;Chrást;1 429;1 002;999;151;1;1;51;...
557846;Chválenice;561;369;369;50;3;0;21;0;...
etc.
```

If you wish to see all the data I would strongly recommend LibreOffice Calc on Ubuntu or any Linux environment.(Separator Option = semicolon).
