import logging
import time
from logging import Logger

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from src.stabiB_scrawler.model.config import Config
from src.stabiB_scrawler.util import mk_logger


class PPNFetcher:
    config: Config
    logger: Logger
    driver: WebDriver
    ppns: list[str]

    def __init__(self, config: Config) -> None:
        self.config = config
        self.logger = mk_logger(self.__class__.__name__)
        self._mk_chrome_driver()

    def _mk_chrome_driver(self) -> None:
        options = Options()
        options.add_argument("--headless=new")

        self.driver = webdriver.Chrome(options=options)

    def _fetch_ppns(self) -> None:
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

            for i in list_items:
                ppn = i.get_attribute("href").split("?")[1].lstrip("PPN=").split("&")[0]
                self.logger.debug(f"{ppn=}")
                self.ppns.append(ppn)

        self.driver.close()

    @classmethod
    def fetch(cls, config) -> list[str]:
        fetcher = cls(config)
        fetcher._fetch_ppns()
        return fetcher.ppns
