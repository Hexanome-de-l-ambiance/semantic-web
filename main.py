from SPARQLWrapper import SPARQLWrapper, JSON
import re
import urllib.parse

from unidecode import unidecode


all_categories = ["French_cuisine", "French_soups", "French_cakes", "French_breads", "French_meat_dishes", "French_pastries", "French_snacks_foods", "French_sandwiches", "French_desserts", "French_sausages", "French_stews", "French_cheeses", "French_fusion_cuisine", "Chefs_of_French_cuisine", "French_restaurants"]


def get_list_french_dishes():
    sparql = SPARQLWrapper("https://dbpedia.org/sparql")
    query = """
    PREFIX dbr: <http://dbpedia.org/resource/>
    PREFIX dbc: <http://dbpedia.org/resource/Category:>
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX dct: <http://purl.org/dc/terms/>

    SELECT ?dish ?id ?name ?image (GROUP_CONCAT(CONCAT(?ingredientName, " - ", ?ingredient); SEPARATOR=", ") AS ?ingredients) ?mainIngredient
    WHERE {
        ?dish dct:subject dbc:French_cuisine.
        ?dish rdfs:label ?name.
        ?dish a dbo:Food.
        ?dish dbo:thumbnail ?image;
        dbo:wikiPageID ?id.
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
            'id': result["id"]["value"],
            'image': result["image"]["value"] if "image" in result else "",
            # List to store ingredients
            'ingredients': result["ingredients"]["value"].split(", "),
            'mainIngredient': result["mainIngredient"]["value"] if "mainIngredient" in result else ""
        }

        dishes.append(dish_info)
    print(dishes)
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
            # List to store ingredients
            'ingredients': result["ingredients"]["value"].split(", "),
            'mainIngredient': result["mainIngredient"]["value"] if "mainIngredient" in result else ""
        }

        dishes.append(dish_info)
    return dishes[0]


def search_about_french_cuisine(search_term: str, criteria: str = "all"):
    sparql = SPARQLWrapper("https://dbpedia.org/sparql")

    # Sanitize the search term to prevent SPARQL injection
    safe_search_term = re.escape(search_term)

    query = f"""
    """


def search_french_dishes(search_term, categories):
    sparql = SPARQLWrapper("https://dbpedia.org/sparql")

    # Sanitize the search term to prevent SPARQL injection
    safe_search_term = re.escape(search_term)
    if not categories:
        categories = all_categories
    print(categories)
    # Join the categories to create a UNION of patterns for the SPARQL query
    union_patterns = "\nUNION\n".join([
        f"""
        {{
            ?dish dct:subject dbc:{category};
            rdfs:label ?name;
            dbo:thumbnail ?image;
            dbo:wikiPageID ?id.

            FILTER(LANG(?name) = "en")
            OPTIONAL {{ ?dish dbo:abstract ?description. FILTER(LANG(?description) = "en") }}
            BIND(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(str(?dish),
            "à", "a"),
            "À", "A"),
            "â", "a"),
            "Â", "A"),
            "è", "e"),
            "È", "E"),
            "ù", "u"),
            "Ù", "U"),
            "é", "e"),
            "É", "E"),
            "ç", "c"),
            "Ç", "C"),
            "ê", "e"),
            "Ê", "E"),
            "î", "i"),
            "Î", "I") AS ?modifiedDish)
    
            FILTER regex(REPLACE(str(?modifiedDish), "[^a-zA-Z0-9]", "", "i"), "{re.escape(safe_search_term)}", "i")

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
        """ for category in categories
    ])

    query = f"""
    PREFIX dbr: <http://dbpedia.org/resource/>
    PREFIX dbc: <http://dbpedia.org/resource/Category:>
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX dct: <http://purl.org/dc/terms/>

    SELECT ?dish ?id ?name ?description ?image (GROUP_CONCAT(CONCAT(?ingredientName, " - ", ?ingredient); SEPARATOR=", ") AS ?ingredients) ?mainIngredient
    WHERE {{
        {union_patterns}
    }}
    LIMIT 100
    """

    print(query)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    sparql.method = 'POST'  # Set the HTTP method to POST

    results = sparql.query().convert()

    dishes = []
    for result in results["results"]["bindings"]:
        dish_info = {
            'name': result["name"]["value"],
            'link': result["dish"]["value"],
            'image': result["image"]["value"] if "image" in result else "",
            'description': result["description"]["value"] if "description" in result else '',
            # List to store ingredients
            'ingredients': result["ingredients"]["value"].split(", "),
            'mainIngredient': result["mainIngredient"]["value"] if "mainIngredient" in result else ""
        }

        dishes.append(dish_info)
    return dishes


def get_dish_by_id(dish_id):
    sparql = SPARQLWrapper("https://dbpedia.org/sparql")
    print(dish_id)
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
        dbo:thumbnail ?image;
        dbo:wikiPageID ?id.

        FILTER(LANG(?name) = "en")
        OPTIONAL {{ ?dish dbo:abstract ?description. FILTER(LANG(?description) = "en") }}
        FILTER (?id = {dish_id})

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
            # List to store ingredients
            'ingredients': result["ingredients"]["value"].split(", "),
            'mainIngredient': result["mainIngredient"]["value"] if "mainIngredient" in result else ""
        }

        dishes.append(dish_info)
    return dishes[0]


def get_ingredient_by_link(ingredient_url):
    # Extract the resource identifier from the DBpedia URL
    resource_identifier = ingredient_url.rsplit('/', 1)[-1]

    # SPARQL query to retrieve information about the dish
    query = f"""
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX dct: <http://purl.org/dc/terms/>

    SELECT ?name ?description ?image
    WHERE {{
        <http://dbpedia.org/resource/{resource_identifier}> rdfs:label ?name.
        
        OPTIONAL {{ <http://dbpedia.org/resource/{resource_identifier}> dbo:abstract ?description; dbo:thumbnail ?image . FILTER(LANG(?description) = "en"). FILTER(LANG(?name) = "en")}}
    }}
    LIMIT 1
    """

    sparql = SPARQLWrapper("https://dbpedia.org/sparql")
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    if "results" in results and "bindings" in results["results"] and results["results"]["bindings"]:
        result = results["results"]["bindings"][0]

        chef_info = {
            'name': result["name"]["value"],
            'link': ingredient_url,
            'image': result["image"]["value"] if "image" in result else "",
            'description': result["description"]["value"] if "description" in result else '',
        }

        return chef_info
    else:
        return None


def get_chef_by_link(chef_url):
    # Extract the resource identifier from the DBpedia URL
    resource_identifier = chef_url.rsplit('/', 1)[-1]

    # SPARQL query to retrieve information about the dish
    query = f"""
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX dct: <http://purl.org/dc/terms/>

    SELECT ?name ?description ?image
    WHERE {{
        <http://dbpedia.org/resource/{resource_identifier}> dbp:name ?name.

        OPTIONAL {{ <http://dbpedia.org/resource/{resource_identifier}> dbo:abstract ?description; dbo:thumbnail ?image. FILTER(LANG(?description) = "en")}}
    }}
    LIMIT 1
    """

    sparql = SPARQLWrapper("https://dbpedia.org/sparql")
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    if "results" in results and "bindings" in results["results"] and results["results"]["bindings"]:
        result = results["results"]["bindings"][0]

        chef_info = {
            'name': result["name"]["value"],
            'link': chef_url,
            'image': result["image"]["value"] if "image" in result else "",
            'description': result["description"]["value"] if "description" in result else '',
        }

        return chef_info
    else:
        return None


def get_restaurant_by_link(restaurant_url):
    # Extract the resource identifier from the DBpedia URL
    resource_identifier = restaurant_url.rsplit('/', 1)[-1]

    # SPARQL query to retrieve information about the dish
    query = f"""
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX dct: <http://purl.org/dc/terms/>

    SELECT ?name ?description ?image
    WHERE {{
        <http://dbpedia.org/resource/{resource_identifier}> dbp:name ?name.

        OPTIONAL {{ <http://dbpedia.org/resource/{resource_identifier}> dbo:abstract ?description; dbo:thumbnail ?image. FILTER(LANG(?description) = "en").}}
    }}
    LIMIT 1
    """

    sparql = SPARQLWrapper("https://dbpedia.org/sparql")
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    if "results" in results and "bindings" in results["results"] and results["results"]["bindings"]:
        result = results["results"]["bindings"][0]

        chef_info = {
            'name': result["name"]["value"],
            'link': restaurant_url,
            'image': result["image"]["value"] if "image" in result else "",
            'description': result["description"]["value"] if "description" in result else '',
        }

        return chef_info
    else:
        return None


region_to_cuisine = {
    "occitanie": "Occitan_cuisine",
    "normandie": "Norman_cuisine",
    "provence-alpes-cote d'azur": "Cuisine_of_Provence",
    "hauts-de-france": "Picardy_cuisine",
    "grand_est": "Alsatian_cuisine",
    "auvergne-rhone-alpes": "Cuisine_of_Auvergne-Rhône-Alpes",
    "corse": "Corsican_cuisine",
    "nouvelle-aquitaine": "Basque_cuisine",
    "bretagne": "Breton_cuisine",
    "bourgogne-franche-comté": "Cuisine_of_Haute-Saône"
}

def get_french_dishes_by_region(region):
    sparql = SPARQLWrapper("https://dbpedia.org/sparql")

    cuisine_by_region = region_to_cuisine.get(region.lower())
    cuisine_by_region_space = cuisine_by_region.replace("_", " ")
    print(cuisine_by_region)

    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    query = f"""
        PREFIX dbr: <http://dbpedia.org/resource/>
        PREFIX dbc: <http://dbpedia.org/resource/Category:>
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX dct: <http://purl.org/dc/terms/>
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

        SELECT ?dish ?name ?image (GROUP_CONCAT(CONCAT(?ingredientName, " - ", ?ingredient); SEPARATOR=", ") AS ?ingredients) ?mainIngredient
        WHERE {{
            ?regionalCuisine skos:prefLabel "{cuisine_by_region_space}"@en.
            ?dish dct:subject ?regionalCuisine.
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
            # List to store ingredients
            'ingredients': result["ingredients"]["value"].split(", "),
            'mainIngredient': result["mainIngredient"]["value"] if "mainIngredient" in result else ""
        }

        dishes.append(dish_info)
    return dishes

def get_region_info_link(region):
    sparql = SPARQLWrapper("https://dbpedia.org/sparql")
    region_formatted = region.replace(" ", "_")  # Replace spaces with underscores for DBpedia resource format

    query = f"""
    PREFIX dbr: <http://dbpedia.org/resource/>
    PREFIX dbc: <http://dbpedia.org/resource/Category:>
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX dct: <http://purl.org/dc/terms/>  # Define the dct prefix

    SELECT ?region
    WHERE {{
        {{
            ?region dct:subject dbc:Regions_of_France.
        }} UNION {{
            ?region dbo:type dbr:Regions_of_France.
        }}
        ?region rdfs:label ?name.
        FILTER(LANG(?name) = "fr")
        FILTER regex(?name, "{region}", "i")  # Case-insensitive match for the region name
    }}
    LIMIT 1
    """

    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    # Return the link to the region's DBpedia resource
    if results["results"]["bindings"]:
        return results["results"]["bindings"][0]["region"]["value"]

    else:
        return "No information found for the specified region."

# Example usage:



# Example usage
# french_dishes = get_french_dishes()
# print(french_dishes)


def split_list_into_portions(dishes):
    # Assuming 'dishes' is the list of retrieved dishes
    total_dishes = len(dishes)
    portion_size = total_dishes // 4  # Divide the list into 4 portions

    portions = [
        dishes[i * portion_size: (i + 1) * portion_size] for i in range(4)]

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

        suggestions = [result["name"]["value"]
                       for result in results["results"]["bindings"]]
        return suggestions


def get_dish_by_url(dbpedia_url):
    # Extract the resource identifier from the DBpedia URL
    resource_identifier = dbpedia_url.rsplit('/', 1)[-1]

    # SPARQL query to retrieve information about the dish
    query = f"""
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX dct: <http://purl.org/dc/terms/>

    SELECT ?name ?description ?image (GROUP_CONCAT(CONCAT(?ingredientName, " - ", ?ingredient); SEPARATOR=", ") AS ?ingredients) ?mainIngredient
    WHERE {{
        <http://dbpedia.org/resource/{resource_identifier}> rdfs:label ?name;
        a dbo:Food;
        dbo:thumbnail ?image.

        OPTIONAL {{ <http://dbpedia.org/resource/{resource_identifier}> dbo:abstract ?description. FILTER(LANG(?description) = "en") }}

        OPTIONAL {{ 
            <http://dbpedia.org/resource/{resource_identifier}> dbo:ingredient ?ingredient.
            ?ingredient rdfs:label ?ingredientName.
            FILTER(LANG(?ingredientName) = "en")
        }}

        OPTIONAL {{
            <http://dbpedia.org/resource/{resource_identifier}> dbp:mainIngredient ?mainIngredient.
            FILTER NOT EXISTS {{ <http://dbpedia.org/resource/{resource_identifier}> dbo:ingredient ?ingredient }}
        }}
    }}
    LIMIT 1
    """

    sparql = SPARQLWrapper("https://dbpedia.org/sparql")
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    if "results" in results and "bindings" in results["results"] and results["results"]["bindings"]:
        result = results["results"]["bindings"][0]

        dish_info = {
            'name': result["name"]["value"],
            'link': dbpedia_url,
            'image': result["image"]["value"] if "image" in result else "",
            'description': result["description"]["value"] if "description" in result else '',
            'ingredients': result["ingredients"]["value"].split(", ") if "ingredients" in result else [],
            'mainIngredient': result["mainIngredient"]["value"] if "mainIngredient" in result else ""
        }

        return dish_info
    else:
        return None
