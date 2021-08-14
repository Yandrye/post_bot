import re
from igdb.wrapper import IGDBWrapper
import requests
import translate
try:
    import ujson as json
except:
    import json
from typing import Dict
from animeBD import DBHelper
import time


class igdbHelper(object):
    def __init__(self, client_id: str, client_secret: str, db: DBHelper):
        self.db = db
        db_response = db.get_igdb_app_access_token()
        if db_response:
            app_access_token, expire = db_response
        else:
            app_access_token, expire = None, None

        if not app_access_token or time.time() >= expire:
            response = requests.post(
                f"https://id.twitch.tv/oauth2/token?client_id={client_id}&client_secret={client_secret}&grant_type=client_credentials")
            if response.status_code == 200:
                auth = json.loads(response.text)
                app_access_token = auth['access_token']
                expires_in = auth['expires_in']
                expire = int(time.time()) + expires_in
                db.set_igdb_app_access_token(app_access_token, expire)

        self.wrapper = IGDBWrapper(client_id, app_access_token)

    def search(self, game_name: str):
        byte_array = self.wrapper.api_request(
            'games',
            f'fields id, name, cover.url; search "{game_name}";'
        )
        raw_response: Dict = json.loads(byte_array)

        def get_cover_ulr(item):
            url = None
            try:
                url = 'https:' + \
                    item['cover']['url'].replace('thumb', 'cover_big', 1)
            except:
                pass
            return url

        info = [{
            'coverImage': get_cover_ulr(item),
            'title': item['name'],
            'id': item['id']
        }for item in raw_response]

        return info

    def get(self, game_id: int):
        byte_array = self.wrapper.api_request(
            'games',
            f'fields name, platforms.name, genres.name, summary, game_modes.name, cover.url; where id={game_id};'
        )
        raw_response = json.loads(byte_array)
        raw_response: Dict = raw_response[0]
        #print(json.dumps(raw_response, indent=2))

        def get_cover_ulr(item):
            url = None
            try:
                url = 'https:' + \
                    item['cover']['url'].replace('thumb', 'cover_big', 1)
            except:
                pass
            return url

        info = {
            'id': raw_response['id'],
            'coverImage': get_cover_ulr(raw_response),
            'title': raw_response['name'],
            'genres': (['#{0}'.format(x) for x in (y['name'] for y in raw_response['genres'])]) if raw_response.get('genres') else None,
            'game_modes': (', '.join(x for x in (y['name'] for y in raw_response['game_modes']))) if raw_response.get('game_modes') else None,
            'description': (translate.traducir(str(re.sub('<.*?>', '', raw_response.get("summary", ''))))) if raw_response.get('summary') else None,
            'platforms': raw_response.get('platforms', None)
        }
        return info

    def get_date(self, game_id: int, platform_id: int):
        byte_array = self.wrapper.api_request(
            'release_dates',
            f'fields y; where game={game_id} & platform={platform_id};'
        )
        raw_response: Dict = json.loads(byte_array)
        return sorted([y["y"] for y in raw_response])[0]
