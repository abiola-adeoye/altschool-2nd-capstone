from log import load_logging

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


class MHScrapper:
    def __init__(self, health_data_website, test=True):
        # load logger
        self.logger = load_logging(__name__)
        self.page = 1
        self.test = test

        try:
            self.logger.info(f"Minitry of Health data scrapping has started...")
            self.driver = webdriver.Chrome()
            self.driver.get(health_data_website)
            self.driver.implicitly_wait(5)
        except Exception:
            self.logger.error("An error occurred opening the Ministry of Health webpage", exc_info=True)

    def scrape_mh_data(self):
        rows = []

        page = self.get_page_table()
        header = self.get_table_headers(page)

        body = self.get_table_body(page)
        data = self.get_table_data(body)

        rows.append(data)

        self.get_next_page()
        while True:
            page = self.get_page_table()

            data = self.get_table_data(page)
            rows.append(data)

            page_bool = self.get_next_page()
            if page_bool is False:
                break
            if self.test is True:
                if self.page == 10:
                    break
        return {"header":header, "rows":rows}

    def get_page_table(self):
        try:
            page_table = self.driver.find_element(By.ID, "hosp")
            self.logger.info(f"getting table tag element for page {self.page}")
        except Exception:
            self.logger.error("An error occurred opening the Ministry of Health webpage", exc_info=True)
        return page_table

    @staticmethod
    def get_table_headers(page_table):
        table_headers_text = page_table.find_element(By.TAG_NAME, "thead").text
        table_headers_split = table_headers_text.split()
        return table_headers_split

    @staticmethod
    def get_table_body(page_table):
        return page_table.find_element(By.TAG_NAME, "tbody")  # find body tag

    def get_table_data(self, table_body):
        table_data_text = table_body.text  # find elements and return the text
        table_data_rows = table_data_text.split("\n")  # split the text data by newline command

        table_data_values = [row.split() for row in table_data_rows]
        return table_data_values

    @staticmethod
    def get_page_view_buttons(self, table_body):
        buttons = table_body.find_elements(By.LINK_TEXT, "View")
        return buttons

    def click_extract_view_buttons_data(self, buttons):
        views_data = []
        for button in buttons:
            button.click()
            view_panel = self.driver.find_element(By.CLASS_NAME, "panel-group")
            view_headers = self.get_drop_down_headers(view_panel)
            button_data = self.extract_view_drop_down_data(view_headers, view_panel)

            views_data.append(button_data)

    @staticmethod
    def get_drop_down_headers(view_panel):
        drop_down_heading = view_panel.find_elements(By.CLASS_NAME, "panel-heading")    # find all heading objs

        drop_down_heading_text = [heading.text for heading in drop_down_heading]  # extract the heading text
        return drop_down_heading_text

    def extract_view_drop_down_data(self, drop_down_headers, view_panel):
        views_data = {}
        count = 1

        clickable_headers = [view_panel.find_element(By.LINK_TEXT, header) for header in drop_down_headers]
        for clickable_header in clickable_headers:
            clickable_header.click()
            clickable_header_text = clickable_header.text.lower()
            if clickable_header_text == "identifiers":
                data = self.get_identifiers()
            elif clickable_header_text == "location":
                data = self.get_location()
            elif clickable_header_text == "contacts":
                data = self.get_contacts()
            elif clickable_header_text == "status":
                data = self.get_status()
            elif clickable_header.text == "services":
                data = self.get_services()
            elif clickable_header.text == "personnel":
                data = self.get_personnel()

            views_data[clickable_header_text] = data

        return views_data

    @staticmethod
    def get_identifiers(view_panel):
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
            "facility_level": facility_level,"facility_level_option":facility_level_option,
            "days_of_operation":days_of_operation, "hours_of_operation": hours_of_operation
        }
        return data





    @staticmethod
    def get_location(view_panel):
        pass

    @staticmethod
    def get_contacts(view_panel):
        pass

    @staticmethod
    def get_status(view_panel):
        pass

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


        data = {"outpatient_service":outpatient_service,"ambulance_services":ambulance_services,"mortuary_services":mortuary_services,
                "onsite_imaging":onsite_imaging,"onsite_pharmarcy":onsite_pharmarcy,"onsite_laboratory":onsite_laboratory,
                "tot_num_beds":tot_num_beds,"special_service":special_service,"dental_service":dental_service,
                "pediatrics_service":pediatrics_service, "gynecology_service":gynecology_service, "surgical_service":surgical_service,
                "medical_service":medical_service,"inpatient_service":inpatient_service}

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

        data = {"num_of_docs":num_of_docs,"num_of_pharms": num_of_pharms,"num_of_midwifes": num_of_midwifes,
                "num_of_nurses":num_of_nurses, "num_of_nurse_midwife":num_of_nurse_midwife,
                "num_of_pharm_technicians":num_of_pharm_technicians,"num_of_dentists":num_of_dentists,
                "num_of_health_attendants":num_of_health_attendants,"num_of_env_health_officers": num_of_env_health_officers,
                "num_of_him_officers":num_of_him_officers,"num_of_community_health_officer":num_of_community_health_officer,
                "num_of_jun_community_extension_worker":num_of_jun_community_extension_worker,
                "num_of_community_extension_workers":num_of_community_extension_workers,"num_of_dental_technicians":num_of_dental_technicians,
                "num_of_lab_technicians":num_of_lab_technicians,"num_of_lab_scientists":num_of_lab_scientists}

        return data


    @staticmethod
    def close_view_panel(view_button):
        view_button.send_keys(Keys.ESCAPE)

    def get_next_page(self):
        pagination = self.driver.find_element(By.CLASS_NAME, "pagination")
        try:
            next_page = pagination.find_element(By.LINK_TEXT, '›')
            next_page.click()
            self.page += 1
        except NoSuchElementException:
            self.logger.info("End of Health Ministry data pages")
            return False
