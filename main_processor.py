import os
import argparse
import sys

from sawtooth_sdk.processor.core import TransactionProcessor
from sawtooth_sdk.processor.log import init_console_logging

from processor.handler import PnrdNetHandler


TOP_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, os.path.join(TOP_DIR, 'pnrdnet_addressing'))
sys.path.insert(0, os.path.join(TOP_DIR, 'processor'))
sys.path.insert(0, os.path.join(TOP_DIR, 'pnrdnet_protobuf'))


def parse_args(args):
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument(
        '-C', '--connect',
        default='tcp://localhost:4004',
        help='Endpoint for the validator connection')

    parser.add_argument(
        '-v', '--verbose',
        action='count',
        default=0,
        help='Increase output sent to stderr')

    return parser.parse_args(args)


def main(args=None):
    if args is None:
        args = sys.argv[1:]
    opts = parse_args(args)
    processor = None
    try:
        init_console_logging(verbose_level=opts.verbose)

        processor = TransactionProcessor(url=opts.connect)
        handler = PnrdNetHandler()
        processor.add_handler(handler)
        print("Startou!")
        processor.start()
    except KeyboardInterrupt:
        pass
    except Exception as err:  # pylint: disable=broad-except
        print("Error: {}".format(err))
    finally:
        if processor is not None:
            processor.stop()


if __name__ == '__main__':
    main()
