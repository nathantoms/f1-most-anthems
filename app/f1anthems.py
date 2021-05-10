import requests
import json

def initialize_country(nationality, country_count, driver_or_constructor):
    if nationality not in country_count:
        country_count[nationality] = {}
    
    if driver_or_constructor not in country_count[nationality]:
        country_count[nationality][driver_or_constructor] = 0

    if "total" not in country_count[nationality]:
        country_count[nationality]["total"] = 0

    if "same_country" not in country_count[nationality]:
        country_count[nationality]["same_country"] = 0

def add_nationality_from_result(grand_prix_result, country_count):
    driver_nationality = grand_prix_result["Results"][0]["Driver"]["nationality"]
    initialize_country(driver_nationality, country_count, "driver")
    country_count[driver_nationality]["driver"] += 1
    country_count[driver_nationality]["total"] += 1

    constructor_nationality = grand_prix_result["Results"][0]["Constructor"]["nationality"]
    initialize_country(constructor_nationality, country_count, "constructor")
    country_count[constructor_nationality]["constructor"] += 1
    
    if driver_nationality == constructor_nationality:
        country_count[constructor_nationality]["same_country"] += 1
    else:
        country_count[constructor_nationality]["total"] += 1

    
def is_exception(grand_prix_result):
    return false

def get_anthem_count():
    number_of_seasons = 1000
    country_count = {}

    seasons_response = requests.get("http://ergast.com/api/f1/seasons.json?limit=" + str(number_of_seasons))
    seasons = json.loads(seasons_response.text.encode(seasons_response.encoding))["MRData"]["SeasonTable"]["Seasons"]

    for season in seasons:
        season_results_response = requests.get("http://ergast.com/api/f1/" + season["season"] + "/results/1.json?limit=1000")
        season_results = json.loads(season_results_response.text.encode(season_results_response.encoding))["MRData"]["RaceTable"]["Races"]
        for grand_prix_result in season_results:
            add_nationality_from_result(grand_prix_result, country_count)
    res = sorted(country_count.items(), key = lambda x: x[1]['total'], reverse = True)
    return res