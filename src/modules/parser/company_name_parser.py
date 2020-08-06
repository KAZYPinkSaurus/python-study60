import re
from lxml import etree


class CompanyNameParser:
    title = "company_name"

    def run(self, tree: etree._Element):
        etree_element = tree.find(
            "jpcrp_cor:CompanyNameCoverPage", namespaces=tree.nsmap
        )

        if etree_element is None:
            return self.title, "Unknown"

        text = re.sub(r"\s", "", etree_element.text)

        return self.title, text
