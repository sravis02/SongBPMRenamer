import requests
from constants import HEADERS, AUDIO_FILE_TYPES
from bs4 import BeautifulSoup as bs
from os import listdir, rename
from os.path import join

class BpmScraper:
    def __init__(self, folderPath):
        self.folderPath = folderPath


    def _getBeatportResults(self, keyword):
        # Fetch API
        try:
            response = requests.get('https://www.beatport.com/search', headers=HEADERS, params=(
                ('q', keyword),
                ('_pjax', '#pjax-inner-wrapper'),
            ))
            response.raise_for_status()
        except Exception as e: 
            print(f"Error occured while fetching by keyword {keyword}: {e.args[0]}")
            return None

        # Parse html elements for each result
        soup = bs(response.text, "html.parser")
        tracks = soup.find_all(class_="bucket-item ec-item track")

        # Serialize html to json
        searchResults = []
        for track in tracks:
            trackId = track.get("data-ec-id")
            trackName = track.get("data-ec-name")
            trackArtist = track.get("data-ec-d1")
            trackGenre = track.get("data-ec-d3")

            searchResults.append({
                "id":trackId,
                "title": f"{trackName} - {trackArtist}",
                "genre":trackGenre,
            })

        return searchResults
    

    def _selectResult(self, searchResults, keyword):
        if len(searchResults) == 0:
            print(f"No results for \"{keyword}\"\n")
            return None

        # Output search results
        print(f"{len(searchResults)} results for \"{keyword}\"\n")
        for index, result in enumerate(searchResults):
            title = result.get("title")
            genre = result.get("genre")
            print(f"[{index}] {title}\n   Genre: {genre}")
        
        print("---\nInput an index to select a track: ")
        print("Or type \"skip\"")
        
        # User input handling
        while True:
            userInput = input()

            if(userInput.upper() == "SKIP"):
                print(f"Audio file process skipped for \"{keyword}\"")
                return None
            try:
                resultIndex = int(userInput)
            except ValueError:
                print("Input a number and retry please")
            else:
                if(resultIndex < len(searchResults) and resultIndex > -1):
                    selectedResult = searchResults[resultIndex]
                    return selectedResult.get("id")
                else:
                    print("Invalid number, please retry")


    def _getFoldersAudioFiles(self):
        fileList = listdir(self.folderPath)

        # Exclude non audio files
        def filterFunction(file):
            for fileType in AUDIO_FILE_TYPES:
                if(file.endswith(fileType)):
                    return True
            return False

        return list(filter(filterFunction, fileList))


    def _removeFileType(self, fileName):
        splitted = fileName.split(".")
        del splitted[-1]
        return ".".join(splitted)


    def _initFilesCollection(self, filesList):
        self.filesCollection = []
        for file in filesList:
            element = {
                "fileName":file,
                "keyword":self._removeFileType(file),
                "beatportId": None,
                
            }
            self.filesCollection.append(element)
        

    def _insertBeatportIds(self):
        for fileData in self.filesCollection:
            keyword = fileData.get("keyword")
            searchResults = self._getBeatportResults(keyword)
            # Select track by user input
            beatportId = self._selectResult(searchResults, keyword)
            # If no correct result found (/skipped) continue with next file
            if not beatportId:
                continue
            else:
                fileData["beatportId"] = beatportId


    def _getBpm(self, beatportId):
        try:
            response = requests.get(f"https://www.beatport.com/track/-/{beatportId}", headers=HEADERS)
            response.raise_for_status()
        except Exception as e: 
            print(f"Error occured while fetching Track {beatportId}: {e.args[0]}")
            return None
        
        soup = bs(response.text, "html.parser")
        parentElement = soup.find(class_="interior-track-bpm")
        element = parentElement.find("span", class_="value")

        return element.text
    

    def _changeFileName(self, oldFileName, newFileName):
        oldFilePath = join(self.folderPath, oldFileName)
        newFilePath = join(self.folderPath, newFileName)

        rename(oldFilePath, newFilePath)


    def run(self):
        audioFilesList = self._getFoldersAudioFiles()
        print(f"#####\nFound {len(audioFilesList)} audio files\n#####\n")

        # filesCollection contains data for each file
        self._initFilesCollection(audioFilesList)
        # Fetch search results by kw, select result by user input, insert beatportId into filesCollection
        self._insertBeatportIds()

        for fileData in self.filesCollection:
            beatportId = fileData.get("beatportId")
            if not beatportId:
                continue
            
            # Fetching BPM
            print("Fetching BPM...")
            bpm = self._getBpm(beatportId)
            if not bpm:
                print("Skipping File...")
                continue
            fileData["bpm"] = bpm

            # Renaming
            oldFileName = fileData.get("fileName")
            newFileName = f"{bpm}_{oldFileName}"
            print(f"Renaming to {newFileName}")
            self._changeFileName(oldFileName, newFileName)


scraper = BpmScraper("C:\\Users\\lucas\\Documents\\mixtapes\\technonewera");
scraper.run()

