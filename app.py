from flask import Flask, render_template
import random
import os
import urllib.request
from bs4 import BeautifulSoup


app = Flask(__name__)

NYT_URL = 'https://www.nytimes.com/interactive/2020/02/22/us/elections/results-nevada-caucus.html'


templates = [x for x in os.listdir("templates") if '.html' in x]


@app.route('/')
def hello_world():
    page = random.choice(templates)    

    candidate_list = retrieve_table()
    
    return render_template('intro.html', candidates = candidate_list)



def retrieve_table():
     with urllib.request.urlopen(NYT_URL) as response:
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')



        table = soup.find('table', class_='e-table e-results-table')

        candidate_list = []

        for row in table.find_all('tr'):
            if 'e-show-all' not in row['class']:
                candidate_list.append(extract_row(row))
        
        return candidate_list


def extract_row(row):
    res = {} 
    res['winner'] = 'e-winner' in row['class']
    res['votes'] = int(row.find('span', class_='e-votes-display').contents[0].replace(',', ''))
    res['name'] = row.find('span', class_='e-name-display').contents[0].strip()

    res['delegates'] = int(row.find('span', class_='e-del-display').contents[0].replace(',', ''))


    return res
    


def retreive_nyt():
    """
    Returns the NYT page with the elections results
    """
    with urllib.request.urlopen(NYT_URL) as response:
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')


        soup.find('div', id='standalone-header').decompose()
        soup.find('nav', class_='e-navigation').decompose()
        soup.find('section', class_='e-column')['style'] = "width: 100%"
        names = soup.find_all('span', class_='e-name-display')

        html_pretty = soup.prettify()

        
        # print(table.prettify())

        return html_pretty



