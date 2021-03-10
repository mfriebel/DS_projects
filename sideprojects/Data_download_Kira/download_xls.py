"""
Download xls from "https://www.mavir.hu/en/web/riportok/rendelkezesre-allasi-dijak"
"""

import os
from bs4 import BeautifulSoup
import time
import requests
import re
import pandas

URL = "https://www.mavir.hu/en/web/riportok/rendelkezesre-allasi-dijak"
HEADER = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:83.0) Gecko/20100101 Firefox/83.0"}
PATH = "./XLS/"

""" Monthly links
Extract all links in tbody "class" = "table-data" -> "tr class" = ""/"td class" = "table-cell first" -> node for link  
# ; "class" - entry title year """

def get_links_year(path):
    # Get HTML of lyrics page
    http_request = requests.get(url= path, headers=HEADER)

    if http_request.status_code == 404:
        raise Exception('Wrong pattern')
    # find each lyrics URL inside the artist page using RE and save to a list
   # Parse HTML file
    table_soup = BeautifulSoup(http_request.text, 'html.parser')
    # Extract sections with lyrics text
    table_list = table_soup.body.find_all(attrs={'class':'table-cell first'})
    year_list = table_soup.body.find_all(attrs={'class':'entry-title-text'})
    links_dict = {}
    for year in year_list[:-1]:
        link = year.find_parent('a').get('href')
        links_dict[year.text] = link
        #year_list.append(year.text)
    return links_dict

def days(year_dict, month):
    url = year_dict[month]
    path = PATH+ month + '/'
    if not os.path.exists(path):
        os.mkdir(path)
        # Get HTML of lyrics page
        http_request_part1 = requests.get(url= url, headers=HEADER)
        # find each lyrics URL inside the artist page using RE and save to a list
        xls_links_part1 = re.findall(f'<a href="(.+{month}.+-en\.xlsx.+)">', http_request_part1.text)
        second_page_ls = re.findall('<a href="(.+)".+onclick.+>', http_request_part1.text)
        second_page = re.sub('amp;', '' ,second_page_ls[2])
        if second_page != 'javascript:;':
            http_request_part2 = requests.get(url= second_page, headers=HEADER)
            xls_links_part2 = re.findall(f'<a href="(.+{month}.+-en\.xlsx.+)">', http_request_part2.text)
            xls_all = xls_links_part1 + xls_links_part2
        else:
            xls_all = xls_links_part1
        print(f'Downloading xlsx of month: {month}')
        for url in xls_all:
            time.sleep(1)
            day = re.findall(f'https:.+-(\d+)-en\.xlsx.+', url)[0]      # Get song title
            day_html = requests.get(url, headers=HEADER)                         # Get song lyrics html                          
            output = open(path + f'/{day}.xlsx', 'wb')  # Write lyrics page to ".html" file
            output.write(day_html.content)
            output.close()
    else:
        print(f'XLSX for month {month} already exists')
    #print(table_list[:-1][3].text)
    #for element in table_list:
    #    print(element)
        #xls = re.findall(f'<a href="(.+{month}.+xlsx.+)">', element)

""" Dayly links
Extract all links in tbody "class" = "table-data" -> "tr class" = ""/"td class" = "table-cell first" -> node for link  
# ; "class" = "entry title" -> year ; search for ending "en.xlsx" & Extract naming (e.g. 20120102("""

if __name__ == "__main__":
    year = get_links_year(URL)
    for month in year:
        print(month)
        days(year, month)