import logging
import os


class FileManager:
    @staticmethod
    def ensure_directory_exists(directory: str) -> None:
        if not os.path.exists(directory):
            logging.info(f"Creating directory: {directory}")
            os.makedirs(directory)

    @staticmethod
    def save_file(path: str, content: bytes) -> None:
        with open(path, 'wb') as file:
            file.write(content)
        logging.info(f"Saved file {path}")
