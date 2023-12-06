from flask import Flask, render_template, request
from main import get_french_dishes, search_french_dishes

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html')
@app.route('/list', methods=['Post'])
def list_all():
    dishes = get_french_dishes()
    return render_template('list.html', dishes=dishes)


@app.route('/search', methods=['GET'])
def search():
    search_query = request.args.get('search_query', '')
    print(search_query)
    dishes = search_french_dishes(search_query)
    return render_template('results.html', dishes=dishes)


if __name__ == '__main__':
    app.run()
