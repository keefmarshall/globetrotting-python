import json
import math

R = 6371

distance_cache = {}
distance_cache_hits = 0

def load_countries():
    with open("countries.json") as json_txt:
        data = json.load(json_txt)

    countries = {}
    for c in filter(lambda x: x["capitalCity"] != "", data[1]):
        countries[c["name"]] = c

    return countries

def calc_distance(country1, country2):
    lat1 = math.radians(float(country1["latitude"]))
    lat2 = math.radians(float(country2["latitude"]))
    long1 = float(country1["longitude"])
    long2 = float(country2["longitude"])
    longDelta = math.radians(long2 - long1)

    return math.acos( (math.sin(lat1) * math.sin(lat2)) + (math.cos(lat1) * math.cos(lat2) * math.cos(longDelta)) ) * R

def cached_distance(country1, country2):
    key = (country1["id"], country2["id"])
    if key in distance_cache:
        global distance_cache_hits
        distance_cache_hits += 1
        return distance_cache[key]
    else:
        d = calc_distance(country1, country2)
        distance_cache[key] = d
        return d

def routed_capitals(country, range, visited, country_subset):
    new_visited = visited + [country["id"]]
    #print("visited: ", visited)
    longest_route = []
    most_caps = 0
    for country2 in filter(lambda c: c["id"] not in new_visited, country_subset):
        #print(country["name"] + " -> " + country2["name"])
        distance = cached_distance(country, country2)
        if distance <= range:
            next_capitals = routed_capitals(country2, range - distance, new_visited, country_subset)
            l = len(next_capitals)
            if (l > most_caps):
                longest_route = next_capitals
                most_caps = l
                #print("current longest_route = ", longest_route)
    
    return [country] + longest_route

def all_countries_within_range(country, range):
    within_range = []
    for country2 in countries.values():
        if country2["id"] != country["id"]:
            distance = cached_distance(country, country2)
            if distance <= range:
                within_range.append(country2)
    return within_range


countries = load_countries()
# print(calc_distance(countries["United Kingdom"], countries["Ireland"]))

#print(routed_capitals(countries["Ireland"], 500, []))

start_country = "United Kingdom"
range = 680
countries_in_range = all_countries_within_range(countries[start_country], range)
print("Countries in range: ", len(countries_in_range))
print([c["capitalCity"] for c in routed_capitals(countries[start_country], range, [], countries_in_range)])

print("Distance cache hits: ", distance_cache_hits)