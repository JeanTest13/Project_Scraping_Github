import logging
from selenium.common.exceptions import NoSuchElementException
import requests

class ReadmeDownloader:
    def __init__(self, client) -> None:
        self.client = client

    def find_readme_path(self, repository_url: str) -> str:
        try:
            self.client.driver.get(repository_url)
            readme_element = self.client.driver.find_element_by_xpath("//*[contains(text(), 'README.md')]")
            readme_url = readme_element.get_attribute('href')
            return readme_url
        except NoSuchElementException:
            logging.error(f"README.md not found in repository: {repository_url}")
            return None

    def download_readme(self, readme_url: str) -> bytes:
        try:
            response = requests.get(readme_url)
            if response.status_code == 200:
                return response.content
            else:
                logging.error(f"Failed to download README from {readme_url}, status code: {response.status_code}")
        except requests.RequestException as e:
            logging.error(f"Error downloading README from {readme_url}: {e}")
            return None
