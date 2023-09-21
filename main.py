'''
The default mode of the program is to run in test mode, when it does this, it'll scrape the data on 10 pages and display
the web drowser. When the goal is to scrape all the data on the ministry of health webpage pass in the argument value of
'False' to the class instance assides the website, this will scrape all the data and hide the web browser display
'''
from src import transform_script
from src.extraction_script import MHScrapper
from sqlalchemy import create_engine
import pandas as pd

# change these values to your personal db params
user = "postgres"
password = "dob10012000"
host = "localhost"
port = 5433
db = "capstone2"

# the db engine would be used to insert data into a postgresdb
engine = create_engine("postgresql://" + user + ":" +
                       password + "@" + host + ":" + str(port) + "/" + db)


website = "https://hfr.health.gov.ng/facilities/hospitals-search?_token=46DimSGFwpf0Hz6fkdg4kceauIDPrSjFNh6FiWMN&state_id=1&lga_id=1&ward_id=0&facility_level_id=0&ownership_id=0&operational_status_id=0&registration_status_id=0&license_status_id=0&geo_codes=0&service_type=0&service_category_id=0&facility_name=&entries_per_page=100"
data = MHScrapper(website)
result = data.scrape_mh_data()
file_path = "C:/Users/HP/Documents/"     # change this to the directory you want to save to

for key in result:
    data_table_df = pd.DataFrame.from_records(result[key])
    data_table_df.to_csv(file_path+f"{key}.csv", index=False, sep=";")      # save extracted data
    if key =="page_rows":
        transform_script.clean_load_page_rows(file_path + f"{key}.csv", transform_script.dtype_pages, engine)
    elif key == "identifiers":
        transform_script.clean_load_identifiers(file_path + f"{key}.csv", transform_script.dtype_identifiers, engine)
    elif key == "locations":
        transform_script.clean_load_locations(file_path + f"{key}.csv", transform_script.dtype_locations, engine)
    elif key == "contacts":
        transform_script.clean_load_contacts(file_path + f"{key}.csv", transform_script.dtype_contacts, engine)
    elif key == "status":
        transform_script.clean_load_status(file_path + f"{key}.csv", transform_script.dtype_status, engine)
    elif key == "services":
        transform_script.clean_load_services(file_path + f"{key}.csv", transform_script.dtype_services, engine)
    elif key == "personnel":
        transform_script.clean_load_personnel(file_path + f"{key}.csv", transform_script.dtype_personnel, engine)
