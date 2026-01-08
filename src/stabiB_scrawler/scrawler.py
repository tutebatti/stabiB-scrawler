#!/usr/bin/python3

'''
Crawl and scrape xml URLs based on PPNs (Pica-Produktionsnummer) of manuscripts at StaBi Berlin
(c) 2023, Florian Jäckel
'''
import logging
import time
from datetime import datetime
from logging import Logger

import tqdm
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from src.stabiB_scrawler.config import Config

METS_BASE_URL = "https://content.staatsbibliothek-berlin.de/dc/"
METS_EXTENSION = ".mets.xml"


class Scrawler:
    config: Config
    logger: Logger
    driver: WebDriver
    ppns: list[str]

    def __init__(self) -> None:
        self.config = Config.read_from_file()
        self._mk_logger()
        self._mk_chrome_driver()

    def _mk_logger(self) -> None:
        self.logger = logging.getLogger("StabiScrawler")
        self.logger.setLevel(logging.INFO)

        ch = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        ch.setFormatter(formatter)

        self.logger.addHandler(ch)

    def _mk_chrome_driver(self) -> None:
        options = Options()
        options.add_argument("--headless=new")

        self.driver = webdriver.Chrome(options=options)

    def run(self):
        self._mk_ppns()
        self._write_output()
        self.driver.close()

    def _mk_ppns(self) -> None:
        self.ppns = []

        for page in range(1, self.config.number_of_pages + 1):
            page_url = f"{self.config.base_url}{page}"
            self.logger.info(f"Scraping page {page}: {page_url}")
            self.driver.get(page_url)

            time.sleep(self.config.sleep_time)

            list_element = self.driver.find_element(by=By.CLASS_NAME, value="search-result-list")

            list_items = list_element.find_elements(by=By.XPATH, value="./a")
            if not list_items:
                self.logger.info(f"Found no manuscripts on this page")
                continue

            self.logger.info(f"Found {len(list_items)} manuscripts on this page")

            for i in tqdm.tqdm(list_items):
                ppn = i.get_attribute("href").lstrip("/werkansicht?PPN=").split("&")[0]
                self.logger.debug(f"{ppn=}")
                self.ppns.append(ppn)

    def _write_output(self) -> None:
        if not self.ppns:
            return

        with open(f"output_{datetime.isoformat(datetime.now())}", "w") as file:
            file.write("\n".join(f"{METS_BASE_URL}{ppn}{METS_EXTENSION}" for ppn in self.ppns))

