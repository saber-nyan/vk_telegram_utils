"""
Main file!
"""
import argparse
import itertools
import logging
import pickle
import string
import sys
from typing import TextIO, List, BinaryIO, Optional

import ujson

from vkopt_telegram_parser import utils, vk, tg

log = logging.getLogger('vkopt-telegram-parser')


def main() -> None:
    log.info('Starting vkopt-telegram-parser!')
    args = parse_args()

    # Output variants:
    json_file: Optional[TextIO] = args.json_file[0] if args.json_file else None
    pickle_file: Optional[BinaryIO] = args.pickle_file[0] if args.pickle_file else None
    text_file: Optional[TextIO] = args.text_file[0] if args.text_file else None
    if not (json_file or pickle_file or text_file):
        log.critical('No dump save method selected, use -j/-p/-x parameters')
        sys.exit(1)

    if args.verbose:
        utils.init_logging(debug=True)
        log.debug('Logger reinitialized, debug logs enabled')

    vk_results_list = []
    vk_file: List[TextIO]  # WTF?!
    for vk_file in args.vk_files or []:
        vk_results_list.append(
            vk.parse_file(vk_file[0], args.vk_ids[0] if args.vk_ids else None)
        )
        vk_file[0].close()

    tg_results_list = []
    tg_file: List[TextIO]
    for tg_file in args.tg_files or []:
        tg_results_list.append(
            tg.parse_file(tg_file[0], args.tg_ids[0] if args.tg_ids else None)
        )
        tg_file[0].close()

    tg_results_list.extend(vk_results_list)
    result = list(itertools.chain.from_iterable(tg_results_list))
    log.info('Got %d messages', len(result))

    if json_file:
        log.info('Saving results into JSON file "%s"...', json_file.name)
        ujson.dump(result, json_file, ensure_ascii=False, escape_forward_slashes=False)
        log.info('...done')

    if pickle_file:
        log.info('Saving results into Pickle file "%s"...', pickle_file.name)
        pickle.dump(
            result, pickle_file,
            protocol=pickle.HIGHEST_PROTOCOL, fix_imports=False
        )
        log.info('...done')

    if text_file:
        log.info('Saving results into plain text file (with sanitizing) "%s"...', text_file.name)
        sanitized = ''
        for entry in result:
            words = entry['message'] \
                .lower() \
                .split()
            bad_chars = string.punctuation + string.ascii_lowercase + string.digits
            translator = str.maketrans(bad_chars, ' ' * len(bad_chars))
            stripped = [word.translate(translator) for word in words]
            sanitized += ' '.join(stripped) + ' '

        text_file.write(
            ' '.join(sanitized.strip().split())
        )
        log.info('...done')

    log.info('Done!')


def parse_args() -> argparse.Namespace:
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
            'rt', errors='surrogateescape'
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
        help='select usernames to extract, without @ (VkOpt)',
        metavar='username',
        dest='vk_ids'
    )
    arg_parser.add_argument(
        '--telegram-file', '-t',
        action='append',
        nargs=1,
        type=argparse.FileType(
            'rt', errors='surrogateescape'
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
    arg_parser.add_argument(
        '--out-json', '-j',
        action='store',
        nargs=1,
        type=argparse.FileType(
            'xt', encoding='utf-8', errors='surrogateescape'
        ),
        help='choose a path to dump results as JSON',
        metavar='/path/to/dump.json',
        dest='json_file'
    )
    arg_parser.add_argument(
        '--out-pickle', '-p',
        action='store',
        nargs=1,
        type=argparse.FileType('xb'),
        help='choose a path to dump results as Pickle',
        metavar='/path/to/dump.pkl',
        dest='pickle_file'
    )
    arg_parser.add_argument(
        '--out-txt', '-x',
        action='store',
        nargs=1,
        type=argparse.FileType(
            'xt', encoding='utf-8', errors='surrogateescape'
        ),
        help='choose a path to dump results as plain text',
        metavar='/path/to/dump.txt',
        dest='text_file'
    )
    return arg_parser.parse_args()


if __name__ == '__main__':
    utils.init_logging(debug=False)
    main()
