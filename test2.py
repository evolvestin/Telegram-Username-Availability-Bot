import os
import re
import asyncio
import gspread
import objects
import secrets
import requests
from time import sleep
from copy import deepcopy
import concurrent.futures
from aiogram import types
from bs4 import BeautifulSoup
from datetime import datetime
from aiogram.utils import executor
from objects import printer
from aiogram.dispatcher import Dispatcher
from requests_futures.sessions import FuturesSession
from aiogram.types import InlineQueryResultArticle as Article
from aiogram.types import InlineQuery, InputTextMessageContent
import _thread

f = ''
print(f[:1])
print()

