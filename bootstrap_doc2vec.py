from argparse import ArgumentParser

import sys

import logging

from data.options import Options
from processors.doc2vec_processor import Doc2VecProcessor

logging.basicConfig(
    level=logging.INFO,
    stream=sys.stdout,
    format='[%(asctime)s]: %(name)s : %(levelname)s : %(message)s'
)
log = logging.getLogger(__name__)


def main(argv):
    options = parse_args(argv)
    processor = Doc2VecProcessor(options)
    processor.process()


def parse_args(argv):
    parser = ArgumentParser(prog="wassa-task")
    parser.add_argument('--input_file_path', metavar='Input File Path',
                        type=str, required=True)

    return parser.parse_args(argv, namespace=Options())


if __name__ == "__main__":
    main(sys.argv[1:])
