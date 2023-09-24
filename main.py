'''
The default mode of the program is to run in test mode, when it does this, it'll scrape the data on 3 pages max and display
the browser. When the goal is to scrape all the data on the ministry of health webpage pass in the argument value of
'False' to the class instance assides the website, this will scrape all the data and hide the web browser display
'''
from src.gcp_bucket import MHGCPStorage
from src.extraction_script import MHScrapper


scraper = MHScrapper(test=False, start_page=1, stop_page=4)
gcp_storage = MHGCPStorage('ministry-health-data-proj')
result = scraper.scrape_mh_data()


for key, value in result.items():
    gcp_storage.create_or_append_json_data(key, value)