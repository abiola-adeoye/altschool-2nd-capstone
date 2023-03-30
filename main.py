'''
The default mode of the program is to run in test mode, when it does this, it'll scrape the data on 10 pages and display
the web drowser. When the goal is to scrape all the data on the ministry of health webpage pass in the argument value of
'False' to the class instance assides the website, this will scrape all the data and hide the web browser display
'''
import transform_script
from extraction_script import MHScrapper
from sqlalchemy import create_engine
import pandas as pd

user = "insert your db username here"
password = "insert your password here"
host = "insert your host name here"
port = "insert the port number as an int here"
db = "insert the name of the db you want to insert into here"

# the db engine would be used to insert data into a postgresdb
engine = create_engine("postgresql://" + user + ":" +
                       password + "@" + host + ":" + str(port) + "/" + db)


website = "https://hfr.health.gov.ng/facilities/hospitals-search?_token=46DimSGFwpf0Hz6fkdg4kceauIDPrSjFNh6FiWMN&state_id=1&lga_id=1&ward_id=0&facility_level_id=0&ownership_id=0&operational_status_id=0&registration_status_id=0&license_status_id=0&geo_codes=0&service_type=0&service_category_id=0&facility_name=&entries_per_page=1000"
data = MHScrapper(website, False)
result = data.scrape_mh_data()

for key in result:
    data_table_df = pd.DataFrame.from_records(result[key])
    data_table_df.to_csv(f"C:/Users/HP/Documents/{key}.csv", index=False, sep=";")      # save extracted data
    if key =="page_rows":
        transform_script.clean_load_page_rows(f"C:/Users/HP/Documents/{key}.csv", transform_script.dtype_pages, engine)
    elif key == "identifiers":
        transform_script.clean_load_identifiers(f"C:/Users/HP/Documents/{key}.csv", transform_script.dtype_identifiers, engine)
    elif key == "locations":
        transform_script.clean_load_locations(f"C:/Users/HP/Documents/{key}.csv", transform_script.dtype_locations, engine)
    elif key == "contacts":
        transform_script.clean_load_contacts(f"C:/Users/HP/Documents/{key}.csv", transform_script.dtype_contacts, engine)
    elif key == "status":
        transform_script.clean_load_status(f"C:/Users/HP/Documents/{key}.csv", transform_script.dtype_status, engine)
    elif key == "services":
        transform_script.clean_load_services(f"C:/Users/HP/Documents/{key}.csv", transform_script.dtype_services, engine)
    elif key == "personnel":
        transform_script.clean_load_personnel(f"C:/Users/HP/Documents/{key}.csv", transform_script.dtype_personnel, engine)
