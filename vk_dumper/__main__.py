"""
Main file!
"""
import argparse
import logging
import pickle
import string
import sys
from typing import Optional, TextIO, BinaryIO

import ujson

from vk_dumper import utils, vk

log = logging.getLogger('vk-dumper')


def main() -> None:
    log.info('Starting vk-dumper!')
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

    result = vk.dump_messages(
        args.login, args.password,
        args.message_count[0] if args.message_count else None,
        args.vk_ids[0] if args.vk_ids else None
    )
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
            words = entry['text'] \
                .lower() \
                .split()
            bad_chars = string.punctuation + string.ascii_lowercase + string.digits
            translator = str.maketrans(bad_chars, ' ' * len(bad_chars))
            stripped = [word.translate(translator) for word in words]
            sanitized += ' '.join(stripped) + ' '
            if args.markovify:
                sanitized += '\n'

        if args.markovify:
            text_file.write(sanitized)
        else:
            text_file.write(
                ' '.join(sanitized.strip().split())
            )
        log.info('...done')


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
        '--message-count', '-c',
        action='store',
        nargs=1,
        type=int,
        help='maximum messages count to extract',
        metavar='count',
        dest='message_count'
    )
    arg_parser.add_argument(
        '--vk-id', '-d',
        action='append',
        nargs=1,
        type=str,
        help='select usernames to extract, without @',
        metavar='username',
        dest='vk_ids'
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
    arg_parser.add_argument(
        '--markov', '-m',
        action='store_true',
        help='store plaintext with line break after each message for markovify',
        dest='markovify'
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
