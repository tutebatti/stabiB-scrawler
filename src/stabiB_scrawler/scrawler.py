#!/usr/bin/python3

"""
Crawl and scrape XML URLs based on PPNs (Pica-Produktionsnummer) of manuscripts at StaBi Berlin
(c) 2023, Florian Jäckel
"""
from dataclasses import fields
from datetime import datetime
from logging import Logger

from src.stabiB_scrawler.handling.ms_maker import ManuscriptMaker
from src.stabiB_scrawler.model.config import Config
from src.stabiB_scrawler.model.manuscript import Manuscript
from src.stabiB_scrawler.handling.ppn_fetcher import PPNFetcher
from src.stabiB_scrawler.util import mk_logger


class Scrawler:
    config: Config
    logger: Logger
    ppns: list[str]
    mss: list[Manuscript]

    def __init__(self) -> None:
        self.config = Config.read_from_file()
        self.logger = mk_logger(self.__class__.__name__)

    def run(self):
        self._mk_ppns()
        self._extract_data_from_ppns()
        self._write_output()

    def _mk_ppns(self) -> None:
        self.ppns = PPNFetcher.fetch(self.config)

    def _extract_data_from_ppns(self) -> None:
        self.mss = ManuscriptMaker.mk_mss_from_ppn_list(self.ppns)

    def _write_output(self) -> None:
        if not self.mss:
            return

        with open(f"data/output_{datetime.isoformat(datetime.now())}.csv", "w") as file:
            file.write("\t".join(f.name for f in fields(Manuscript)) + "\n")
            file.write("\n".join(ms.to_csv_line() for ms in self.mss))
