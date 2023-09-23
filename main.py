'''
The default mode of the program is to run in test mode, when it does this, it'll scrape the data on 3 pages max and display
the browser. When the goal is to scrape all the data on the ministry of health webpage pass in the argument value of
'False' to the class instance assides the website, this will scrape all the data and hide the web browser display
'''
import os.path

from src.extraction_script import MHScrapper
import json
import tempfile
import shutil

scraper = MHScrapper(start_page=18)
result = scraper.scrape_mh_data()
temp_dir = tempfile.mkdtemp(prefix="unclean_data", suffix="")


for key, value in result.items():
    temp_file_path = os.path.join(temp_dir, f"{key}.json")
    with open(temp_file_path, 'w') as temp_json:
        json.dump(value, temp_json, indent=1)

