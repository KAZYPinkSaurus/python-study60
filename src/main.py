import os
import click
import logging
import logzero
from logzero import logger
from src.modules.parser.parser import Parser
from src.modules.wordcloud import WordClouder

logzero.loglevel(logging.INFO)


x_help = "Please set directory which contains xbrl files."


@click.command()
@click.option("-x", "--xbrl_dir", "xbrl_dir", required=True, help=x_help)
@click.option("-w", "--word_class", "word_class", default="noun")
def main(xbrl_dir,word_class):
    # file paths
    base_path = os.getcwd()
    os.makedirs(os.getcwd() + "/parsed", exist_ok=True)
    os.makedirs(os.getcwd() + "/wordcloud", exist_ok=True)
    xbrl_dir = (
        os.path.join(base_path, xbrl_dir) if base_path not in xbrl_dir else xbrl_dir
    )
    parsed_dir = os.path.join(base_path, "parsed")
    wordclouded_dir = os.path.join(base_path, "wordcloud")

    # Parse
    parser = Parser(xbrl_dir, parsed_dir)
    logger.info(parser)
    parser.run()

    # Word Cloud
    wordcloud = WordClouder(parser.target_tsv, wordclouded_dir)
    logger.info(wordcloud)
    wordcloud.run(word_class)


if __name__ == "__main__":
    main()
