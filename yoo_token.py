import configparser
read_config = configparser.ConfigParser()
read_config.read("settings.ini")
from yoomoney import Authorize

if read_config['settings']['yoomoney_client_id'].strip().replace(" ", "") == "":
       print("Вставьте client_id в settings.ini!")

if read_config['settings']['yoomoney_redirect_uri'].strip().replace(" ", "") == "":
       print("Вставьте redirect_uri в settings.ini!") 

if read_config['settings']['yoomoney_client_id'].strip().replace(" ", "") != "" and read_config['settings']['yoomoney_redirect_uri'].strip().replace(" ", "") != "":
       client_id = read_config['settings']['yoomoney_client_id'].strip().replace(" ", "")
       redirect_uri = read_config['settings']['yoomoney_redirect_uri'].strip().replace(" ", "")
       Authorize(
              client_id=client_id,
              redirect_uri=redirect_uri,
              scope=["account-info",
                     "operation-history",
                     "operation-details",
                     "incoming-transfers",
                     "payment-p2p",
                     "payment-shop",
                     ]
              )