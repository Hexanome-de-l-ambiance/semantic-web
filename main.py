from SPARQLWrapper import SPARQLWrapper, JSON
import re
import urllib.parse

categories = ["French_cuisine", "French_soups", "French_cakes", "French_breads", "French_meat_dishes", "French_pastries",
              "French_snacks_foods", "French_sandwiches", "French_desserts", "French_sausages", "French_stews"]    


def get_list_french_dishes():
    sparql = SPARQLWrapper("https://dbpedia.org/sparql")
    query = """
    PREFIX dbr: <http://dbpedia.org/resource/>
    PREFIX dbc: <http://dbpedia.org/resource/Category:>
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX dct: <http://purl.org/dc/terms/>

    SELECT ?dish ?name ?image (GROUP_CONCAT(CONCAT(?ingredientName, " - ", ?ingredient); SEPARATOR=", ") AS ?ingredients) ?mainIngredient
    WHERE {
        ?dish dct:subject dbc:French_cuisine.
        ?dish rdfs:label ?name.
        ?dish a dbo:Food.
        ?dish dbo:thumbnail ?image.
        FILTER(LANG(?name) = "en")

        # Retrieve ingredients and their links
        OPTIONAL {{ 
            ?dish dbo:ingredient ?ingredient.
            ?ingredient rdfs:label ?ingredientName.
            FILTER(LANG(?ingredientName) = "en")
        }}

        OPTIONAL {{
            ?dish dbp:mainIngredient ?mainIngredient.
            FILTER NOT EXISTS {{ ?dish dbo:ingredient ?ingredient }}
        }}
    }
    LIMIT 100


    """
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    dishes = []
    for result in results["results"]["bindings"]:
        dish_info = {
            'name': result["name"]["value"],
            'link': result["dish"]["value"],
            'image': result["image"]["value"] if "image" in result else "",
            'ingredients': result["ingredients"]["value"].split(", "),  # List to store ingredients
            'mainIngredient': result["mainIngredient"]["value"] if "mainIngredient" in result else ""
        }

        dishes.append(dish_info)
    return dishes


def get_random_french_dish():
    sparql = SPARQLWrapper("https://dbpedia.org/sparql")
    query = """
    PREFIX dbr: <http://dbpedia.org/resource/>
    PREFIX dbc: <http://dbpedia.org/resource/Category:>
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX dct: <http://purl.org/dc/terms/>

    SELECT ?dish ?name ?image ?description (GROUP_CONCAT(CONCAT(?ingredientName, " - ", ?ingredient); SEPARATOR=", ") AS ?ingredients) ?mainIngredient
    WHERE {
        ?dish dct:subject dbc:French_cuisine.
        ?dish rdfs:label ?name.
        ?dish a dbo:Food.
        ?dish dbo:thumbnail ?image.
        FILTER(LANG(?name) = "en")

        OPTIONAL {{ ?dish dbo:abstract ?description. FILTER(LANG(?description) = "en") }}

        # Retrieve ingredients and their links
        OPTIONAL {{ 
            ?dish dbo:ingredient ?ingredient.
            ?ingredient rdfs:label ?ingredientName.
            FILTER(LANG(?ingredientName) = "en")
        }}

        OPTIONAL {{
            ?dish dbp:mainIngredient ?mainIngredient.
            FILTER NOT EXISTS {{ ?dish dbo:ingredient ?ingredient }}
        }}
    }
    ORDER BY RAND()
    LIMIT 1

    """
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    dishes = []
    for result in results["results"]["bindings"]:
        dish_info = {
            'name': result["name"]["value"],
            'link': result["dish"]["value"],
            'image': result["image"]["value"] if "image" in result else "",
            'description': result["description"]["value"] if "description" in result else '',
            'ingredients': result["ingredients"]["value"].split(", "),  # List to store ingredients
            'mainIngredient': result["mainIngredient"]["value"] if "mainIngredient" in result else ""
        }

        dishes.append(dish_info)
    return dishes[0]


def search_about_french_cuisine(search_term : str, criteria : str = "all"):
    sparql = SPARQLWrapper("https://dbpedia.org/sparql")

    # Sanitize the search term to prevent SPARQL injection
    safe_search_term = re.escape(search_term)

    query = f"""
    """
    
    
    

