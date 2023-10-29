from websocket import create_connection
import json

class WebSocket:
    def __init__(self, access_token: str, connection_key: str) -> None:
        self.access_token = access_token
        self.connection_key = connection_key
    
    def connect(self):

        headers = {
            'Pragma': 'no-cache',
            'Origin': 'https://www.freepik.com',
            'Accept-Language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7',
            'Sec-WebSocket-Key': '2gPnOJbN84T0L5JrSxrXog==',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
            'Upgrade': 'websocket',
            'Cache-Control': 'no-cache',
            'Connection': 'Upgrade',
            'Sec-WebSocket-Version': '13',
            'Sec-WebSocket-Extensions': 'permessage-deflate; client_max_window_bits',
        }
        ws = create_connection('wss://realtime.ably.io/?access_token='+self.access_token+'&echo=false&format=json&heartbeats=true&v=2&agent=ably-js%252F1.2.42%2520browser%2520laravel-echo%252F1.0.3', headers=headers)
        xd = json.loads(ws.recv())
        key = xd['connectionDetails']['connectionKey']
        return ws, key
    
    def get_job(self, ws, uuid):
        url_list = []
        ws.send('{"action":10,"channel":"public:tracked-job.'+uuid+'"}')
        while True:
            res = ws.recv()
            if "images" in res:
                for i in json.loads(json.loads(res)['messages'][0]['data'])['images']:
                    url_list.append(i['url'])
                return url_list


