'''
The default mode of the program is to run in test mode, when it does this, it'll scrape the data on 10 pages and display
the web drowser. When the goal is to scrape all the data on the ministry of health webpage pass in the argument value of
'False' to the class instance assides the website, this will scrape all the data and hide the web browser display
'''

from extraction_script import MHScrapper
import pandas as pd


website = "https://hfr.health.gov.ng/facilities/hospitals-search?_token=46DimSGFwpf0Hz6fkdg4kceauIDPrSjFNh6FiWMN&state_id=1&lga_id=1&ward_id=0&facility_level_id=0&ownership_id=0&operational_status_id=0&registration_status_id=0&license_status_id=0&geo_codes=0&service_type=0&service_category_id=0&facility_name=&entries_per_page=1000"
data = MHScrapper(website, False)
result = data.scrape_mh_data()

for key in result:
    data_table_df = pd.DataFrame.from_records(result[key])
    data_table_df.to_csv(f"C:/Users/HP/Documents/{key}.csv", index=False)
