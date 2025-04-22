import json
import requests
from geopy import distance
import folium
import os
from dotenv import load_dotenv


def fetch_coordinates(apikey, address):
    base_url = 'https://geocode-maps.yandex.ru/1.x'
    response = requests.get(base_url, params={
        'geocode': address,
        'apikey': apikey,
        'format': 'json',
    })
    response.raise_for_status()
    found_places = response.json(
    )['response']['GeoObjectCollection']['featureMember']

    if not found_places:
        return None

    most_relevant = found_places[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(' ')
    return lon, lat


def find_distance(latitude, longitude, cafe_coords):
    length = distance.distance((latitude, longitude), cafe_coords).km
    return length


def get_distance(cafe):
    return cafe['distance']


def fetch_nearest_cafe(new_list_сoffeeshops):
    return min(new_list_сoffeeshops, key=get_distance)


def load_coffee_shops(filepath):
    with open(filepath, 'r', encoding='CP1251') as file:
        return json.load(file)


def change_coords(coords_user_point):
    longitude, latitude = coords_user_point
    return latitude, longitude


def read_file():
    with open('index.html') as file:
        return file.read()


def main():
    load_dotenv('apikey.env')
    apikey = os.getenv('apikey')
    сoffeeshops = load_coffee_shops('coffee.json')
    location = input('Где вы находитесь? ')
    coords_point = fetch_coordinates(apikey, location)
    latitude, longitude = change_coords(coords_point)
    new_list_сoffeeshops = []
    for cafe in сoffeeshops:
        cafe_coords = (
            cafe['geoData']['coordinates'][1],
            cafe['geoData']['coordinates'][0],
        )
        distance = find_distance(latitude, longitude, cafe_coords)
        new_list_сoffeeshops.append({
            'title': cafe['Name'],
            'distance': distance,
            'latitude': cafe_coords[0],
            'longitude': cafe_coords[1],
        })
    closest_coffee_shops = sorted(new_list_сoffeeshops, key=get_distance)
    m = folium.Map(['55.755864', '37.617698'], zoom_start=12)
    for cafe in closest_coffee_shops[:5]:
        folium.Marker([cafe['latitude'], cafe['longitude']],
                      popup=cafe['title'],
                      icon=folium.Icon(color='red',
                                       icon='info-sign')).add_to(m)
    m.save('map.html')


if __name__ == '__main__':
    main()
