import random
import urllib.request
from bs4 import BeautifulSoup
import locale

locale.setlocale(locale.LC_ALL, 'en_US.utf8')


states = {
    "New Hampshire" : 'https://www.nytimes.com/interactive/2020/02/11/us/elections/results-new-hampshire-primary-election.html', 
    "South Carolina": 'https://www.nytimes.com/interactive/2020/02/29/us/elections/results-south-carolina-primary-election.html'
}



avatars = {
    "Bernie Sanders" : "/static/res/bernie.png", 
    "Pete Buttigieg" : "/static/res/pete.jpg",
    "Amy Klobuchar" : "/static/res/amy.jpg", 
    "Elizabeth Warren": "/static/res/warren.jpg", 
    "Joseph R. Biden Jr.": "/static/res/joe.jpg", 
    "Tom Steyer" : "/static/res/steyer.jpg", 
    "Michael Bloomberg" : "/static/res/mike.jpg"
}

NUM_CANDIDATES = 5





def process_candidate_list(candidate_list):
    total_votes = sum([x['votes'] for x in candidate_list])


    candidate_list = candidate_list[:NUM_CANDIDATES]
    
    for x in candidate_list:
        if total_votes == 0:
            x['percentage'] = str("{:.1f}".format(0, 2)) + "%"
        else:
            x['percentage'] = str("{:.1f}".format(100 * x['votes'] / total_votes, 2)) + "%"
        x['votes'] = locale.format("%d", x['votes'], grouping=True)

    return candidate_list


def retrieve_table(state):
    if state in states:
        url = states[state]
    else:
        url = states['South Carolina']



    with urllib.request.urlopen(url) as response:
        info_dict = {}
        info_dict['state'] = state
        
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')

        table = soup.find('table', class_='e-table e-results-table')
        
        total_votes_found = soup.find('span', class_='e-total-votes')
        if total_votes_found and total_votes_found.contents:
            total_votes = total_votes_found.contents[0][:-2]
        else:
            total_votes = "No results yet..."

        info_dict['total_votes'] = total_votes

        precinct_count_found = soup.find('span', class_='e-precinct-count')
        if precinct_count_found and precinct_count_found.contents:
            precinct_count = precinct_count_found.contents[0]
        else:
            precinct_count = "No Precincts Reporting"

        info_dict['precincts_reporting'] = precinct_count

        percent_reporting_found = soup.find('span', class_='e-pct-reporting')
        if percent_reporting_found and percent_reporting_found.contents:
            percentage_reporting = percent_reporting_found.contents[0]
        else:
            percentage_reporting = "0% reporting"

        
        info_dict['percentage_reporting'] = percentage_reporting


        candidate_list = []

        info_dict['winner'] = False

        for row in table.find_all('tr'):
            if 'e-show-all' not in row['class']:
                extracted = extract_row(row)
                if extracted['name'] == 'Others':
                    continue
                if extracted['winner']:
                    info_dict['winner'] = True
                
                candidate_list.append(extracted)

        return info_dict, candidate_list


def extract_row(row):
    res = {} 
    res['winner'] = 'e-winner' in row['class']

    found_votes = row.find('span', class_='e-votes-display')
    if found_votes and found_votes.contents:
        votes = int(found_votes.contents[0].replace(',', ''))
    else:
        votes = 0

    res['votes'] = votes
    res['name'] = row.find('span', class_='e-name-display').contents[0].strip()

    found_delegates = row.find('span', class_='e-del-display')

    if found_delegates and found_delegates.contents:
        delegates = int(row.find('span', class_='e-del-display').contents[0].replace(',', ''))
    else:
        delegates = 0

    

    res['delegates'] = delegates

    res['avatar'] = avatars[res['name']] if res['name'] in avatars else ""


    return res
