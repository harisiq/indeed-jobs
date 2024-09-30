"""
Crawler module for scraping job listings from the Indeed website.
"""

import time
from typing import List, Tuple
from selenium.webdriver import Chrome
from selenium.common.exceptions import NoSuchElementException
from loguru import logger
from enums import WebConfig, JobConfig

class IndeedJobScraper:
    def __init__(self):
        """
        Initialize the IndeedJobScraper.
        """
        self.job_title = JobConfig.JOB_TITLE.value
        self.location = JobConfig.LOCATION.value
        self.jobs_list: List[str] = []
        self.company_list: List[str] = []
        self.location_list: List[str] = []
        self.driver = Chrome()

    def navigate_to_indeed(self):
        """
        Navigate to the location
        """
        self.driver.get(WebConfig.INDEED_URL.value)
        time.sleep(2)

    def search_jobs(self):
        """
        Perform a job search on Indeed.
        """
        job_search = self.driver.find_element("xpath", '//input[@id="text-input-what"]')
        job_search.send_keys(self.job_title)

        location_search = self.driver.find_element("xpath", '//input[@id="text-input-where"]')
        location_search.send_keys(self.location)

        find_btn = self.driver.find_element("xpath", '//button[@type="submit"]')
        find_btn.click()
        time.sleep(5)

    def extract_job_details(self, job) -> Tuple[str, str, str]:
        """
        Extract job details from a job element.
        """
        try:
            title_element = job.find_element("xpath", './/h2[contains(@class, "jobTitle")]/a/span').text
            company_element = job.find_element("xpath", './/span[@data-testid="company-name"]').text
            location_element = job.find_element("xpath", './/div[@data-testid="text-location"]').text

            return title_element, company_element, location_element
        except NoSuchElementException as e:
            logger.warning(f"Error fetching job details: {e}")
            return "", "", ""

    def scrape_jobs(self):
        """
        Scrape job listings from Indeed.
        """
        while True:
            try:
                self.close_modal_if_present()

                job_containers = self.driver.find_elements("xpath", '//div[@id="mosaic-provider-jobcards"]//div[contains(@class, "cardOutline")]')
                logger.info(f"Number of job containers found on page {self.driver.current_url}: {len(job_containers)}")

                for job in job_containers:
                    title, company, location = self.extract_job_details(job)
                    self.jobs_list.append(title)
                    self.company_list.append(company)
                    self.location_list.append(location)

                self.move_to_next_page()
                time.sleep(2)

            except NoSuchElementException:
                logger.info("No more pages available.")
                break

    def close_modal_if_present(self):
        """
        Close the modal window if it is present.
        """
        try:
            close_modal_button = self.driver.find_element("xpath", '//button[@aria-label="close"]')
            close_modal_button.click()
            time.sleep(1)
        except NoSuchElementException:
            pass

    def move_to_next_page(self):
        """
        Move to the next page of job listings
        """
        next_page = self.driver.find_element("xpath", '//a[@data-testid="pagination-page-next"]')
        next_page.click()
        time.sleep(2)

    def quit_driver(self):
        self.driver.quit()
