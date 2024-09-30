"""
Main module to execute the Indeed job scraping and database storage process.
"""
from crawler import IndeedJobScraper
from database import DatabaseManager

if __name__ == "__main__":
    job_scraper = IndeedJobScraper()

    job_scraper.navigate_to_indeed()
    job_scraper.search_jobs()
    job_scraper.scrape_jobs()

    db_manager = DatabaseManager()
    db_manager.create_jobs_table()
    db_manager.store_data(job_scraper.jobs_list, job_scraper.company_list, job_scraper.location_list)

    job_scraper.quit_driver()
