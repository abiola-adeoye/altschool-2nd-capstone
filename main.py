'''
The default mode of the program is to run in test mode, when it does this, it'll scrape the data on 10 pages and display
the web drowser. When the goal is to scrape all the data on the ministry of health webpage pass in the argument value of
'False' to the class instance assides the website, this will scrape all the data and hide the web browser display
'''
from src import transform_script
from src.extraction_script import MHScrapper
from sqlalchemy import create_engine
import pandas as pd

scraper = MHScrapper(start_page=18)
result = scraper.scrape_mh_data()

# create a temp file path