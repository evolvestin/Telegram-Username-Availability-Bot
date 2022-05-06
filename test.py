import hashlib
import logging
import secrets

from aiogram import Bot, Dispatcher, executor
from aiogram.types import InlineQuery, InputTextMessageContent, InlineQueryResultArticle
from aiogram import types

# API_TOKEN = '1356734882:AAFWCJMdhLWAqF4A_BYQOYnq7I9ZkqCJnNE'
API_TOKEN = '429683355:AAE2isaUNIbpcQ9TAjwzzcJYryA6oK8Ywow'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.inline_handler()
async def inline_echos(inline_query: InlineQuery):
    print(inline_query)
    # id affects both preview and content,
    # so it has to be unique for each result
    # (Unique identifier for this result, 1-64 Bytes)
    # you can set your unique id's
    # but for example i'll generate it based on text because I know, that
    # only text will be passed in this example
    text = inline_query.query
    print(text)
    if len(text) > 0:
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(types.InlineKeyboardButton('/g_deposit', callback_data='deposit'))
        item = InlineQueryResultArticle(id=secrets.token_hex(20), title=f'Result {text}',
                                        input_message_content=InputTextMessageContent(text),
                                        url='https://telegram.me/evolvemintbot?start=1',
                                        hide_url=False)
        item2 = InlineQueryResultArticle(id=secrets.token_hex(20), title='kl',
                                         input_message_content=InputTextMessageContent(text),
                                         url='https://telegram.me/evolvemintbot?start=1',
                                         hide_url=True)

        await bot.answer_inline_query(inline_query.id, switch_pm_text='/hello', switch_pm_parameter='lekflkl', results=[item, item2], cache_time=1)
        # Only 0-9, a-z, and underscores allowed.|This link is invalid|Sorry, this link is too short
        # Sorry, this link is already occupied|This link is available
    else:
        await bot.answer_inline_query(inline_query.id, results=[], cache_time=1)


#@dp.inline_handler()
async def inline_echo(inline_query: InlineQuery):
    print(inline_query)
    # id affects both preview and content,
    # so it has to be unique for each result
    # (Unique identifier for this result, 1-64 Bytes)
    # you can set your unique id's
    # but for example i'll generate it based on text because I know, that
    # only text will be passed in this example
    print(inline_query.query)
    text = inline_query.query or 'echo'
    input_content = InputTextMessageContent(text)
    result_id: str = hashlib.md5(text.encode()).hexdigest()
    item = InlineQueryResultArticle(
        id=result_id,
        title=f'Result {text!r}',
        input_message_content=input_content,
    )
    # don't forget to set cache_time=1 for testing (default is 300s or 5m)
    await bot.answer_inline_query(inline_query.id, results=[item], cache_time=1)


if __name__ == '__main__':
    executor.start_polling(dp)
