from flask import Flask, render_template
import random
import os
import urllib.request
from bs4 import BeautifulSoup
import locale

app = Flask(__name__)

locale.setlocale(locale.LC_ALL, 'en_US')


states = {
    "New Hampshire" : 'https://www.nytimes.com/interactive/2020/02/11/us/elections/results-new-hampshire-primary-election.html'
}

avatars = {
    "Bernie Sanders" : "static/res/bernie.png", 
    "Pete Buttigieg" : "static/res/pete.jpg",
    "Amy Klobuchar" : "static/res/amy.jpg", 
    "Elizabeth Warren": "static/res/warren.jpg", 
    "Joseph R. Biden Jr.": "static/res/joe.jpg"
}

NUM_CANDIDATES = 5





templates = [x for x in os.listdir("templates") if '.html' in x]



def process_candidate_list(candidate_list):
    total_votes = sum([x['votes'] for x in candidate_list])

    candidate_list = candidate_list[:NUM_CANDIDATES]

    for x in candidate_list:
        x['percentage'] = str("{:.1f}".format(100 * x['votes'] / total_votes, 2)) + "%"
        x['votes'] = locale.format("%d", x['votes'], grouping=True)

    return candidate_list



@app.route('/')
def hello_world():
    page = random.choice(templates)    

    info_dict, candidate_list = retrieve_table("New Hampshire")

    candidate_list = process_candidate_list(candidate_list)

    

    return render_template('intro.html', candidates=candidate_list, info=info_dict)


@app.route('/retrieve_next')
def help():
    info_dict, candidate_list = retrieve_table("New Hampshire")
    candidate_list = process_candidate_list(candidate_list)
    return {"info" : info_dict, "candidates": candidate_list}


def retrieve_table(state):
    with urllib.request.urlopen(states[state]) as response:

        info_dict = {}
        info_dict['state'] = state
        
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')

        table = soup.find('table', class_='e-table e-results-table')

        info_dict['total_votes'] = soup.find('span', class_='e-total-votes').contents[0][:-2]
        info_dict['precincts_reporting'] = soup.find('span', class_='e-precinct-count').contents[0]
        info_dict['percentage_reporting'] = soup.find('span', class_='e-pct-reporting').contents[0]

        print(info_dict)


        candidate_list = []

        for row in table.find_all('tr'):
            if 'e-show-all' not in row['class']:
                candidate_list.append(extract_row(row))
        
        return info_dict, candidate_list


def extract_row(row):
    res = {} 
    res['winner'] = 'e-winner' in row['class']
    res['votes'] = int(row.find('span', class_='e-votes-display').contents[0].replace(',', ''))
    res['name'] = row.find('span', class_='e-name-display').contents[0].strip()

    res['delegates'] = int(row.find('span', class_='e-del-display').contents[0].replace(',', ''))
    res['avatar'] = avatars[res['name']] if res['name'] in avatars else ""


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



