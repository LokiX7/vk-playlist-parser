import os
import requests
from bs4 import BeautifulSoup


HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
}

def get_url():
    url = input('Playlist url: ')
    url = url.strip()
    return url


def get_page(url, headers):
    response = requests.get(url, headers=headers, params='')
    return response


def get_content(response):
    soup = BeautifulSoup(response.text, 'html.parser')
    playlist = soup.find('div', class_='AudioPlaylistSnippet__title').get_text().strip()
    block = soup.find('div', class_='AudioPlaylistSnippet__body')
    items = block.find_all('div', class_='audio_row')
    soundtracks = []

    for item in items:
        soundtracks.append(
            {
                'actor':item.find('div', class_='audio_row__performers').get_text().strip(),
                'name':item.find('div', class_='audio_row__title _audio_row__title').get_text().strip(),
            }
        )

    return soundtracks, playlist


def save_data(data):
    os.makedirs('playlists', exist_ok=True)
    with open(f'playlists/{data[1]}.txt', 'w') as file:
        for item in data[0]:
            line = f"{item['name']} - {item['actor']}\n"
            file.write(line)
        

def parser():
    url = get_url()
    response = get_page(url, HEADERS)
    if response.status_code == 200:
        data = get_content(response)
        save_data(data)
        print('Done!')
    else:
        print(f'Error. Status code: {response.status_code}')


if __name__ == '__main__':
   parser() 


