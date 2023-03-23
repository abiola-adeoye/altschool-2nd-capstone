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
        while True:
            page = self.get_page_table()
            header = self.get_table_headers(page)
            data = self.get_table_data(page)
            page_bool = self.get_next_page()
            if page_bool is False:
                break
            if self.test is True:
                if self.page == 10:
                    break

    def get_page_table(self):
        try:
            page_table = self.driver.find_element(By.ID, "hosp")
            self.logger.info(f"getting table tag element for page {self.page}")
        except Exception:
            self.logger.error("An error occurred opening the Ministry of Health webpage", exc_info=True)
        return page_table

    def get_next_page(self):
        pagination = self.driver.find_element(By.CLASS_NAME, "pagination")
        try:
            next_page = pagination.find_element(By.LINK_TEXT, '›')
            next_page.click()
            self.page += 1
        except NoSuchElementException:
            self.logger.info("End of Health Ministry data pages")
            return False

    @staticmethod
    def get_table_headers(page_table):
        table_headers_text = page_table.find_element(By.TAG_NAME, "thead").text
        table_headers_split = table_headers_text.split()
        return table_headers_split

    @staticmethod
    def get_table_data(page_table):
        table_data_text = page_table.find_element(By.TAG_NAME, "tbody").text    #find elements and return the text
        table_data_rows = table_data_text.split("\n")   #split the text data by newline command

        table_data_values = [ row.split() for row in table_data_rows ]
        return table_data_values


