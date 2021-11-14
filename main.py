from colorama.ansi import Fore
import requests, threading, random, time, string, colorama, json


settings = json.loads(open('settings.json', 'r').read())

colorama.init()

guilds = settings['guilds']
message_ = settings['messages']
tokens = open('tokens.txt', 'r').read().splitlines()
proxies = open('proxies.txt', 'r').read().splitlines()

headers = {
    'authority': 'canary.discord.com',
    'accept-language': 'en-US',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.34 Chrome/83.0.4103.122 Electron/9.3.5 Safari/537.36',
    'accept': '*/*',
    'origin': 'https://canary.discord.com',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://canary.discord.com/channels/@me',
    'content-type': 'application/json',
    'authorization':random.choice(tokens)
}

userIds = []
past = [0]

offset = 0
ok = ''

timeout_bruh = False

print(colorama.Fore.WHITE + '[=] - Searching for users..')

for guild in guilds:
    for x in range(settings['userSearch']):
        try:
            req = requests.get(f'https://discord.com/api/v9/guilds/{guild}/messages/search?content=a{ok}', headers=headers).json()
            req = req['messages']
            for message in req:
                userId = message[0]['author']['id']
                if past.count(userId) < 1:
                    past.append(userId)
                    userIds.append(userId)
                    offset += 25
                    ok = f'&offset={offset}'
        except:
            pass
        time.sleep(1)
    time.sleep(1)

random.shuffle(userIds)

time.sleep(3)
print(colorama.Fore.YELLOW + f'-> We have found ({len(userIds)}) amount of Users to send a message to from {len(guilds)} amount of guilds!')

def checkChannel(token, getUserId):
    try:
        headers = {
            'authority': 'canary.discord.com',
            'accept-language': 'en-US',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.34 Chrome/83.0.4103.122 Electron/9.3.5 Safari/537.36',
            'accept': '*/*',
            'origin': 'https://canary.discord.com',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://canary.discord.com/channels/@me',
            'content-type': 'application/json',
            'authorization':token,
            "x-super-properties":"eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzkzLjAuNDU3Ny44MiBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiOTMuMC40NTc3LjgyIiwib3NfdmVyc2lvbiI6IjEwIiwicmVmZXJyZXIiOiJodHRwczovL2Rpc2NvcmQuY29tL2xvZ2luIiwicmVmZXJyaW5nX2RvbWFpbiI6ImRpc2NvcmQuY29tIiwicmVmZXJyZXJfY3VycmVudCI6IiIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjk3NjYyLCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ==",
            "sec-ch-ua":'Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Windows",
        }

        cookies = requests.get('https://canary.discord.com/channels/@me', headers=headers).cookies

        createDM = requests.post(
            'https://canary.discord.com/api/users/@me/channels',

            headers=headers,

            proxies={'http':random.choice(proxies), 'https':random.choice(proxies)},

            cookies=cookies,

            json={
                'recipient_id':getUserId
            }
        ).json()


        author = createDM['recipients'][0]['username'] + '#' + createDM['recipients'][0]['discriminator']
        createDM = createDM['id']

        generated_message = random.choice(message_)
        
        time.sleep(settings['delay'])

        sendMSG = requests.post(
            f'https://canary.discord.com/api/v9/channels/{createDM}/messages',

            headers=headers,

            proxies={'http':random.choice(proxies), 'https':random.choice(proxies)},

            cookies=cookies,

            json={
                'content':generated_message
            }
        )

        if sendMSG.status_code == 200:
            print(colorama.Fore.GREEN + f'[+] - Advertisement Sent | Reciever: [{author}]')
        else:
            print(colorama.Fore.RED + f'[!] - Advertisement Failed | Reciver: [{author}]')


        if sendMSG.status_code == 403:
            global timeout_bruh
            timeout_bruh = True
    except:
        pass
            
count = 0
for userid in userIds:
    if timeout_bruh == True:
        print(colorama.Fore.YELLOW + '- Detected Ratelimit (30 Second stop on threads)')
        time.sleep(30)
        timeout_bruh = False
    if settings['random'] == False:
        try:
            time.sleep(settings['delay'])
            token = tokens[count]
            # tokens.remove(token)
            s = threading.Thread(target=checkChannel, args=(token,userid)).start()
            count += 1
        except:
            time.sleep(settings['delay'])
            count = 0
            token = tokens[count]
            s = threading.Thread(target=checkChannel, args=(token,userid)).start()
            count += 1
    elif settings['random'] == True:
        token = random.choice(tokens)
        s = threading.Thread(target=checkChannel, args=(token,userid)).start()
        time.sleep(settings['delay'])
