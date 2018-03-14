# -*- coding: utf-8 -*-
"""
Created on Mon Mar 12 09:43:12 2018

@author: KR_NefedovAS
"""

import sys
sys.path.append(r'C:\Users\KR_NefedovAS\Desktop\Trash\telegBot\test1')
import config
import requests

headers = {'Authorization':'Bearer '+config.token_dialog}
url = 'https://api.dialogflow.com/v1/'
method = 'query'
params = {'query':'Как дела', 'v':'20150910', 'lang':'ru', 'sessionId':'12345'}
r = requests.get(url+method, params, headers=headers)

def SmallTalk(token, query_string, sessionId):
    headers = {'Authorization':'Bearer '+token}
    url = 'https://api.dialogflow.com/v1/'
    method = 'query'
    params = {'query':query_string, 'v':'20150910', 'lang':'ru', 'sessionId':str(sessionId)}
    r = requests.get(url+method, params, headers=headers)
    return r.json()['result']['fulfillment']['speech']
    
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

bot = MyBot(config.token_telebot)
def main():    
#    new_offset = bot.get_updates()[-1]['update_id']+1
    new_offset = None
    while True:
        bot.get_updates(new_offset)
        last_update = bot.get_last_update()
        if last_update is None:
            continue
        last_chat_id = last_update['message']['chat']['id']
        last_message = last_update['message']['text']
        answer = SmallTalk(config.token_dialog, last_message, '12345')
        bot.send_message(last_chat_id, answer)
        new_offset = last_update['update_id']+1

if __name__=='__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()


        
