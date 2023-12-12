from flask import Flask, render_template, request
from main import *

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/list', methods=['Post'])
def list_all():
    dishes = get_list_french_dishes()
    return render_template('list.html', dishes=dishes)


@app.route('/search', methods=['GET'])
def search():
    search_query = request.args.get('search_query', '')
    print(search_query)
    dishes = search_french_dishes(search_query)
    return render_template('results.html', dishes=dishes)


@app.route('/random', methods=['POST'])
def random():
    dish = get_random_french_dish()
    return render_template('random.html', dish=dish)


@app.route('/region', methods=['GET'])
def region():
    region_name = request.args.get('regionName', '')
    print(region_name)
    region = get_french_dishes_by_region(region_name)
    print(region)
    return render_template('region.html', region=region)


if __name__ == '__main__':
    app.run()
