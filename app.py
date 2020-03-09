from flask import Flask, render_template, request

from events.onyourleft import retrieve_table, process_candidate_list

app = Flask(__name__)




@app.route('/events/<string:title>')
def hello_world(title):
    page = title + ".html"

    return render_template(page)



@app.route('/retrieve_next')
def retrieve_next_page():
    current_state = request.args['state']
    info_dict, candidate_list = retrieve_table(current_state)
    candidate_list = process_candidate_list(candidate_list)
    return {"info" : info_dict, "candidates": candidate_list}





