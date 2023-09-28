import json
import re
import time

import requests
from bs4 import BeautifulSoup


def main():

    html_text = requests.get("https://www.insider.com/spotify-most-monthly-listeners-artists-2023-8").text
    soup = BeautifulSoup(html_text, 'lxml')
    artist_dict = {}
    ranking = 20
    artists = soup.find_all('div', class_ = 'slide keyline')

    for artist in artists:
        artist_info = []

        artist_name = artist.find('h2', class_ = 'slide-title-text').text
        artist_name = re.search(r'\d+\.\s*(.+)', artist_name).group(1)
        artist_info.append(artist_name)

        artist_listeners= artist.find_all('p')[0].text
        artist_listeners = re.search(r'(\d+(?:\.\d+)?)\s*million', artist_listeners).group()
        artist_info.append(artist_listeners)

        most_streamed_song = artist.find_all('p')[1].text
        pattern = r"Most streamed song:\s+(.+)"
        artist_song = re.search(pattern, most_streamed_song).group(1)
        artist_info.append(artist_song)

        artist_image = artist.find('div', class_ = 'lazy-holder').find('noscript').find('img').get('src')
        artist_info.append(artist_image)

        artist_dict[ranking] = artist_info
        ranking -= 1


    artist_dict = dict(sorted(artist_dict.items()))

    with open("sample.json", "w") as outfile:
        json.dump(artist_dict, outfile)

    json_object = json.dumps(artist_dict)
    with open("Top Artists", "w") as outfile:
        outfile.write(json_object)


    for key, value in artist_dict.items():
        print(f"Ranking: {key}\nArtist: {value[0]}\nMonthly listeners: {value[1]}\nMost streamed song: {value[2]}\nLooks: {value[3]}")
        print("")


if __name__ == "__main__":
    while True:
        main()
        time_wait = 10
        print(f'Waiting {time_wait} minutes to be updated ...')
        time.sleep(time_wait * 60)
