import configparser
from dataclasses import dataclass, fields


@dataclass
class Config:
    number_of_pages: int
    sleep_time: int
    base_url: str

    @classmethod
    def read_from_file(cls) -> Config:
        parser = configparser.ConfigParser()
        parser.read("config.ini")
        return cls(
            number_of_pages=parser.getint("PARAMETERS", "number_of_pages"),
            sleep_time=parser.getint("PARAMETERS", "sleep_time"),
            base_url=parser.get("PARAMETERS", "base_url"),
        )
