# wikipedia_data_fetcher.py
import requests
from bs4 import BeautifulSoup

class WikipediaDataFetcher:
    @staticmethod
    
# Helper function to fetch data from the Wikipedia API based on the provided topic
    def fetch_wikipedia_data(topic):
        try:
            # Construct the Wikipedia API URL for the specified topic to get the page ID
            page_id_url = f'https://en.wikipedia.org/w/api.php?action=query&format=json&titles={topic}'

            # Make a GET request to get the page ID
            response = requests.get(page_id_url)
            response.raise_for_status()
            data = response.json()

            # Get the page ID from the API response
            page_id = list(data['query']['pages'].keys())[0]

            # Use the obtained page ID to construct the URL for fetching the full content
            full_content_url = f'https://en.wikipedia.org/w/api.php?action=query&format=json&pageids={page_id}&prop=extracts'

            # Make a GET request to fetch the full content
            response = requests.get(full_content_url)
            response.raise_for_status()

            # Parse the JSON response and return the data
            return response.json()

        except requests.exceptions.RequestException as e:
            return None

    @staticmethod
    def clean_article_text(article_text):
        clean_text = BeautifulSoup(article_text, 'html.parser').get_text()

        return clean_text
