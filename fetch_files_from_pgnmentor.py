from bs4 import BeautifulSoup
import urllib.request
import requests
import os
import sys


# Main menu
print('\nSelect download target:')
print('   1) By player (ZIP with PGN file inside)')
print('   2) By opening type (ZIP with PGN file inside)')
print('   3) By event (PGN)')
choice = input(' > ')

if (choice == '1'): DOWNLOAD_TARGET = 'players'
elif (choice == '2'): DOWNLOAD_TARGET = 'openings'
elif (choice == '3'): DOWNLOAD_TARGET = 'events'
else: exit('Wrong choice')

print('')


# Fetch urls
headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36'}
page = requests.get('https://www.pgnmentor.com/files.html', headers = headers)
soup = BeautifulSoup(page.content, 'html.parser')
links = soup.findAll('a', href=True)


# Clean urls
urls = []
for link in links:
    if (
        link['href'].startswith(DOWNLOAD_TARGET) 
        and (
            # 'players' and 'openings' files are in zip format
            link['href'].endswith('zip')
            or 
            # 'events' files are in pgn format
            link['href'].endswith('pgn')
        )
    ):
        url = 'https://www.pgnmentor.com/' + link['href']

        # The same url usually appears twice in the web page
        if url not in urls:
            urls.append(url)


# Download files

if not os.path.exists('pgn'):
    os.makedirs('pgn')

for index, url in enumerate(urls):
    filename = url.split('/')[-1]
    if not os.path.isfile(filename):
        try:
            print(
                'Downloading file {index:d} of {total:d}: {filename}' 
                .format(
                    index = index + 1,
                    total = len(urls),
                    filename = filename
                )
            )
            urllib.request.urlretrieve(url, 'pgn/' + filename)
        except:
            print(
                'Unable to download file {index:d}: {filename}'
                .format(
                    index = index + 1,
                    total = len(urls),
                    filename = filename
                )
            )
