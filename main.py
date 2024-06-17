import os
import logging
from dotenv import load_dotenv
from src.clients.github_client import GitHubClient
from src.scrapers.trending_scraper import TrendingRepositoriesScraper
from src.downloaders.readme_downloader import ReadmeDownloader
from src.utils.file_manager import FileManager


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


load_dotenv()

if __name__ == "__main__":
    github_username = os.getenv("GITHUB_USERNAME")
    github_password = os.getenv("GITHUB_PASSWORD")

    if github_username is None or github_password is None:
        logging.error("GitHub credentials not found. Please check your .env file.")
        exit(1)

    client = GitHubClient(github_username, github_password)

    if not client.connected:
        logging.error("Exiting due to failed GitHub login.")
        exit(1)

    scraper = TrendingRepositoriesScraper(client)
    downloader = ReadmeDownloader(client)
    FileManager.ensure_directory_exists('readme_trending')

    repo_links = scraper.get_trending_repositories()
    for link in repo_links:
        readme_content = downloader.download_readme(link)
        if readme_content:
            file_path = os.path.join('readme_trending', os.path.basename(link) + '-README.md')
            FileManager.save_file(file_path, readme_content)