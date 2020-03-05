"""
Telegram Desktop dump parsers.
"""
import logging
from typing import TextIO, Optional, List, Dict

# noinspection PyProtectedMember
from bs4 import BeautifulSoup, Tag

log = logging.getLogger('vkopt-telegram-parser.tg')


def parse_file(file: TextIO, user_ids: Optional[List[str]]) -> List[Dict[str, str]]:
    log.info('Processing Telegram file "%s", filtering users "%s"...',
             file.name, user_ids)
    soup = BeautifulSoup(file.read(), features='lxml')

    result = []
    container: Tag
    last_sender_username: Optional[str] = None
    for container in soup.find_all('div', class_='message default clearfix'):
        body: Tag = container.find_next('div', class_='body')
        if body.find('div', class_='forwarded'):
            log.debug('Seems like forwarded/attachment message, skipping')
            continue
        sender_username_tag: Tag = body.find_next('div', class_='from_name')
        if not sender_username_tag:
            sender_username = last_sender_username
        else:
            sender_username = sender_username_tag.text.strip()
            last_sender_username = sender_username
        message: str = body.find_next('div', class_='text').text.strip()
        log.debug('Got message "%s" from "%s"', message, sender_username)
        result.append({
            'from': sender_username,
            'message': message,
        })
    log.info('...done')
    return result
