from flask import Flask, render_template, request
from main import *

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/list', methods=['GET'])
def list_all():
    all_dishes = get_list_french_dishes()
    portions = split_list_into_portions(all_dishes)
    return render_template('list.html', portion1=portions[0], portion2=portions[1], portion3=portions[2], portion4=portions[3])


@app.route('/search', methods=['GET'])
def search():
    search_query = request.args.get('search_query', '')
    print(search_query)
    all_dishes = search_french_dishes(search_query)
    portions = split_list_into_portions(all_dishes)
    return render_template('results.html', portion1=portions[0], portion2=portions[1], portion3=portions[2], portion4=portions[3])


@app.route('/random', methods=['GET'])
def random():
    dishes = get_random_french_dish()
    return render_template('random.html', dishes=dishes)


if __name__ == '__main__':
    app.run()
