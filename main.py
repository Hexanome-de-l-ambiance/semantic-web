from SPARQLWrapper import SPARQLWrapper, JSON
import re


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
    PREFIX dct: <http://purl.org/dc/terms/>

    SELECT ?dish ?name ?image
    WHERE {
        ?dish dct:subject dbc:French_cuisine;
        rdfs:label ?name;
        a dbo:Food;
        dbo:thumbnail ?image.

        FILTER(LANG(?name) = "en")
    }
    ORDER BY RAND()
    LIMIT 1
    """

    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    dish = results["results"]["bindings"][0]["dish"]["value"] if results["results"]["bindings"] else None
    return dish


def search_french_dishes(search_term):
    sparql = SPARQLWrapper("https://dbpedia.org/sparql")

    # Sanitize the search term to prevent SPARQL injection
    safe_search_term = re.escape(search_term)

    query = f"""
    PREFIX dbr: <http://dbpedia.org/resource/>
    PREFIX dbc: <http://dbpedia.org/resource/Category:>
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX dct: <http://purl.org/dc/terms/>

    SELECT ?dish ?name ?description ?image ?ingredient
    WHERE {{
        ?dish dct:subject dbc:French_cuisine;
        rdfs:label ?name;
        a dbo:Food;
        dbo:thumbnail ?image.

        FILTER(LANG(?name) = "en")
        OPTIONAL {{ ?dish dbo:abstract ?description. FILTER(LANG(?description) = "en") }}
        FILTER regex(str(?dish), "{safe_search_term}", "i")

        OPTIONAL {{         
            ?dish dbo:ingredient ?ingredientResource.
            ?ingredientResource rdfs:label ?ingredient.
            FILTER (LANG(?ingredient) = 'en')
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
            'description': result["description"]["value"] if "description" in result else "",
            'image': result["image"]["value"] if "image" in result else "",
            'ingredients': []  # List to store ingredients
        }

        # Extract and add ingredients to the dish's ingredients list
        if "ingredient" in result:
            dish_info['ingredients'].append({
                'name': result["ingredient"]["value"],
                'link': result["ingredientResource"]["value"]  # Link to the ingredient
            })

        dishes.append(dish_info)
        
    return dishes


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
    print(cuisine_by_region)

    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    query = """
        PREFIX dbc: <http://dbpedia.org/resource/Category:>
        PREFIX dbr: <http://dbpedia.org/resource/>

        SELECT ?regionalCuisine
        WHERE {{
            ?regionalCuisine skos:prefLabel "{}"@en .
            
        }}
        """.format(cuisine_by_region.replace("_", " "))

    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    regional_cuisine = results["results"]["bindings"][0]["regionalCuisine"]["value"] if results["results"]["bindings"] else None
    return regional_cuisine


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
