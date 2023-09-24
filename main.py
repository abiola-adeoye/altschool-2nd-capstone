# The program by default runs in test mode, it'll scrape the data on 3 pages max and push to the gcp bucket
# When the goal is not to run in test mode, instantiate the MHScrapper class with the arg 'test=False'

from src.gcp_bucket import MHGCPStorage
from src.extraction_script import MHScrapper


scraper = MHScrapper(test=False, start_page=1, stop_page=4)
result = scraper.scrape_mh_data()
gcp_storage = MHGCPStorage('ministry-health-data-proj')

for key, value in result.items():
    gcp_storage.create_or_append_json_data(key, value)
