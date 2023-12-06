from SPARQLWrapper import SPARQLWrapper, JSON
import re


def get_french_dishes():
    sparql = SPARQLWrapper("https://dbpedia.org/sparql")
    query = """
    PREFIX dbr: <http://dbpedia.org/resource/>
PREFIX dbc: <http://dbpedia.org/resource/Category:>
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX dct: <http://purl.org/dc/terms/>

SELECT ?dish ?description
WHERE {
    ?dish dct:subject dbc:French_cuisine.
    OPTIONAL { ?dish dbo:abstract ?description. FILTER(LANG(?description) = "en") }
}
LIMIT 100

    """
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    dishes = [result["dish"]["value"] for result in results["results"]["bindings"]]
    return dishes


def search_french_dishes(search_term):
    sparql = SPARQLWrapper("https://dbpedia.org/sparql")

    # Sanitize the search term to prevent SPARQL injection
    safe_search_term = re.escape(search_term)

    query = f"""
    PREFIX dbr: <http://dbpedia.org/resource/>
    PREFIX dbc: <http://dbpedia.org/resource/Category:>
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX dct: <http://purl.org/dc/terms/>

    SELECT ?dish ?description
    WHERE {{
        ?dish dct:subject dbc:French_cuisine.
        OPTIONAL {{ ?dish dbo:abstract ?description. FILTER(LANG(?description) = "en") }}
        FILTER regex(str(?dish), "{safe_search_term}", "i")
    }}
    LIMIT 100
    """

    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    dishes = [{'name': result["dish"]["value"],
               'description': result["description"]["value"] if "description" in result else ""} for result in
              results["results"]["bindings"]]
    return dishes

# Example usage
# french_dishes = get_french_dishes()
# print(french_dishes)
