import configparser
import requests
import os 

def NotifyTelegramBot(textMessage):
    ConfigPath = "/root/notificationConfig.ini"
    #print("[+] Sending notification to telegram bot")
    config = configparser.RawConfigParser()
    if os.path.isfile(ConfigPath):
        config.read(ConfigPath)
        if config.has_option("telegram","apiToken") and config.has_option("telegram","chatId"): 
            apiToken = config.get("telegram","apiToken")
            chatId = config.get("telegram","chatId")
            send_text = 'https://api.telegram.org/bot'+apiToken+'/sendMessage?chat_id='+chatId+'&parse_mode=Markdown&text='+textMessage
            response = requests.post(send_text)
            if response.status_code == 200:
                #print("\t[!] Message Send successfully")
                pass
        else:
            print("[-] Error : no credentials are setted for Telegram bot (API token and ChatId)")
    else:
        print("[-] Error : There is no config file available '/root/notificationConfig.ini'")
