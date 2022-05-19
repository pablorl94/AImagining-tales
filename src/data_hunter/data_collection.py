import argparse
import logging
import os
from io import BytesIO
from zipfile import ZipFile

import requests


LOG_FORMAT = '%(asctime)s - %(levelname)s: %(message)s'
LOG_DATEFORMAT = '%Y-%m-%d %H:%M:%S'
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT, datefmt=LOG_DATEFORMAT)
logger = logging.getLogger(__name__)

SCRAPED_DATA_PATH = './scraped_data'

TEXTS_URL = 'http://www.cs.toronto.edu/~atef/stories.zip'
ALIGNMENTS_URL = 'http://www.cs.toronto.edu/~atef/manual_alignments.zip'


def setup_environment():
    os.makedirs(SCRAPED_DATA_PATH, exist_ok=True)


def collect_texts():
    logger.info(f"Collecting texts from '{TEXTS_URL}'.")
    response = requests.get(TEXTS_URL)

    logger.info("Decompressing texts files.")
    files = ZipFile(BytesIO(response.content))
    files.extractall(SCRAPED_DATA_PATH)
    logger.info("Decompression finished successfully.")


def clean_texts():
    pass


def get_texts():
    collect_texts()
    clean_texts()


def collect_summaries():
    pass


def clean_summaries():
    pass


def get_summaries():
    collect_summaries()
    clean_summaries()


def collect_alignments():
    logger.info(f"Collecting texts from '{ALIGNMENTS_URL}'.")
    response = requests.get(ALIGNMENTS_URL)

    logger.info("Decompressing alignments files.")
    files = ZipFile(BytesIO(response.content))
    files.extractall(SCRAPED_DATA_PATH)
    logger.info("Decompression finished successfully.")


def clean_alignments():
    pass


def get_alignments():
    collect_alignments()
    clean_alignments()


def get_all():
    get_texts()
    get_summaries()
    get_alignments()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Data hunter process parser')
    parser.add_argument('-r', '--resource', choices=['texts', 'summaries', 'alignments', 'all'], default='all',
                        help="Resource to collect ['texts', 'summaries', 'alignments', 'all']. Defaults 'all'.")
    args = parser.parse_args()

    setup_environment()

    logging.info(f"Extracting {args.resource} resources.")
    globals().get(f'get_{args.resource}')()
