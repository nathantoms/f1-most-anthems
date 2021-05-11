import requests
import json

def initialize_country(nationality, country_count):
    country_count[nationality] = {
        "driver": 0,
        "constructor": 0,
        "total": 0,
        "same_country": 0
    }

def add_nationality_from_result(grand_prix_result, country_count):
    driver_nationality = grand_prix_result["Results"][0]["Driver"]["nationality"]
    constructor_nationality = grand_prix_result["Results"][0]["Constructor"]["nationality"]

    if driver_nationality not in country_count: initialize_country(driver_nationality, country_count)
    if constructor_nationality not in country_count: initialize_country(constructor_nationality, country_count)

    country_count[driver_nationality]["driver"] += 1
    country_count[constructor_nationality]["constructor"] += 1
    country_count[driver_nationality]["total"] += 1
    
    if driver_nationality == constructor_nationality:
        country_count[constructor_nationality]["same_country"] += 1
    else:
        country_count[constructor_nationality]["total"] += 1

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

    return sorted(country_count.items(), key = lambda x: x[1]['total'], reverse = True)

def get_race_count():
    number_of_seasons = 1000
    race_count = 0

    seasons_response = requests.get("http://ergast.com/api/f1/seasons.json?limit=" + str(number_of_seasons))
    seasons = json.loads(seasons_response.text.encode(seasons_response.encoding))["MRData"]["SeasonTable"]["Seasons"]

    for season in seasons:
        season_results_response = requests.get("http://ergast.com/api/f1/" + season["season"] + "/results/1.json?limit=1000")
        season_results = json.loads(season_results_response.text.encode(season_results_response.encoding))["MRData"]["RaceTable"]["Races"]
        for races in season_results:
            race_count += 1
            
    return race_count
    