import requests
import urllib2 as urllib  
from bs4 import BeautifulSoup
from pprint import pprint
import re

TOKEN = "#########################"
URL = "https://www.techgig.com/challenge"
CHAT_ID = "########"

class BotHandler:

    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)

    def send_message(self, text, chat_id):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

bot = BotHandler(TOKEN)

html_doc=urllib.urlopen(URL).read()
soup = BeautifulSoup(html_doc, 'lxml')
listit = soup.select('div#live-contest-listing div header a')

details = []
for competition in listit:
    details.append(re.sub('[\\n]+',' ',competition.attrs['href'] + ' ' +competition.text))

pprint(details)
for item in details:
    print(bot.send_message(item,CHAT_ID))
