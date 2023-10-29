import random, json, httpx, random, string, threading

from core import api

class Account:
    def __init__(self, cookies: dict, proxie: str) -> None:
        self.cookies = cookies
        self.proxie = proxie
        self.api_client = api.Api(cookies=cookies,proxie=proxie)

    def generate_image(self, image_count: int = 1, prompt: str = ""):
        aspect_ratio_list = ['square','portrait','landscape']
        return self.api_client.send_prompt(prompt, image_count, 'square')



if __name__ == "__main__":
    def thread():
        for i in range(100):
            try:
                proxie = random.choice(open("proxies.txt","r").read().splitlines())
                accounts = open("accounts.txt","r").read().splitlines()
                cookie = json.loads(random.choice(accounts))
                client = Account(cookies=cookie, proxie=proxie)
                res = client.generate_image(4, "logo, app, icon, red-black, hacking, flat")
                for i in res:
                    open("images/"+''.join(random.choice(string.ascii_letters) for i in range(7))+".jpg","wb").write(httpx.get(i).content)
            except:
                pass
    for i in range(10):
        threading.Thread(target=thread).start()