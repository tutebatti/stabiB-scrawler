from logging import Logger

import lxml.etree as ET
import requests
import tqdm

from src.stabiB_scrawler.model.manuscript import Manuscript
from src.stabiB_scrawler.util import mk_logger

METS_BASE_URL = "https://content.staatsbibliothek-berlin.de/dc/"
METS_EXTENSION = ".mets.xml"

XPATHS = {
    "shelf_locator": "mets:dmdSec[1]//mods:shelfLocator/text()",
    "record_identifier": "mets:dmdSec[1]//mods:recordInfo/mods:recordIdentifier[@source='gbv-ppn']/text()",
    "purl": "mets:dmdSec[1]//mods:identifier[@type='purl']/text()",
    "date_as_str": "mets:dmdSec[1]//mods:dateCreated[@qualifier='approximate']/text()",
    "date_exact": "mets:dmdSec[1]//mods:dateCreated[@encoding='iso8601']/text()",
    "content": "mets:dmdSec//mods:titleInfo/mods:title/text()",
}
NAMESPACES = {
    'mets': 'http://www.loc.gov/METS/',
    'mods': 'http://www.loc.gov/mods/v3'
}


class ManuscriptMaker:
    logger: Logger
    raw_data: dict[str, str]

    def __init__(self) -> None:
        self.logger = mk_logger(self.__class__.__name__)

    @classmethod
    def mk_mss_from_ppn_list(cls, ppn_list: list[str]) -> list[Manuscript]:
        result = []

        for ppn in tqdm.tqdm(ppn_list):
            ms = cls.mk_manuscript_from_ppn(ppn)
            result.append(ms)

        return result

    @classmethod
    def mk_manuscript_from_ppn(cls, ppn: str) -> Manuscript:
        maker = cls()
        xml = maker._fetch_xml_from_ppn(ppn)
        return maker._mk_manuscript_from_xml(xml)

    def _fetch_xml_from_ppn(self, ppn: str) -> str:
        full_url = f"{METS_BASE_URL}{ppn}{METS_EXTENSION}"

        self.logger.debug(f"Retrieving data for {ppn} at {full_url}")

        response = requests.get(full_url)
        response.raise_for_status()

        return response.content

    def _mk_manuscript_from_xml(self, xml_content: str) -> Manuscript:
        root = ET.fromstring(xml_content)
        self.raw_data = {k: root.xpath(v, namespaces=NAMESPACES) for k, v in XPATHS.items()}

        self._process_raw_data()

        return Manuscript(**self.raw_data)

    def _process_raw_data(self) -> None:
        for x in ["shelf_locator", "record_identifier", "purl", "date_as_str"]:
            self.raw_data[x] = self.raw_data[x][0] if self.raw_data[x] else ""
        self.raw_data["date_exact"] = "-".join(self.raw_data["date_exact"])
        self.raw_data["content"] = "; ".join(
            i
            for i in self.raw_data["content"]
            if i != "Orientalische Handschriften digital"
        )
