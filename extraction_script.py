from selenium import webdriver

driver = webdriver.Chrome()
health_data_website = "https://hfr.health.gov.ng/facilities/hospitals-search?" \
                      "_token=uHw9x4DLz9c8MwyEEHT7icRzqQ58EbDYmDotb9Ez&state_id=1&ward_id=0&facility_level" \
                      "_id=0&ownership_id=0&operational_status_id=1&registration_status_id=2&license_status_" \
                      "id=1&geo_codes=0&service_type=0&service_category_id=0&entries_per_page=20&page=1#"

driver.get(health_data_website)



driver.close()