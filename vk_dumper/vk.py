import logging
import os
from typing import Dict, Union, List, Optional

import vk_api

from vk_dumper import utils

log = logging.getLogger('vk-dumper.vk')

user_cache: Dict[int, Optional[Dict[str, Union[str, int]]]] = {}


def get_user_by_id_cached(vk: vk_api.vk_api.VkApiMethod,
                          peer_id: int) -> Optional[Dict[str, Union[str, int]]]:
    if peer_id in user_cache:
        log.debug('Cache hit')
        return user_cache[peer_id]
    else:
        log.debug('Cache miss')
        try:
            user_info: Dict[str, Union[str, int]] = vk.users.get(
                user_ids=peer_id, fields='domain'
            )[0]
        except vk_api.ApiError:
            log.debug('Cache fail', exc_info=True)
            user_cache[peer_id] = None
            return None
        user_cache[peer_id] = user_info
        return user_info


def dump_messages(
        login: str, password: str,
        message_count: Optional[int],
        user_ids: Optional[List[str]]
) -> List[Dict[str, Union[str, int, Dict[str, Union[str, int]]]]]:
    log.info('Logging in as %s', login)
    session = vk_api.VkApi(
        login, password,
        config_filename=os.path.join(utils.BASE_DIR, 'vk_config.json'),
        api_version='5.103',
        scope=vk_api.VkUserPermissions.MESSAGES | vk_api.VkUserPermissions.OFFLINE,
        app_id=2685278
    )
    session.auth()
    vk = session.get_api()
    tools = vk_api.VkTools(vk)
    log.info('Authentication succeed')

    current_messages = 0
    results: List[
        Dict[str, Union[str, int, Dict[str, Union[str, int]]]]
    ] = []
    log.debug('Getting dialogs...')
    # noinspection PyBroadException
    try:
        for dialog in tools.get_all_iter(
                'messages.getConversations',
                max_count=200,
        ):
            peer_id: int = dialog['conversation']['peer']['id']
            user_info = get_user_by_id_cached(vk, peer_id)
            if user_info:
                domain: Optional[str] = user_info.get('domain')
                first_name: Optional[str] = user_info.get('first_name')
                last_name: Optional[str] = user_info.get('last_name')
                log.info('Processing dialog w/ @%s (%s %s), total msgs: %d',
                         domain, last_name, first_name, current_messages)
            else:
                log.info('Processing dialog #%d, total msgs: %d',
                         peer_id, current_messages)

            message: Dict[str, Union[str, int, Dict[str, Union[str, int]]]]
            for message in tools.get_all_iter(
                    'messages.getHistory', max_count=200,
                    values={
                        'peer_id': peer_id,
                        'rev': 1,
                    }
            ):
                sender_user = get_user_by_id_cached(vk, message['from_id'])
                domain: Optional[str] = None
                first_name: Optional[str] = None
                last_name: Optional[str] = None
                if sender_user:
                    domain = sender_user.get('domain')
                    first_name = sender_user.get('first_name')
                    last_name = sender_user.get('last_name')
                date: Optional[int] = message.get('date')
                body: Optional[str] = message.get('text')

                if user_ids and domain not in user_ids:
                    log.debug('Skipping not selected id "%s"', domain)
                    continue

                if utils.str_none_or_empty(body):
                    log.debug('Skipping empty message (attachment?)')
                    continue

                log.debug('Saving message "%s" at %d from @%s (%s %s)',
                          body, date, domain, last_name, first_name)
                message['sender'] = sender_user
                results.append(message)
                current_messages += 1
                if message_count and current_messages >= message_count:
                    log.info('Got %d messages out of %d, stopping', current_messages, message_count)
                    return results
    except Exception:
        log.critical('Got unexpected exception, saving and exiting!', exc_info=True)
        return results
    return results
