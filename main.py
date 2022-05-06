import os
import re
import asyncio
import objects
import secrets
import requests
import concurrent.futures
from aiogram import types
from bs4 import BeautifulSoup
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from aiogram.types import InlineQueryResultArticle as Article
from aiogram.types import InlineQuery, InputTextMessageContent
# ========================================================================================================
stamp1 = objects.time_now()
Auth = objects.AuthCentre(ID_DEV=-1001312302092,
                          TOKEN=os.environ['TOKEN'],
                          DEV_TOKEN=os.environ['DEV_TOKEN'])
bot, idMe, t_me, dispatcher = Auth.async_bot, 396978030, 'https://t.me/', Dispatcher(Auth.async_bot)
# ========================================================================================================
if os.environ.get('local') is None:
    Auth.dev.start(stamp1)


def rand():
    return secrets.token_hex(20)


@dispatcher.message_handler()
async def repeat_all_messages(message: types.Message):
    try:
        if message['chat']['id'] == idMe:
            if message['text'].startswith('/log'):
                doc = open('log.txt', 'rb')
                await bot.send_document(message['chat']['id'], doc)
                doc.close()
    except IndexError and Exception:
        await Auth.dev.async_except()


async def line(query):
    title = f't.me/{query} '
    content = InputTextMessageContent(query)
    if 5 <= len(query) <= 32:
        try:
            response = requests.get(t_me + query)
        except IndexError and Exception:
            await asyncio.sleep(0.01)
            try:
                response = requests.get(t_me + query)
            except IndexError and Exception:
                response = None
        if response:
            soup = BeautifulSoup(response.text, 'html.parser')
            is_username_exist = soup.find('a', class_='tgme_action_button_new')
            if is_username_exist is None:
                description = 'This link is available'
                title += '✅'
            else:
                title += '🚫'
                description = 'Sorry, this link is already occupied'
        else:
            title += '🚫'
            description = 'Something’s wrong, wait a bit and try again'
    else:
        title += '🚫'
        description = 'Sorry, this link is too '
        if len(query) < 5:
            description += 'short'
        else:
            description += 'long'
    return Article(id=rand(), title=title, input_message_content=content, description=description)


@dispatcher.inline_handler()
async def inline_echos(inline_query: InlineQuery):
    results = []
    query = inline_query.query
    if 1 <= len(query) <= 32 and re.search('[^a-zA-Z0-9_]', query) is None and re.sub('[0-9]', '', query) \
            and re.search('__', query) is None and query[:1].isdigit() is False:
        queries = {}
        for key in [query + postfix for postfix in ['', 'bot', '_bot']]:
            queries[key] = {
                'title': f't.me/{key} ',
                'desc': None}
            if 5 <= len(key) <= 32:
                queries[key]['desc'] = t_me + key
            else:
                queries[key]['title'] += '🚫'
                queries[key]['desc'] = 'Sorry, this link is too '
                if len(query) < 5:
                    queries[key]['desc'] += 'short'
                else:
                    queries[key]['desc'] += 'long'

        futures = [queries[key]['desc'] for key in queries if queries[key]['desc'].startswith(t_me)]
        if len(futures) > 0:
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as future_executor:
                futures = [future_executor.submit(requests.get, future) for future in futures]
                for future in concurrent.futures.as_completed(futures):
                    soup = BeautifulSoup(future.result().content, 'html.parser')
                    get_key = soup.find('meta', {'name': 'twitter:app:url:googleplay'})
                    is_username_exist = soup.find('a', class_='tgme_action_button_new')
                    if soup.find('meta', {'name': 'twitter:app:url:googleplay'}):
                        key = get_key.get('content')
                        if key:
                            key = re.sub(t_me, '', key)
                            if is_username_exist is None:
                                queries[key]['title'] += '✅'
                                queries[key]['desc'] = 'This link is available'
                            else:
                                queries[key]['title'] += '🚫'
                                queries[key]['desc'] = 'Sorry, this link is already occupied'
        for key in queries:
            title = queries[key]['title']
            description = queries[key]['desc']
            content = InputTextMessageContent('t.me/' + key)
            if description.startswith(t_me):
                title += '🚫'
                description = 'Something’s wrong, wait a bit and try again'
            results.append(Article(id=rand(), title=title, input_message_content=content, description=description))
    else:
        description = None
        if len(query) == 0:
            title = 'You can use a-z, 0-9 and underscores.'
            description = 'Minimum length is 2 characters.'
        elif re.sub('[a-zA-Z0-9_]', '', query):
            title = 'Only 0-9, a-z, and underscores allowed.'
        elif re.search('[^0-9]', query) is None or re.search('__', query) or query[:1].isdigit():
            title = 'This link is invalid'
        else:
            title = 'Sorry, this link is too long'
        content = InputTextMessageContent(t_me + re.sub('[^a-zA-Z0-9_]', '', query))
        results.append(Article(id=rand(), title=title, input_message_content=content, description=description))
    await bot.answer_inline_query(inline_query.id, results=results)


if __name__ == '__main__':
    executor.start_polling(dispatcher)
