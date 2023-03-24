from typing import List, Dict

from log import load_logging

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


class MHScrapper:
    def __init__(self, health_data_website, test=True):
        # load logger
        self.logger = load_logging(__name__)
        self.page = 1
        self.test = test
        options = Options()
        options.headless = True

        try:
            self.logger.info(f"Ministry of Health data scrapping has started...")
            self.driver = webdriver.Chrome(options=options)
            self.driver.get(health_data_website)
            self.driver.implicitly_wait(5)
        except Exception:
            self.logger.error("An error occurred opening the Ministry of Health webpage", exc_info=True)

    def scrape_mh_data(self):
        rows = []
        views = []

        while True:
            page_table = self.get_page_table()
            if self.page <= 1:
                header = self.get_table_headers(page_table)     # extract headers once as they don't change

            # extracts all row data of current page
            page_body = self.get_table_body(page_table)
            data = self.get_table_data(page_body)
            rows.append(data)

            # click each view button one by one and extract data then close
            view_buttons = self.get_page_view_buttons(page_body)
            view_button_data = self.click_extract_view_buttons_data(view_buttons)
            views.append(view_button_data)

            # move to next page and check if we're at final page
            page_bool = self.get_next_page()
            if page_bool is False:
                break
            if self.test is True:   # for testing purposes only scrapes 10 pages worth of data
                if self.page == 3:
                    break
        return {"header": header, "rows": rows, "views": views}

    def get_page_table(self) -> WebElement | None:
        try:
            page_table = self.driver.find_element(By.ID, "hosp")
            self.logger.info(f"getting table tag element for page {self.page}")
            return page_table
        except Exception:
            self.logger.error(f"An error occurred getting table tag element for page {self.page}", exc_info=True)
            return None

    @staticmethod
    def get_table_headers(page_table: WebElement) -> List[str]:
        table_headers_text = page_table.find_element(By.TAG_NAME, "thead").text
        table_headers_split = table_headers_text.split()
        return table_headers_split

    @staticmethod
    def get_table_body(page_table: WebElement) -> WebElement:
        body = page_table.find_element(By.TAG_NAME, "tbody")  # find body tag
        return body

    @staticmethod
    def get_table_data(table_body: WebElement) -> List[List[str]]:
        table_data_text = table_body.text  # find elements and return the text
        table_data_rows = table_data_text.split("\n")  # split the text data by newline command

        table_data_values = [row.split() for row in table_data_rows]
        return table_data_values

    @staticmethod
    def get_page_view_buttons(table_body: WebElement) -> list[WebElement]:
        buttons = table_body.find_elements(By.LINK_TEXT, "View")
        return buttons

    def click_extract_view_buttons_data(self, buttons: list[WebElement]) -> list[dict]:
        page_view_buttons_data = []
        count = 1
        for button in buttons:
            print(count)

            button.click()
            self.driver.implicitly_wait(2)

            view_panel = self.driver.find_element(By.CLASS_NAME, "panel-group")
            view_headers = self.get_drop_down_headers(view_panel)
            view_data = self.extract_view_drop_down_data(view_headers, view_panel)

            self.close_view_panel()   # close the current view button
            self.driver.implicitly_wait(2)

            count += 1


            page_view_buttons_data.append(view_data)
        return page_view_buttons_data

    @staticmethod
    def get_drop_down_headers(view_panel: WebElement) -> List[str]:
        drop_down_heading = view_panel.find_elements(By.CLASS_NAME, "panel-heading")    # find all heading objs

        drop_down_heading_text = [heading.text for heading in drop_down_heading]  # extract the heading text
        return drop_down_heading_text

    def extract_view_drop_down_data(self, drop_down_headers: List[str], view_panel: WebElement) -> Dict:
        views_data = {}
        clickable_headers = [view_panel.find_element(By.LINK_TEXT, header) for header in drop_down_headers]
        for clickable_header in clickable_headers:
            clickable_header.click()
            clickable_header_text = clickable_header.text.lower()
            if clickable_header_text == "identifiers":
                data = self.get_identifiers(view_panel)
            elif clickable_header_text == "location":
                data = self.get_location(view_panel)
            elif clickable_header_text == "contacts":
                data = self.get_contacts(view_panel)
            elif clickable_header_text == "status":
                data = self.get_status(view_panel)
            elif clickable_header.text == "services":
                data = self.get_services(view_panel)
            elif clickable_header.text == "personnel":
                data = self.get_personnel(view_panel)

            #self.close_view_panel(view_panel)
            views_data[clickable_header_text] = data

        return views_data

    @staticmethod
    def get_identifiers(view_panel: WebElement) -> dict[str, str]:
        facility_code = view_panel.find_element(By.ID, "unique_id").text
        state_unique_id = view_panel.find_element(By.ID, "state_unique_id").text
        registration_no = view_panel.find_element(By.ID, "registration_no").text
        facility_name = view_panel.find_element(By.ID, "facility_name").text
        alternate_name = view_panel.find_element(By.ID, "alt_facility_name").text
        start_date = view_panel.find_element(By.ID, "start_date").text
        ownership = view_panel.find_element(By.ID, "ownership").text
        ownership_type = view_panel.find_element(By.ID, "ownership_type").text
        facility_level = view_panel.find_element(By.ID, "facility_level").text
        facility_level_option = view_panel.find_element(By.ID, "facility_level_option").text
        days_of_operation = view_panel.find_element(By.ID, "operational_days").text
        hours_of_operation = view_panel.find_element(By.ID, "operational_hours").text

        data = {
            "facility_code": facility_code, "state_unique_id": state_unique_id,
            "registration_no": registration_no, "facility_name": facility_name,
            "alternate_name": alternate_name, "start_date": start_date,
            "ownership": ownership, "ownership_type": ownership_type,
            "facility_level": facility_level, "facility_level_option": facility_level_option,
            "days_of_operation": days_of_operation, "hours_of_operation": hours_of_operation
        }
        return data

    @staticmethod
    def get_location(view_panel: WebElement) -> dict[str, str]:
        state = view_panel.find_element(By.ID, "state").text
        lga = view_panel.find_element(By.ID, "lga").text
        ward = view_panel.find_element(By.ID, "ward").text
        physical_location = view_panel.find_element(By.ID, "physical_location").text
        postal_address = view_panel.find_element(By.ID, "postal_address").text
        longitude = view_panel.find_element(By.ID, "longitude").text
        latitude = view_panel.find_element(By.ID, "latitude").text

        data = {
            "state": state, "lga": lga, "ward": ward, "physical_location": physical_location,
            "postal_address": postal_address, "longitude": longitude, "latitude": latitude
        }
        return data

    @staticmethod
    def get_contacts(view_panel: WebElement) -> dict[str, str]:
        phone_number = view_panel.find_element(By.ID, "phone_number").text
        alternate_number = view_panel.find_element(By.ID, "alternate_number").text
        email_address = view_panel.find_element(By.ID, "email_address").text
        website = view_panel.find_element(By.ID, "website").text

        data = {
            "phone_number": phone_number, "alternate_number": alternate_number,
            "email_address": email_address, "website": website
        }
        return data

    @staticmethod
    def get_status(view_panel: WebElement) -> dict[str, str]:
        operation_status = view_panel.find_element(By.ID, "operation_status").text
        registration_status = view_panel.find_element(By.ID, "registration_status").text
        license_status = view_panel.find_element(By.ID, "license_status").text

        data = {
            "operation_status": operation_status, "registration_status": registration_status,
            "license_status": license_status
        }

        return data

    @staticmethod
    def get_services(view_panel):
        outpatient_service = view_panel.find_element(By.ID, 'outpatient').text
        inpatient_service = view_panel.find_element(By.ID, 'inpatient').text
        medical_service = view_panel.find_element(By.ID, 'medical').text
        surgical_service = view_panel.find_element(By.ID, 'surgical').text
        gynecology_service = view_panel.find_element(By.ID, 'gyn').text
        pediatrics_service = view_panel.find_element(By.ID, 'pediatrics').text
        dental_service = view_panel.find_element(By.ID, 'dental').text
        special_service = view_panel.find_element(By.ID, 'specialservice').text
        tot_num_beds = view_panel.find_element(By.ID, 'beds').text
        onsite_laboratory = view_panel.find_element(By.ID, 'onsite_laboratory').text
        onsite_imaging = view_panel.find_element(By.ID, 'onsite_imaging').text
        onsite_pharmarcy = view_panel.find_element(By.ID, 'onsite_pharmarcy').text
        mortuary_services = view_panel.find_element(By.ID, 'mortuary_services').text
        ambulance_services = view_panel.find_element(By.ID, 'ambulance_services').text

        data = {"outpatient_service": outpatient_service, "ambulance_services": ambulance_services,
                "mortuary_services": mortuary_services, "onsite_imaging": onsite_imaging,
                "onsite_pharmarcy": onsite_pharmarcy, "onsite_laboratory": onsite_laboratory,
                "tot_num_beds": tot_num_beds, "special_service": special_service,
                "dental_service": dental_service, "pediatrics_service": pediatrics_service,
                "gynecology_service": gynecology_service, "surgical_service": surgical_service,
                "medical_service": medical_service, "inpatient_service": inpatient_service}

        return data

    @staticmethod
    def get_personnel(view_panel):
        num_of_docs = view_panel.find_element(By.ID, 'doctors').text
        num_of_pharms = view_panel.find_element(By.ID, 'pharmacists').text
        num_of_pharm_technicians = view_panel.find_element(By.ID, 'pharmacy_technicians').text
        num_of_dentists = view_panel.find_element(By.ID, 'dentist').text
        num_of_dental_technicians = view_panel.find_element(By.ID, 'dental_technicians').text
        num_of_nurses = view_panel.find_element(By.ID, 'nurses').text
        num_of_midwifes = view_panel.find_element(By.ID, 'midwifes').text
        num_of_nurse_midwife = view_panel.find_element(By.ID, 'nurse_midwife').text
        num_of_lab_technicians = view_panel.find_element(By.ID, 'lab_technicians').text
        num_of_lab_scientists = view_panel.find_element(By.ID, 'lab_scientists').text
        num_of_him_officers = view_panel.find_element(By.ID, 'him_officers').text
        num_of_community_health_officer = view_panel.find_element(By.ID, 'community_health_officer').text
        num_of_community_extension_workers = view_panel.find_element(By.ID, 'community_extension_workers').text
        num_of_jun_community_extension_worker = view_panel.find_element(By.ID, 'jun_community_extension_worker').text
        num_of_env_health_officers = view_panel.find_element(By.ID, 'env_health_officers').text
        num_of_health_attendants = view_panel.find_element(By.ID, 'attendants').text

        data = {"num_of_docs": num_of_docs, "num_of_pharms": num_of_pharms,
                "num_of_midwifes": num_of_midwifes, "num_of_nurses": num_of_nurses,
                "num_of_nurse_midwife": num_of_nurse_midwife, "num_of_pharm_technicians": num_of_pharm_technicians,
                "num_of_dentists": num_of_dentists, "num_of_health_attendants": num_of_health_attendants,
                "num_of_env_health_officers": num_of_env_health_officers, "num_of_him_officers": num_of_him_officers,
                "num_of_community_health_officer": num_of_community_health_officer,
                "num_of_jun_community_extension_worker": num_of_jun_community_extension_worker,
                "num_of_community_extension_workers": num_of_community_extension_workers,
                "num_of_dental_technicians": num_of_dental_technicians,
                "num_of_lab_technicians": num_of_lab_technicians,
                "num_of_lab_scientists": num_of_lab_scientists}

        return data

    def close_view_panel(self) -> None:
        views_footer = self.driver.find_element(By.CLASS_NAME, "modal-footer")
        close_button = views_footer.find_element(By.TAG_NAME, "button")
        close_button.send_keys(Keys.ESCAPE)

    def get_next_page(self) -> bool:
        pagination = self.driver.find_element(By.CLASS_NAME, "pagination")
        try:
            next_page = pagination.find_element(By.LINK_TEXT, '›')
            next_page.click()
            self.page += 1
            return True
        except NoSuchElementException:
            self.logger.info("End of Health Ministry data pages")
            return False
