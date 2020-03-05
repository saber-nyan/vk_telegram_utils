"""
VkOpt dump parsers.
"""
import logging
from typing import TextIO, List, Optional, Dict

# noinspection PyProtectedMember
from bs4 import BeautifulSoup, Tag

from vkopt_telegram_parser import utils

log = logging.getLogger('vkopt-telegram-parser.vk')


def parse_file(file: TextIO, user_ids_raw: Optional[List[str]]) -> List[Dict[str, str]]:
    user_ids: Optional[List[str]] = None
    if user_ids_raw:
        user_ids = list(map(lambda e: f'@{e}', user_ids_raw))
    log.info('Processing VkOpt file "%s", filtering users "%s"...',
             file.name, user_ids_raw)
    soup = BeautifulSoup(file.read(), features='lxml')

    result = []
    message: Tag
    for message in soup.find_all('div', class_='msg_item'):
        sender_id: str = message.find_next('a', attrs={
            'target': '_blank'
        }).text.strip()
        if user_ids and sender_id not in user_ids:
            log.debug('Skipping not selected id "%s"', sender_id)
            continue
        message: str = message.find_next('div', class_='msg_body').text.strip()
        log.debug('Got message "%s" from "%s"', message, sender_id)
        if utils.str_none_or_empty(message):
            log.debug('Skipping empty message (attachment?)')
        result.append({
            'from': sender_id[1:],
            'message': message,
        })
    log.info('...done')
    return result
