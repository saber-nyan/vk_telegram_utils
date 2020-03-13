"""
Main file!
"""
import argparse
import logging

from vk_dumper import utils, vk

log = logging.getLogger('vk-dumper')


def main() -> None:
    log.info('Starting vk-dumper!')
    args = parse_args()

    if args.verbose:
        utils.init_logging(debug=True)
        log.debug('Logger reinitialized, debug logs enabled')

    result = vk.dump_messages(args.login, args.password)
    log.info('Got %d messages', len(result))


def parse_args() -> argparse.Namespace:
    arg_parser = argparse.ArgumentParser(
        prog='python -m vk_dumper',
        description='Utility for dumping VK messages.',
        epilog='desu~'
    )
    arg_parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='show additional debug logs',
        dest='verbose'
    )
    arg_parser.add_argument(
        'login',
        action='store',
        type=str,
        help='VK.com phone number/email',
        metavar='login',
    )
    arg_parser.add_argument(
        'password',
        action='store',
        type=str,
        help='VK.com password',
        metavar='password',
    )
    return arg_parser.parse_args()


if __name__ == '__main__':
    utils.init_logging(debug=False)
    main()
