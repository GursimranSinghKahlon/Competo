import requests
#import urllib3 as urllib  
from bs4 import BeautifulSoup
#from pprint import pprint
import re
import datetime
from time import sleep

TOKEN = "#####################"
URL = "https://www.techgig.com/challenge"
CHAT_ID = "############"

class BotHandler:

    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)

    def send_message(self, text, chat_id):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp


def fetch(details):
    #html_doc=urllib.urlopen(URL).read()
    response = requests.get(URL)
    soup = BeautifulSoup(response.content,"html.parser")
    listit = soup.select('div#live-contest-listing div header a')

    for competition in listit:
        details.append(re.sub('[\\n]+',' ',competition.attrs['href'] + ' ' +competition.text))


def main():
    bot = BotHandler(TOKEN)
    bot.send_message('Deployed successfully. ',CHAT_ID)
    while(True):
        now = datetime.datetime.now()    
        #print(now.hour)   
        #bot.send_message(now.hour,CHAT_ID)     
        if now.hour==0:
            break  
        sleep(30)

    while(True):
        details = []
        details2 = []
        fetch(details)
        for item in details:
            #print(item)
            bot.send_message(item,CHAT_ID)
        t=0

        #Check for any new competition every 24 hour
        while(True):
            sleep(3600 * 24)
            #sleep(10)   
             
            #Reset every third day : Receive list of all competitions         
            t+=1
            if t == 3:
                break   

            fetch(details2)
            #pprint(details2)
            bot.send_message('New item : ',CHAT_ID)
            for item in details2:
                if item  not in details:
                    #print(item)
                    #print('New competition : ')
                    bot.send_message('New competition : ',CHAT_ID)
                    bot.send_message(item,CHAT_ID)

if __name__ == '__main__':  
    try:
        main()
    except KeyboardInterrupt:
        exit()