import argparse
import logging
import os
from io import BytesIO
from zipfile import ZipFile

import requests

from collect_summaries import scrape_summaries, SHMOOP_URL


LOG_FORMAT = '%(asctime)s - %(levelname)s: %(message)s'
LOG_DATEFORMAT = '%Y-%m-%d %H:%M:%S'
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT, datefmt=LOG_DATEFORMAT)
logger = logging.getLogger(__name__)

SCRAPED_DATA_PATH = './scraped_data'

STORIES_URL = 'http://www.cs.toronto.edu/~atef/stories.zip'
ALIGNMENTS_URL = 'http://www.cs.toronto.edu/~atef/manual_alignments.zip'


def setup_environment():
    """Set up the environment."""
    os.makedirs(SCRAPED_DATA_PATH, exist_ok=True)


def get_stories():
    """Get the stories."""
    logger.info(f"Collecting stories from '{STORIES_URL}'.")
    response = requests.get(STORIES_URL)

    logger.info("Decompressing stories files.")
    files = ZipFile(BytesIO(response.content))
    files.extractall(SCRAPED_DATA_PATH)
    logger.info("Decompression finished successfully.")


def get_summaries():
    """Get the summaries."""
    logger.info(f"Collecting summaries from '{SHMOOP_URL}'.")
    scrape_summaries()


def get_alignments():
    """Get the manual alignments."""
    logger.info(f"Collecting alignments from '{ALIGNMENTS_URL}'.")
    response = requests.get(ALIGNMENTS_URL)

    logger.info("Decompressing alignments files.")
    files = ZipFile(BytesIO(response.content))
    files.extractall(SCRAPED_DATA_PATH)
    logger.info("Decompression finished successfully.")


def get_all():
    """Get the stories, summaries and manual alignments."""
    get_stories()
    get_summaries()
    get_alignments()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Data hunter process parser')
    parser.add_argument('-r', '--resource', choices=['stories', 'summaries', 'alignments', 'all'], default='all',
                        help="Resource to collect ['stories', 'summaries', 'alignments', 'all']. Defaults 'all'.")
    args = parser.parse_args()

    setup_environment()

    logging.info(f"Extracting {args.resource} resources.")
    globals().get(f'get_{args.resource}')()
