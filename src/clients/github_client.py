from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotInteractableException
from webdriver_manager.chrome import ChromeDriverManager
from ..constants import GITHUB_LOGIN_URL, GITHUB_SETTING_APPEARANCE
import logging


class GitHubClient:
    def __init__(self, username: str, password: str) -> None:
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.connected = self.connection_to_our_github(username, password)

    def connection_to_our_github(self, username: str, password: str) -> bool:
        try:
            self.driver.get(GITHUB_LOGIN_URL)
            self.driver.find_element(By.ID, "login_field").send_keys(username)
            self.driver.find_element(By.ID, "password").send_keys(password + Keys.RETURN)

            WebDriverWait(self.driver, 10).until(EC.url_changes(GITHUB_LOGIN_URL))

            self.driver.get(GITHUB_SETTING_APPEARANCE)
            WebDriverWait(self.driver, 10).until(
                lambda d: d.current_url != GITHUB_LOGIN_URL
            )

            if self.driver.current_url == GITHUB_SETTING_APPEARANCE:
                logging.info("Connected to GitHub.")
                return True
            else:
                logging.error("Failed to log in to GitHub. Check your credentials.")
                return False

        except TimeoutException:
            logging.error("Login timeout or redirection to login page.")
            return False
        except Exception as e:
            logging.error(f"Error during login: {e}")
            return False