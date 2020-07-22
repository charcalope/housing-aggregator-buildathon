from flask import Flask
from flask import render_template, url_for
from utils.data_utils import load_10, fetch_misc_data
from utils.google_utils import fetch_zillow_link

application=Flask(__name__)

@application.route('/')
def hello_world():
    data = load_10()
    for dp in data:
        building_id = dp['buildingid']
        response = fetch_misc_data(building_id)
        if response:
            dp['neighborhood'] = response[0]
            dp['building_name'] = response[1]
            dp['link'] = fetch_zillow_link(response[1])
        else:
            dp['neighborhood'] = 'Seattle'
            dp['building_name'] = 'Apartment Building'
            dp['link'] = 'https://www.zillow.com'
    return render_template('home.html', data=data)

@application.route('/metrics.html')
def metrics_page():
    return render_template('metrics.html')

@application.route('/info.html')
def info_page():
    return render_template('info.html')

@application.route('/aboutme.html')
def about_page():
    return render_template('aboutme.html')

if __name__ == '__main__':
    application.run()
