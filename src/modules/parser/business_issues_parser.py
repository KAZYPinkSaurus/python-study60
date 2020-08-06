import re
from lxml import etree


class BusinessIssuesParser:
    title = "business_issues"
    block_title_re = re.compile(r"【\s*?経営方針.?経営環境(及|およ)び対処すべき課題等\s*?】")
    tag_re = re.compile(r"&lt;.*?&gt;|<.*?>")

    def run(self, tree: etree._Element):
        """
        【経営方針、経営環境及び対処すべき課題等】のブロックを抽出する.
        """

        etree_element = tree.find(
            "jpcrp_cor:BusinessPolicyBusinessEnvironmentIssuesToAddressEtcTextBlock",
            namespaces=tree.nsmap,
        )

        if (
            etree_element is None
            or self.block_title_re.search(etree_element.text) is None
        ):
            return self.title, "Unknown"

        text = "".join(self.tag_re.sub("", etree_element.text).split())

        return self.title, self.block_title_re.sub("", text)

