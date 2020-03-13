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


def dump_messages(login: str, password: str) -> List[
    Dict[str, Union[str, int, Dict[str, Union[str, int]]]]
]:
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

    results: List[
        Dict[str, Union[str, int, Dict[str, Union[str, int]]]]
    ] = []
    log.debug('Getting dialogs...')
    for dialog in tools.get_all_iter(
            'messages.getConversations',
            max_count=200,
    ):
        peer_id: int = dialog['conversation']['peer']['id']
        user_info = get_user_by_id_cached(vk, peer_id)
        if not user_info:
            log.debug('Skipping...')
            continue
        domain: str = user_info['domain']
        first_name: str = user_info['first_name']
        last_name: str = user_info['last_name']
        log.info('Processing dialog w/ @%s (%s %s)', domain, last_name, first_name)

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
                domain = sender_user['domain']
                first_name = sender_user['first_name']
                last_name = sender_user['last_name']
            date: int = message['date']
            body: str = message['text']

            log.debug('Saving message "%s" at %d from @%s (%s %s)',
                      body, date, domain, last_name, first_name)
            message['sender'] = sender_user
            results.append(message)
    return results
