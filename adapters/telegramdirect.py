import argparse
import logging
import os
import re
import requests
from model import WatchResult
from . import SendAdapter

class TelegramDirectSendAdapter(SendAdapter):
    def __init__(self, args):
        self.args = self._parse_args(args)

    def send(self, data: WatchResult) -> bool:
        bot_message = f'Difference is {data.diff} characters\n[{data.url}]({data.url})'
        send_text = 'https://api.telegram.org/bot' + self.args.bot_token + '/sendMessage?chat_id=' + self.args.chat_id + '&parse_mode=Markdown&text=' + bot_message
        r = requests.get(send_text)
        if not 200 <= r.status_code <= 299:
            logging.error(f'Got response status {r.status_code}')
            return False
        return True

    @classmethod
    def get_parser(cls) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(prog=f'Website Watcher – "{cls.get_name()}" Adapter',
                                         description=cls.get_description())
        parser.add_argument('-c', '--chat_id', required=True, type=str, help='Chat ID')
        parser.add_argument('-b', '--bot_token', required=True, type=str, help='Bot Token')

        return parser

    @classmethod
    def get_name(cls) -> str:
        return os.path.basename(__file__)[:-3]

    @classmethod
    def get_description(cls) -> str:
        return 'An adapter to send push messages via Telegram using a bot. See https://core.telegram.org/bots#6-botfather for instructions on creating a bot..'

adapter = TelegramDirectSendAdapter
