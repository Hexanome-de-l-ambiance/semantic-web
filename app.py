from flask import Flask, render_template, request, send_from_directory, jsonify
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
    selected_categories = request.args.getlist('categories')
    all_dishes = search_french_dishes(search_query, selected_categories)
    portions = split_list_into_portions(all_dishes)
    return render_template('results.html', portion1=portions[0], portion2=portions[1], portion3=portions[2], portion4=portions[3])


@app.route('/searchComplete', methods=['GET'])
def searchComplete():
    search_query = request.args.get('q', '')
    selected_categories = request.args.getlist('categories')
    all_dishes = complete_search_french_dishes(
        search_query, selected_categories)
    return jsonify(all_dishes)


@app.route('/random', methods=['GET'])
def random():
    dish = get_random_french_dish()
    return render_template('about_cuisine.html', dish=dish)


@app.route('/about_cuisine', methods=['GET'])
def about_cuisine():
    dish_name = request.args.get('dish_link', '')
    dish = get_dish_by_link(dish_name)
    reco = get_recommendation_by_link(dish_name)
    portions = split_reco_into_2_portions_of_length_3(reco)
    return render_template('about_cuisine.html', dish=dish, reco1=portions[0], reco2=portions[1])


@app.route('/about_ingredient', methods=['GET'])
def about_ingredient():
    ingredient_name = request.args.get('ingredient_link', '')
    ingredient = get_ingredient_by_link(ingredient_name)
    return render_template('about_ingredient.html', ingredient=ingredient)


@app.route('/about_chef', methods=['GET'])
def about_chef():
    chef_name = request.args.get('chef_link', '')
    chef_id = request.args.get('chef_id', '')
    chef = get_chef_by_link(chef_name)
    if chef is None:
        chef = get_chef_by_id(chef_id)
    return render_template('about_chef.html', chef=chef)


@app.route('/about_restaurant', methods=['GET'])
def about_restaurant():
    restaurant_name = request.args.get('restaurant_link', '')
    restaurant_id = request.args.get('restaurant_id', '')
    restaurant = get_restaurant_by_link(restaurant_name)
    if restaurant is None:
        restaurant = get_restaurant_by_id(restaurant_id)
    return render_template('about_restaurant.html', restaurant=restaurant)


@app.route('/region', methods=['GET'])
def region():
    region_name = request.args.get('regionName', '')

    regional_dishes = get_french_dishes_by_region(region_name)

    # if no dishes found, display a message below the map without reloading the page
    if len(regional_dishes) == 0:
        return render_template('region.html', no_dishes=True)

    portions = split_list_into_portions(regional_dishes)

    return render_template('region.html', portion1=portions[0], portion2=portions[1], portion3=portions[2], portion4=portions[3])


@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)


@app.route('/fetch-wikipedia-image')
def fetch_wikipedia_image():
    full_keyword = request.args.get('keyword')
    keyword_parts = full_keyword.split()
    # Rejoin all parts except the last one
    keyword = ' '.join(keyword_parts[:-1])
    image_url = get_wikipedia_image(keyword)
    if image_url:
        return jsonify({'imageUrl': image_url})
    else:
        return jsonify({'imageUrl': 'static/images/placeholder_chef.png'})


if __name__ == '__main__':
    app.run()
