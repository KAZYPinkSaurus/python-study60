import os
import re
import logging
import logzero
from glob import glob
from lxml import etree
from logzero import logger
from typing import Optional
from collections import defaultdict
from src.modules.parser.company_name_parser import CompanyNameParser
from src.modules.parser.business_issues_parser import BusinessIssuesParser

logzero.loglevel(logging.INFO)

HEADERS = (
    "company_name",
    "business_issues",
)

PARSERS = (CompanyNameParser(), BusinessIssuesParser())


class Parser:
    def __init__(self, input_dir, output_dir):
        self.input_dir = input_dir
        self.target_tsv = os.path.join(output_dir, "parsed.tsv")

    def __repr__(self):
        return f"\ninput_dir:{self.input_dir}\ntarget_tsv:{self.target_tsv}"

    def run(self):
        input_files = glob(os.path.join(self.input_dir, "*.xbrl"))

        # パースして結果を保存する
        with open(self.target_tsv, "w", encoding="utf-8") as f:
            f.write("\t".join(HEADERS) + "\n")
            for file_name in input_files:
                parsed_dict = self.parse(file_name)
                if parsed_dict is None:
                    continue
                f.write("\t".join([parsed_dict[header] for header in HEADERS]) + "\n")

    def parse(self, file_name: str) -> Optional[defaultdict]:
        tree = etree.parse(file_name).getroot()

        if tree is None:
            return None

        parsed_disclosure = defaultdict(lambda: "Unknown")

        for parser in PARSERS:
            title, content = parser.run(tree)
            parsed_disclosure[title] = content
        return parsed_disclosure
