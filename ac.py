
import capsolver
import httpx
import random
import string
import json
import threading

def thread():
    while True:
        try:
            capsolver.api_key = "Key"
            PAGE_URL = "https://id.freepikcompany.com"
            PAGE_KEY  = "6LfEmSMUAAAAAEDmOgt1G7o7c53duZH2xL_TXckC"
            PAGE_ACTION = """message ClientVariations {repeated int32 variation_id = [3325708];}"""

            def solve_recaptcha_v3_enterprise(url,key,pageAction):
                solution = capsolver.solve({
                    "type": "ReCaptchaV2EnterpriseTaskProxyLess",
                    "websiteURL": url,
                    "websiteKey":key,
                    "pageAction":pageAction,
                })
                return solution

            solution = solve_recaptcha_v3_enterprise(PAGE_URL, PAGE_KEY, PAGE_ACTION)
            token = solution["gRecaptchaResponse"]

            headers = {
                'authority': 'id-api.freepikcompany.com',
                'accept': '*/*',
                'accept-language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7',
                'content-type': 'application/json',
                'origin': 'https://id.freepikcompany.com',
                'referer': 'https://id.freepikcompany.com/',
                'sec-ch-ua': '"Not=A?Brand";v="99", "Chromium";v="118"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-site',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
            }

            params = {
                'client_id': 'freepik',
            }

            email = ''.join(random.choice(string.ascii_letters) for i in range(7)) + random.choice(["@hotmail.com",])
            print(email)
            json_data = {
                'email': email,
                'password': ''.join(random.choice(string.ascii_letters + string.digits) for i in range(10)) + "!",
                'recaptchaToken': token,
                'disableNews': False,
                'lang': 'en-US',
                'rememberedUser': 1,
            }

            proxie = random.choice(open("proxies.txt","r").read().splitlines())

            response = httpx.post(
                'https://id-api.freepikcompany.com/v2/signup',
                params=params,
                headers=headers,
                json=json_data,
                proxies="http://" + proxie
            )
            print(response.text)
            res = response.json()
            if res['success'] == True:
                cookies = dict(httpx.get(res['data']['redirectUrl'],headers=headers, proxies="http://" +proxie).cookies)
                open("accounts.txt","a").write(json.dumps(cookies) + "\n")
            else:
                print(res['message'])
        except:
            pass

for i in range(10):
    threading.Thread(target=thread).start()