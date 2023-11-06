import re
from bs4 import BeautifulSoup
from datetime import timedelta
from urllib.request import urlopen

class scrape_video_data:
    def __init__(self, link) -> None:
        # Define the response structure with data types
        self.RESPONSE = {
            'id': str,
            'title': str,
            'upload_date': str,
            'duration': str,
            'description': str,
            'genre': str,
            'is_paid': bool,
            'is_unlisted': bool,
            'is_family_friendly': bool,
            'uploader': {
                'channel_id': str,
            },
            'statistics': {
                'views': int,
                'likes': int,
                'dislikes': int
            },
        }
        self.link = link

    def is_true(self, string):
        # Helper function to check if a string represents a boolean "true"
        return string.lower() not in ['false', '0']

    def remove_comma(self, string):
        # Helper function to remove commas from a string
        return ''.join(string.split(','))

    def make_soup(self, url):
        # Create a BeautifulSoup object from the URL's HTML content
        html = urlopen(url).read()
        return BeautifulSoup(html, 'lxml')

    def make_duration(self, duration_str):
        # Convert duration string (e.g., "PT3M59S") to a timedelta object
        match = re.search(r'PT(\d+)M(\d+)S', duration_str)

        if match:
            minutes = int(match.group(1))
            seconds = int(match.group(2))
            duration = timedelta(minutes=minutes, seconds=seconds)
            return duration
        else:
            return duration

    def scrape_video_data(self):
        '''
        Scrapes data from the YouTube video's page whose ID is passed in the URL,
        and returns a JSON object as a response.
        '''

        youtube_video_url = self.link
        soup = self.make_soup(youtube_video_url)
        soup_itemprop = soup.find(id='watch7-content')

        if len(soup_itemprop.contents) > 1:
            video = self.RESPONSE
            uploader = video['uploader']
            statistics = video['statistics']
            video['regionsAllowed'] = []

            video['id'] = id
            # Extract data from tags with 'itemprop' attribute
            for tag in soup_itemprop.find_all(itemprop=True, recursive=False):
                key = tag['itemprop']
                if key == 'name':
                    # Get video's title
                    video['title'] = tag['content']
                elif key == 'duration':
                    # Get video's duration
                    video['duration'] = self.make_duration(tag['content'])
                elif key == 'datePublished':
                    # Get video's upload date
                    video['upload_date'] = tag['content']
                elif key == 'genre':
                    # Get video's genre (category)
                    video['genre'] = tag['content']
                elif key == 'paid':
                    # Check if the video is paid
                    video['is_paid'] = self.is_true(tag['content'])
                elif key == 'unlisted':
                    # Check if the video is unlisted
                    video['is_unlisted'] = self.is_true(tag['content'])
                elif key == 'isFamilyFriendly':
                    # Check if the video is family-friendly
                    video['is_family_friendly'] = self.is_true(tag['content'])
                elif key == 'thumbnailUrl':
                    # Get video thumbnail URL
                    video['thumbnail_url'] = tag['href']
                elif key == 'interactionCount':
                    # Get video's views
                    statistics['views'] = int(tag['content'])
                elif key == 'channelId':
                    # Get uploader's channel ID
                    uploader['channel_id'] = tag['content']
                elif key == 'description':
                    # Get video description
                    video['description'] = tag['content']
                elif key == 'playerType':
                    video['playerType'] = tag['content']
                elif key == 'regionsAllowed':
                    # Get regions where the video is allowed
                    video['regionsAllowed'].extend(tag['content'].split(','))

            all_scripts = soup.find_all('script')
            for i in range(len(all_scripts)):
                try:
                    if 'ytInitialData' in all_scripts[i].string:
                        match = re.findall("label(.*)", re.findall("LIKE(.*?)like", all_scripts[i].string)[0])[0]
                        hasil = (''.join(match.split(',')).split("\"")[-1]).strip()
                        try:
                            video['statistics']['likes'] = eval(hasil)
                        except:
                            video['statistics']['likes'] = 0

                        match = re.findall("label(.*)", re.findall("DISLIKE(.*?)dislike", all_scripts[i].string)[0])[0]
                        hasil = (''.join(match.split(',')).split("\"")[-1]).strip()
                        try:
                            video['statistics']['dislikes'] = eval(hasil)
                        except:
                            video['statistics']['dislikes'] = 0
                except:
                    pass

            return self.RESPONSE

        return {'error': f'Video with the ID {id} does not exist'}
