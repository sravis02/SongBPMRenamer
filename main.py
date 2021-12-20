import requests
from headers import headers
from bs4 import BeautifulSoup as bs

class BpmScraper:
    def __init__(self, folderPath):
        self.folderPath = folderPath

    def getBeatportTrack(self, keyword):
        params = (
            ('q', keyword),
            ('_pjax', '#pjax-inner-wrapper'),
        )

        try:
            response = requests.get('https://www.beatport.com/search', headers=headers, params=params)
            response.raise_for_status()
        except Exception as e: 
            print(f"Error occured while fetching by keyword {keyword}: {e.args[0]}")
            return None

        soup = bs(response.text, "html.parser")
        tracksDiv = soup.find(class_="bucket tracks standard-interior-tracks")
        tracks = tracksDiv.find_all(class_="bucket-item")

        searchResults = []
        for track in tracks:

            trackId = track.get("data-ec-id")
            trackName = track.get("data-ec-name")
            trackArtist = track.get("data-ec-d")
            trackGenre = track.get("data-ec-d3")

            searchResults.append({
                "id":trackId,
                "title": f"{trackName} - {trackArtist}",
                "genre":trackGenre,
            })


        return searchResults

    def run(self):
        print(self.getBeatportTrack("dj ogi ommp"))

scraper = BpmScraper("C:\\ExamplePath");
scraper.run()
