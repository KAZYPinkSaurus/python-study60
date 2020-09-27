import os
import re
import csv
import logging
import logzero
import wordcloud
from logzero import logger
from dataclasses import dataclass
from collections import Counter
from src.modules.mydataclass.morph import Morph
from src.modules.mydataclass.xbrl import XBRL


logzero.loglevel(logging.INFO)


class WordClouder:
    srop_words_re = re.compile(r"こと|ため|課題|今後|当社グループ|よう|\*")
    font_path = os.path.join(os.getcwd(), "fonts/NotoSansCJKjp-Light.otf")
    word_class_map = {"adjective": "形容詞", "noun": "名詞"}

    def __init__(self, input_tsv, output_dir):
        self.input_tsv = input_tsv
        self.target_tsv = os.path.join(output_dir, "wordcloud.png")

    def __repr__(self):
        return f"\ninput_tsv:{self.input_tsv}\ntarget_tsv:{self.target_tsv}"

    def run(self, word_class):
        xbrls = self.read_xbrl()
        logger.info("\n" + "\n".join(map(str, xbrls)))
        words = self.extract_words(word_class, xbrls)
        logger.info(Counter(words.split()).most_common()[:10])
        if words == "":
            return
        wordc = wordcloud.WordCloud(
            font_path=self.font_path, background_color="white", width=800, height=600
        ).generate(words)

        # 画像ファイルとして保存
        wordc.to_file(self.target_tsv)

    def extract_words(self, word_class, xbrls):
        words = ""
        for xbrl in xbrls:
            nouns = ""
            for morph in xbrl.bussiness_issues_morphs:
                if word_class in self.word_class_map and morph.pos in (
                    self.word_class_map[word_class]
                ):
                    nouns += morph.base
                    continue

                if nouns == "":
                    continue
                words += f"{nouns} "
                nouns = ""
        return self.srop_words_re.sub("", words)

    def read_xbrl(self):
        xbrls = []
        with open(self.input_tsv) as f:
            reader = csv.DictReader(f, delimiter="\t")
            for row in reader:
                xbrls.append(XBRL(row["company_name"], row["business_issues"]))
        return xbrls