def search_french_dishes(search_term):
    sparql = SPARQLWrapper("https://dbpedia.org/sparql")

    # Sanitize the search term to prevent SPARQL injection
    safe_search_term = re.escape(search_term)

    query = f"""
    PREFIX dbr: <http://dbpedia.org/resource/>
    PREFIX dbc: <http://dbpedia.org/resource/Category:>
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX dct: <http://purl.org/dc/terms/>

    SELECT ?dish ?name ?description ?image (GROUP_CONCAT(CONCAT(?ingredientName, " - ", ?ingredient); SEPARATOR=", ") AS ?ingredients) ?mainIngredient
    WHERE {{
        ?dish dct:subject dbc:French_cuisine;
        rdfs:label ?name;
        a dbo:Food;
        dbo:thumbnail ?image.

        FILTER(LANG(?name) = "en")
        OPTIONAL {{ ?dish dbo:abstract ?description. FILTER(LANG(?description) = "en") }}
        FILTER regex(str(?dish), "{safe_search_term}", "i")

        # Retrieve ingredients and their links
        OPTIONAL {{ 
            ?dish dbo:ingredient ?ingredient.
            ?ingredient rdfs:label ?ingredientName.
            FILTER(LANG(?ingredientName) = "en")
        }}

        OPTIONAL {{
            ?dish dbp:mainIngredient ?mainIngredient.
            FILTER NOT EXISTS {{ ?dish dbo:ingredient ?ingredient }}
        }}


    }}
    LIMIT 100
    """

    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    dishes = []
    for result in results["results"]["bindings"]:
        dish_info = {
            'name': result["name"]["value"],
            'link': result["dish"]["value"],
            'image': result["image"]["value"] if "image" in result else "",
            'description': result["description"]["value"] if "description" in result else '',
            'ingredients': result["ingredients"]["value"].split(", "),  # List to store ingredients
            'mainIngredient': result["mainIngredient"]["value"] if "mainIngredient" in result else ""
        }

        dishes.append(dish_info)
    return dishes

def get_dish_by_name(dish_name):
    sparql = SPARQLWrapper("https://dbpedia.org/sparql")

    # Sanitize the search term to prevent SPARQL injection
    name = dish_name.rsplit('/', 1)[-1]
    if '(' in name:
        name = name.split('(', 1)[0].strip()
    else:
        name = name
    safe_search_term = re.escape(name)
    

    query = f"""
    PREFIX dbr: <http://dbpedia.org/resource/>
    PREFIX dbc: <http://dbpedia.org/resource/Category:>
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX dct: <http://purl.org/dc/terms/>

    SELECT ?dish ?name ?description ?image (GROUP_CONCAT(CONCAT(?ingredientName, " - ", ?ingredient); SEPARATOR=", ") AS ?ingredients) ?mainIngredient
    WHERE {{
        ?dish dct:subject dbc:French_cuisine;
        rdfs:label ?name;
        a dbo:Food;
        dbo:thumbnail ?image.

        FILTER(LANG(?name) = "en")
        OPTIONAL {{ ?dish dbo:abstract ?description. FILTER(LANG(?description) = "en") }}
        FILTER regex(str(?dish), "{safe_search_term}", "i")

        # Retrieve ingredients and their links
        OPTIONAL {{ 
            ?dish dbo:ingredient ?ingredient.
            ?ingredient rdfs:label ?ingredientName.
            FILTER(LANG(?ingredientName) = "en")
        }}

        OPTIONAL {{
            ?dish dbp:mainIngredient ?mainIngredient.
            FILTER NOT EXISTS {{ ?dish dbo:ingredient ?ingredient }}
        }}


    }}
    LIMIT 100
    """

    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    dishes = []
    for result in results["results"]["bindings"]:
        dish_info = {
            'name': result["name"]["value"],
            'link': result["dish"]["value"],
            'image': result["image"]["value"] if "image" in result else "",
            'description': result["description"]["value"] if "description" in result else '',
            'ingredients': result["ingredients"]["value"].split(", "),  # List to store ingredients
            'mainIngredient': result["mainIngredient"]["value"] if "mainIngredient" in result else ""
        }

        dishes.append(dish_info)
    return dishes[0]

# Example usage
# french_dishes = get_french_dishes()
# print(french_dishes)
def split_list_into_portions(dishes):
    # Assuming 'dishes' is the list of retrieved dishes
    total_dishes = len(dishes)
    portion_size = total_dishes // 4  # Divide the list into 4 portions

    portions = [dishes[i * portion_size: (i + 1) * portion_size] for i in range(4)]
    
    # Add any remaining dishes to the last portion
    for i in range(total_dishes % 4):
        portions[i].append(dishes[portion_size * 4 + i])

    return portions



 # partie sur l'autocomplétion
def autocomplete_french_dishes(search_term):
    if len(search_term) < 3:
        # Si la chaîne de recherche a moins de trois caractères, retourner une liste vide
        return []
    else:
        sparql = SPARQLWrapper("https://dbpedia.org/sparql")
        safe_search_term = re.escape(search_term)

        query = f"""
        PREFIX dbr: <http://dbpedia.org/resource/>
        PREFIX dbc: <http://dbpedia.org/resource/Category:>
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX dct: <http://purl.org/dc/terms/>

        SELECT DISTINCT ?name
        WHERE {{
            ?dish dct:subject dbc:French_cuisine;
            rdfs:label ?name;
            a dbo:Food.

            FILTER(LANG(?name) = "en")
            FILTER regex(str(?name), "^{safe_search_term}", "i")
        }}
        LIMIT 10
        """
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        suggestions = [result["name"]["value"] for result in results["results"]["bindings"]]
        return suggestions

