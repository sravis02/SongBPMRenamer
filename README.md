# Song BPM Renamer
When creating music mixtapes you often need to know the bpm count from plenty tracks at once.
This tool automatically fetches the bpm of your audio files from the internet and then prepends the bpm count to the original audio file name in your directory.

Instead of technically detecting the bpm, the application fetches a website to pick up the bpm data (webscraping).

## Getting Started
 - Clone this repository
 - Navigate into the folder
 - Create virual environment: `python -m venv renamer_env`
 - Activate it: `renamer_env\Scripts\activate.bat`(windows) `source renamer_env/bin/activate`(mac)
 - Install dependencies: `pip install -r requirements.txt`
 - Insert your folder path inside the constructor (main.py, ln. 175)
 - Execute main file: `python main.py`

## Requirements:
 - Names of the audio files must include keywords about the song
 - Wifi connection is necessary

## Further Improvements
 - Fetch all search results at once and asynchronously
 - Improve error handling
 - Better CLI UX


