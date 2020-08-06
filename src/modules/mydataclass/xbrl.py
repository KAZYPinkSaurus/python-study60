import MeCab
from dataclasses import dataclass
from src.modules.mydataclass.morph import Morph


@dataclass(frozen=True)
class XBRL:
    name: str
    bussiness_issues: str

    def __repr__(self):
        return f"company: {self.name}"

    @property
    def bussiness_issues_morphs(self):
        mecab = MeCab.Tagger()
        node = mecab.parseToNode(self.bussiness_issues)
        morphs = list()
        node = node.next
        while node:
            if node.feature.split(",")[0] == "BOS/EOS":
                node = node.next
                continue
            surface = node.surface
            base = node.feature.split(",")[-3]
            pos = node.feature.split(",")[0]
            pos1 = node.feature.split(",")[1]
            morphs.append(Morph(surface, base, pos, pos1))
            node = node.next
        return morphs
