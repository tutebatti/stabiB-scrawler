from dataclasses import dataclass


@dataclass
class Manuscript:
    shelf_locator: str
    record_identifier: str
    purl: str
    date_as_str: str
    date_exact: str
    content: str

    def to_csv_line(self) -> str:
        return "\t".join([
            self.shelf_locator,
            self.record_identifier,
            self.purl,
            self.date_as_str,
            self.date_exact,
            self.content
        ])
