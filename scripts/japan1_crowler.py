import requests
from bs4 import BeautifulSoup
import re
import time
from numpy.random import normal
from numpy import abs
from pathlib import Path

cur_dir = Path(__file__).resolve().parent
jap_dir = Path(f"{cur_dir}/japan_texts")
if jap_dir.exists() is False:
    jap_dir = Path.mkdir(jap_dir, parents=True)
# чтобы не было проблем с местоположением файлов


def get_chronicle_sheet(url: str) -> list:
    page = requests.get(url)
    beau = BeautifulSoup(page.text, "html")
    p = str(beau.p).replace('<br/>', '\n').replace('<p>', '').replace('</p>', '')
    head = beau.find_all("h1")[1].text
    name, place, _, dat, year, _ = re.findall("(.+?) \((.+?)\) (.{4}-.+?), (.+?), (\d+), (.+)", head)[0]
    if '[volume]' in name:
        name = name.replace('[volume]', '')
        name = name.replace('  ', ' ')
    filename = f"{year}_{dat}_{name}_{place}"
    with open(f"{jap_dir}/{filename}.txt", "wb") as out_file:
        out_file.write(url.encode())
        out_file.write("\n".encode())
        out_file.write(head.encode())
        out_file.write("\n\n".encode())
        out_file.write(p.encode())
        

def get_chronicle_page(first_year: int, last_year: int, req_str: str, page_no: int) -> list:
    url = f"""https://chroniclingamerica.loc.gov/search/pages/results/?date1={first_year}\
&rows=20&searchType=basic&state=&date2={last_year}&proxtext={req_str}&y=19&x=18&\
dateFilterType=yearRange&page={page_no}&sort=relevance"""
    page = requests.get(url)
    beau = BeautifulSoup(page.text, "html")
    urls = list(set([div.find_all("a")[0]["href"] for div in beau.find_all("div", attrs={"class": "highlite"})]))
    urls = [f"https://chroniclingamerica.loc.gov{url.split('#')[0]}ocr/" for url in urls]
    count = len(urls)
    for quo, url in enumerate(urls):
        print(f"{page_no}, {quo} out of {count} {url}", end="\r")
        get_chronicle_sheet(url)
    time.sleep(2 + abs(normal(2, 1)))

# 1047 pages 
for i in range(1, 1048):
    get_chronicle_page(1852, 1855, "Japan", i)
