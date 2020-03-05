"""
Main file!
"""
import argparse
import logging

from vkopt_telegram_parser import utils, vk, tg

log = logging.getLogger('vkopt-telegram-parser')


def main():
    log.info('Starting vkopt-telegram-parser!')
    arg_parser = argparse.ArgumentParser(
        prog='python -m vkopt_telegram_parser',
        description='Parses VkOpt and Telegram dialog dumps.',
        epilog='desu~'
    )
    arg_parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='show additional debug logs',
        dest='verbose'
    )
    arg_parser.add_argument(
        '--vkopt-file', '-i',
        action='append',
        nargs=1,
        type=argparse.FileType(
            'rt', bufsize=8192,
            errors='surrogateescape'
        ),
        help='choose VkOpt dump files',
        metavar='VKOPT.html',
        dest='vk_files'
    )
    arg_parser.add_argument(
        '--vkopt-id', '-d',
        action='append',
        nargs=1,
        type=str,
        help='select usernames to extract without @ (VkOpt)',
        metavar='username',
        dest='vk_ids'
    )
    arg_parser.add_argument(
        '--telegram-file', '-t',
        action='append',
        nargs=1,
        type=argparse.FileType(
            'rt', bufsize=8192,
            errors='surrogateescape'
        ),
        help='choose Telegram dump files',
        metavar='TG.html',
        dest='tg_files'
    )
    arg_parser.add_argument(
        '--telegram-id', '-m',
        action='append',
        nargs=1,
        type=str,
        help='select names to extract (Telegram; do not confuse with a username!)',
        metavar='name',
        dest='tg_ids'
    )
    args = arg_parser.parse_args()
    if args.verbose:
        utils.init_logging(debug=True)
        log.debug('Logger reinitialized, debug logs enabled')

    vk_results_list = []
    for vk_file in args.vk_files or []:
        vk_results_list.append(
            vk.parse_file(vk_file[0], args.vk_ids[0] if args.vk_ids else None)
        )

    tg_results_list = []
    for tg_file in args.tg_files or []:
        tg_results_list.append(
            tg.parse_file(tg_file[0], args.tg_ids[0] if args.tg_ids else None)
        )

    log.info('Done!')


if __name__ == '__main__':
    utils.init_logging(debug=False)
    main()
