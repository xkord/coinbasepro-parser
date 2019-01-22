# -*- coding: utf-8 -*-

import logging
import argparse
from coinbasepro.coinbasepro import CoinbaseproScraper

__version__ = "0.0.1"
logger = logging.getLogger("LOG")


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='coinbasepro parser',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('-V', '--verbose', action='store_const',
                        const=logging.DEBUG, dest='verbosity',
                        help='Make a lot of noise')

    parser.add_argument('-v', '--version', action='version',
                        version=__version__,
                        help='Print version number and exit')

    parser.add_argument('-l', '--logfile', dest='logfile',
                        help='File for logs.',
                        default=None)

    return parser.parse_args()


def main():
    args = parse_arguments()

    # create the logging file handler
    if args.logfile is not None:
        fh = logging.FileHandler(args.logfile)
        logger.addHandler(fh)

    logger.addHandler(logging.StreamHandler())

    if args.verbosity:
        logger.setLevel(args.verbosity)
    else:
        logger.setLevel(logging.INFO)

    logger.debug('coinbasepro version: %s', __version__)

    with CoinbaseproScraper():
        pass


if __name__ == "__main__":
    main()
