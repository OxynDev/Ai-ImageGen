import httpx, random, time, uuid as uuidlib
import asyncio
from ably import AblyRest, AblyRealtime



from . import ws

class Api:

    XSRF_TOKEN = None
    wepik_session_v2 = None


    def __init__(self, cookies: dict, proxie: str) -> None:
        self.cookies = cookies
        self.proxie = proxie

        self.get_xsrf_token()

    def get_xsrf_token(self):

        headers = {
            'authority': 'www.freepik.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7',
            'sec-ch-ua': '"Not=A?Brand";v="99", "Chromium";v="118"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
        }

        params = {
            'prompt': 'asdasdas',
            'style': 'noStyle',
        }

        response = httpx.get('https://www.freepik.com/ai-images-editor', params=params, cookies=self.cookies, headers=headers, proxies="http://"+self.proxie)
        self.XSRF_TOKEN = response.cookies['XSRF-TOKEN']


    def get_websocket_token(self):

        headers = {
            'authority': 'www.freepik.com',
            'accept': 'application/json, application/json',
            'accept-language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-type': 'application/json, application/json',
            'origin': 'https://www.freepik.com',
            'referer': 'https://www.freepik.com/ai-images-editor?prompt=asdasdas&style=noStyle',
            'sec-ch-ua': '"Not=A?Brand";v="99", "Chromium";v="118"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
        }

        params = {
            'rnd': str(random.randint(1398900880916657,9398900880916657)),
        }

        data = '{"channel_name":null,"token":null}'

        response = httpx.post(
            'https://www.freepik.com/ai-images-editor/broadcasting/auth',
            params=params,
            cookies=self.cookies,
            headers=headers,
            data=data,
            proxies="http://"+self.proxie
        )

        return response.json()['token']


    def get_connection_key(self, token):

        headers = {
            'authority': 'rest.ably.io',
            'accept': 'application/json',
            'accept-language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7',
            'origin': 'https://www.freepik.com',
            'referer': 'https://www.freepik.com/ai-images-editor?prompt=asdasdas&style=noStyle',
            'sec-ch-ua': '"Not=A?Brand";v="99", "Chromium";v="118"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
        }

        params = {
            'access_token': token,
            'echo': 'false',
            'stream': 'false',
            'heartbeats': 'true',
            'v': '2',
            'agent': 'ably-js%2F1.2.42%20browser%20laravel-echo%2F1.0.3',
            'rnd': str(random.randint(1398900880916657,9398900880916657)),
        }

        response = httpx.get('https://rest.ably.io/comet/connect', params=params, headers=headers, proxies="http://"+self.proxie)
        ckey = response.json()[0]['connectionDetails']['connectionKey']

        headers = {
            'authority': 'rest.ably.io',
            'accept': 'application/json',
            'accept-language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7',
            'origin': 'https://www.freepik.com',
            'referer': 'https://www.freepik.com/ai-images-editor?prompt=asdasdas&style=noStyle',
            'sec-ch-ua': '"Not=A?Brand";v="99", "Chromium";v="118"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
        }

        params = {
            'access_token': token,
            'echo': 'false',
            'stream': 'false',
            'heartbeats': 'true',
            'v': '2',
            'agent': 'ably-js%2F1.2.42%20browser%20laravel-echo%2F1.0.3',
            'rnd': str(random.randint(1398900880916657,9398900880916657)),
            'upgrade': ckey
        }
        response = httpx.get(
            'https://rest.ably.io/comet/connect',
            headers=headers,params=params
        )

        headers = {
            'authority': 'rest.ably.io',
            'accept': '*/*',
            'accept-language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7',
            'access-control-request-headers': 'content-type',
            'access-control-request-method': 'POST',
            'origin': 'https://www.freepik.com',
            'referer': 'https://www.freepik.com/ai-images-editor?prompt=asdasdas&style=noStyle',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
        }

        params = {
            'access_token': token,
            'rnd': str(random.randint(1398900880916657,9398900880916657)),
        }

        response = httpx.options(
            'https://rest.ably.io/comet/'+ckey+'/send',
            params=params,
            headers=headers, proxies="http://"+self.proxie
        )

        return ckey

    def send_prompt(self, prompt: str, image_count: int = 1, aspect_ratio: str = "square"):

        headers = {
            'authority': 'www.freepik.com',
            'accept': 'application/json',
            'accept-language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-type': 'application/json',
            'origin': 'https://www.freepik.com',
            'referer': 'https://www.freepik.com/ai-images-editor?prompt=asdasdas&style=noStyle',
            'sec-ch-ua': '"Not=A?Brand";v="99", "Chromium";v="118"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
            'x-requested-with': '3',
            'x-xsrf-token': self.XSRF_TOKEN,
        }

        params = {
            'lang': 'en',
            'cacheBuster': '2',
        }

        json_data = {
            'uuid': str(uuidlib.uuid1()),
            'prompt': prompt,
            'modifiers': [],
            'aspect_ratio': aspect_ratio,
            'images': image_count,
        }

        response = httpx.post(
            'https://www.freepik.com/ai-images-editor/api/image/ai',
            params=params,
            cookies=self.cookies,
            headers=headers,
            json=json_data, 
            proxies="http://"+self.proxie
        )
        print(response.text)
        uuid = response.json()['uuid']
        self.wepik_session_v2 = response.cookies['wepik_session_v2']
        self.cookies['wepik_session_v2'] = self.wepik_session_v2
        token = self.get_websocket_token()
        key = self.get_connection_key(token)
        websocket = ws.WebSocket(access_token=token, connection_key=key)
        ws_connection, key = websocket.connect()
        url_list = websocket.get_job(ws_connection, uuid)

        return url_list