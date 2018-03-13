# -*- coding: utf-8 -*-
"""
Created on Mon Mar 12 09:43:12 2018

@author: KR_NefedovAS
"""
import config
import requests

class MyBot():
    def __init__(self, token):
        self.token = token
        self.url  =r'https://api.telegram.org/bot{}/'.format(self.token)
    
    def get_updates(self, offset=None, timeout=30):
        method = 'getUpdates'
        params = {'timeout':timeout, 'offset':offset}
        r = requests.get(self.url + method, params)
        return r.json()['result']
    
    def send_message(self, chat_id, text):
        method = 'sendMessage'
        params = {'chat_id':chat_id, 'text':text}
        r = requests.post(self.url+method, params)
        return r
    
    def get_last_update(self):
        get_result = self.get_updates()
        if len(get_result) > 0:
            last_update = get_result[-1]
        else:
            last_update = None
        return last_update

bot = MyBot(config.token)
def main():    
    new_offset = bot.get_updates()[-1]['update_id']+1
    while True:
        bot.get_updates(new_offset)
        last_update = bot.get_last_update()
        if last_update is None:
            continue
        last_chat_id = last_update['message']['chat']['id']
        last_message = last_update['message']['text']
        bot.send_message(last_chat_id, last_message)
        new_offset = last_update['update_id']+1

if __name__=='__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()


        
