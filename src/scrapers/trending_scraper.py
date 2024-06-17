import logging
from ..constants import GITHUB_TRENDING_URL
from selenium.webdriver.common.by import By


class TrendingRepositoriesScraper:
    def __init__(self, client) -> None:
        self.client = client

    def get_trending_repositories(self) -> list:
        logging.info("Fetching trending repositories...")
        self.client.driver.get(GITHUB_TRENDING_URL)
        trending_repos_elements = self.client.driver.find_elements(By.CSS_SELECTOR, "article.Box-row h2.h3.lh-condensed a.Link")
        repos = [element.get_attribute('href') for element in trending_repos_elements]
        logging.info(f"Found {len(repos)} trending repositories.")
        return repos
