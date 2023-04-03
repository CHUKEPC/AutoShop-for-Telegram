# - *- coding: utf- 8 - *-
import asyncio
import configparser
import requests

read_config = configparser.ConfigParser()
read_config.read("settings.ini")
lolz_token = read_config['settings']['lolz_token']

def get_user():

    api_url = 'https://api.zelenka.guru'
    session_headers = {'Authorization': f'Bearer {lolz_token}'}

    if lolz_token == "":
        return print("Введите токен лолза в settings.ini!!!")

    try:
        user = requests.get(url=f"{api_url}/market/me", headers=session_headers)
        if user.status_code == 200:
            response = user.json()
            if 'user' not in response.keys():
                raise ValueError('Invalid Token [Lolzteam Market]')

            return response['user']
        else:
            error = user.text
            error = error.split('<h1>')[1].split('</h1>')[0]
            raise BaseException(error)
    except BaseException as err:
        print("Ошибка: ", err)

if __name__ == "__main__":
    user = get_user()
    print(f"ID: {user['user_id']} \nНик: {user['username']} \nБаланс: {user['balance']} RUB (В холде: {user['hold']} RUB)")