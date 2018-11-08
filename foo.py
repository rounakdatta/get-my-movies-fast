import requests
from lxml import html
from bs4 import BeautifulSoup
import json
import base64
import urllib.parse

movie_page = requests.get('https://www.hoichoi.tv/categories')
home_page = requests.get('https://www.hoichoi.tv/home')

# get all the links
movie_page_links_dump = html.fromstring(movie_page.content).xpath('//a/@href')
home_page_links_dump = html.fromstring(home_page.content).xpath('//a/@href')

# consolidate all the links and remove duplicates
movie_links = list(set([pl for pl in movie_page_links_dump if pl[:6]=='/films'] + [pl for pl in home_page_links_dump if pl[:6]=='/films']))

print(str(len(movie_links)) + ' movies found!')

parent_url = 'https://www.hoichoi.tv'

for movie in movie_links:
	s = requests.session()
	single_movie_url = parent_url + movie
	single_movie_page = s.get(single_movie_url)

	movie_soup = BeautifulSoup(single_movie_page.content, features='lxml')
	data = movie_soup.find_all("script")[1].string

	data = data[data.find('=') + 2:]
	data = data[data.find("'"):-4]
	bin_data = base64.b64decode(data)
	raw_json = str(urllib.parse.unquote(str(bin_data)))[2:-1]

	myJson = json.loads(raw_json)
	video_metadata = myJson['page']['data']['modules'][0]['contentData'][0]
	
	video_id = video_metadata['gist']['id']
	# get the maximum quality video
	video_url = video_metadata['streamingInfo']['videoAssets']['mpeg'][-1]['url']

	print(movie)
	print(video_url)